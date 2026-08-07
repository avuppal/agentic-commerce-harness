import logging
from typing import List, Dict, Any, Optional

# Import necessary models and services
# Assuming these modules and classes exist or will be created shortly.
# Adjust imports based on actual file locations.
from src.vc_handler.vc_validator import VCValidator, VCValidationResult
from src.sige.unit_price_normalizer import UnitPriceNormalizer, NormalizedPrice
from src.sige.explainability_logger import ExplainabilityLogger, DecisionLogEntry
from src.dpp_parser.dpp_models import DigitalProductPassport

# Define a type alias for the structured query output from NLP processor
StructuredQuery = Dict[str, Any]

# Helper function to safely get nested values from a dictionary
def get_nested_value(data_dict: dict, path: str):
    """
    Safely retrieves a value from a nested dictionary using a dot-separated path.

    Args:
        data_dict (dict): The dictionary to search.
        path (str): A dot-separated string representing the path (e.g., 'unit_pricing.price').

    Returns:
        The value if found, otherwise None.
    """
    keys = path.split('.')
    current_level = data_dict
    for key in keys:
        if not isinstance(current_level, dict):
            return None
        current_level = current_level.get(key)
        if current_level is None:
            return None
    return current_level

class ShortlistingOrchestrator:
    """
    Orchestrates the product shortlisting process, applying filters, verification, normalization, and sorting.
    """

    def __init__(self, vc_validator: VCValidator, unit_price_normalizer: UnitPriceNormalizer, explainability_logger: ExplainabilityLogger):
        self.vc_validator = vc_validator
        self.unit_price_normalizer = unit_price_normalizer
        self.xai_logger = explainability_logger
        self.logger = logging.getLogger(__name__)
        # Ensure logger has handlers if not configured globally
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(logging.StreamHandler())

    def shortlist_products(self, product_stream: List[DigitalProductPassport], structured_query: StructuredQuery) -> List[DigitalProductPassport]:
        """
        Orchestrates the product shortlisting process based on the W3C spec.
        
        Args:
            product_stream: A list of candidate products (DigitalProductPassport objects).
            structured_query: The structured intent from the NLP processor.
            
        Returns:
            A sorted list of shortlisted products that meet all criteria.
        """
        self.logger.info(f"Starting shortlisting for {len(product_stream)} products with query: {structured_query}")
        
        # 1. Filter products using hard constraints from structured_query
        hard_constraints = structured_query.get("hard_constraints", [])
        filtered_products = self._apply_hard_constraints(product_stream, hard_constraints)
        self.logger.info(f"Filtered down to {len(filtered_products)} products after hard constraints.")

        # 2. Call vc_validator for claim verification on remaining products
        # This step will involve iterating through products and their claims.
        # We will store validation results with each product.
        products_with_vc_results = []
        for product in filtered_products:
            validated_claims = []
            total_claim_score = 0.0
            claim_count = 0

            for claim in product.certification_claims: # Assuming certification_claims is a list of VCs
                vc_validation_result: VCValidationResult = self.vc_validator.validate_claims(claim)
                validated_claims.append({
                    "claim": claim.credentialSubject, # Or a relevant identifier for the claim
                    "validation_result": vc_validation_result.model_dump() # Store the whole result for logging
                })
                total_claim_score += vc_validation_result.score
                claim_count += 1

                if not vc_validation_result.is_valid:
                    self.xai_logger.log_decision(
                        product_id=product.gtin, # Use GTIN as product ID
                        decision="REJECTED",
                        gate="VC_VERIFICATION",
                        reason=f"Product rejected due to invalid claim: {vc_validation_result.reason}",
                        evidence={"claim": claim.credentialSubject, "validation_details": vc_validation_result.model_dump()}
                    )
            
            # Add aggregated VC validation info to product if needed, or just store results
            product_data = product.model_dump() # Convert Pydantic model to dict for easier manipulation
            product_data["_vc_validation_results"] = validated_claims
            product_data["_vc_score"] = (total_claim_score / claim_count) if claim_count > 0 else 1.0 # Default to 1.0 if no claims
            products_with_vc_results.append(product_data)
        
        self.logger.info(f"Completed VC validation for {len(products_with_vc_results)} products.")

        # 3. Call unit_price_normalizer for standardized cost
        products_with_normalized_price = []
        for product_data in products_with_vc_results:
            normalized_price: Optional[NormalizedPrice] = None
            price_info = product_data.get("unit_pricing")
            if price_info:
                try:
                    # Assuming unit_price_normalizer expects a dict or Pydantic model representing UnitPriceSpecification
                    normalized_price = self.unit_price_normalizer.normalize_price(price_info)
                    product_data["_normalized_price"] = normalized_price.model_dump() # Store normalized price
                except Exception as e:
                    self.logger.error(f"Failed to normalize price for product {product_data.get('gtin')}: {e}")
                    # Decide how to handle: reject product, log warning, etc.
                    self.xai_logger.log_decision(
                        product_id=product_data.get('gtin'),
                        decision="REJECTED",
                        gate="PRICE_NORMALIZATION",
                        reason=f"Failed to normalize unit price: {e}",
                        evidence={"unit_pricing_data": price_info}
                    )
                    # Skip this product if price normalization fails and is critical
                    continue 
            else:
                # If unit pricing is missing, it might be a hard constraint violation or requires specific handling
                self.logger.warning(f"Product {product_data.get('gtin')} missing unit_pricing information.")
                self.xai_logger.log_decision(
                    product_id=product_data.get('gtin'),
                    decision="REJECTED",
                    gate="PRICE_NORMALIZATION",
                    reason="Missing unit_pricing information required for comparison.",
                    evidence={}
                )
                continue # Skip product if price info is essential
            
            products_with_normalized_price.append(product_data)
        
        self.logger.info(f"Completed unit price normalization for {len(products_with_normalized_price)} products.")

        # 4. Sort the remaining products
        # Sorting criteria: low unit-price, high claim verification scores, trusted merchant domain reputation.
        # This is a simplified sorting; a more complex propensity score might be needed.
        
        # Add merchant reputation to product data if available and not already present
        # For now, assuming merchant reputation is part of product_data if available from DPP.
        # If not, it might need to be fetched separately.

        def sort_key(product_data):
            normalized_price_val = product_data.get("_normalized_price", {}).get("value", float('inf')) # High value for missing price
            vc_score = product_data.get("_vc_score", 0.0) # Default to 0 if no VC score
            # Merchant reputation would need to be defined and fetched. For now, using a placeholder.
            # Example: merchant_reputation_score = product_data.get("merchant_reputation", {}).get("reputation", 0.0)
            # Higher VC score and merchant reputation should contribute positively, lower price positively.
            # A common approach is to create a composite score.
            
            # Simple composite score: prioritize low price, then VC score.
            # Lower price is better, so we use normalized_price_val directly.
            # Higher VC score is better, so we use vc_score.
            # The prompt mentions "trusted merchant domain reputation" as a factor, but we don't have that data directly here.
            # For now, focusing on price and VC score.
            
            # Example sorting logic: Primarily by normalized price (ascending), secondarily by VC score (descending).
            return (normalized_price_val, -vc_score) # Negative vc_score for descending order

        sorted_products = sorted(products_with_normalized_price, key=sort_key)
        self.logger.info(f"Sorted {len(sorted_products)} products.")

        # 5. Use explainability_logger to document each filtering or sorting decision
        # This is partially done within the loops above. Final log for shortlisted items.
        final_shortlist = []
        for i, product_data in enumerate(sorted_products):
            # Log shortlisted products
            self.xai_logger.log_decision(
                product_id=product_data.get('gtin'),
                decision="SHORTLISTED",
                gate="FINAL_SORTING",
                reason=f"Product selected as rank #{i+1} based on price and claim verification.",
                evidence={
                    "rank": i+1,
                    "normalized_price": product_data.get("_normalized_price"),
                    "vc_score": product_data.get("_vc_score")
                }
            )
            final_shortlist.append(product_data)

        self.logger.info(f"Shortlisting complete. {len(final_shortlist)} products shortlisted.")
        return final_shortlist

    def _apply_hard_constraints(self, products: List[Dict[str, Any]], constraints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters products based on hard constraints from the structured query.

        Args:
            products: A list of product dictionaries.
            constraints: A list of constraint dictionaries.

        Returns:
            A list of products that satisfy all hard constraints.
        """
        filtered_products = []
        for product_dict in products: # Expecting dicts here from product.model_dump()
            is_compliant = True
            product_id = product_dict.get('gtin', 'Unknown Product')

            for constraint in constraints:
                attribute_path = constraint.get('attribute')
                expected_value = constraint.get('value')
                operator = constraint.get('operator', '==') # Default to equality

                if not attribute_path or expected_value is None:
                    self.logger.warning(f"Skipping invalid constraint: {constraint}")
                    continue

                product_value = get_nested_value(product_dict, attribute_path)

                constraint_check_failed = False
                if product_value is None:
                    # Attribute not found on product, constraint cannot be met
                    constraint_check_failed = True
                    reason = f"Hard constraint check failed: Attribute '{attribute_path}' not found on product."
                elif operator == 'LESS_THAN_OR_EQUAL_TO':
                    if not (product_value <= expected_value):
                        constraint_check_failed = True
                elif operator == 'GREATER_THAN_OR_EQUAL_TO':
                    if not (product_value >= expected_value):
                        constraint_check_failed = True
                elif operator == 'LESS_THAN':
                    if not (product_value < expected_value):
                        constraint_check_failed = True
                elif operator == 'GREATER_THAN':
                    if not (product_value > expected_value):
                        constraint_check_failed = True
                elif operator == '==':
                    if product_value != expected_value:
                        constraint_check_failed = True
                elif operator == '!=':
                    if product_value == expected_value:
                        constraint_check_failed = True
                elif operator == 'IN':
                    if not (product_value in expected_value): # Expecting expected_value to be a list or set
                        constraint_check_failed = True
                elif operator == 'NOT_IN':
                    if not (product_value not in expected_value): # Expecting expected_value to be a list or set
                        constraint_check_failed = True
                elif operator == 'CONTAINS':
                    # Assumes product_value is iterable (e.g., list of strings) and expected_value is a single item
                    if not (expected_value in product_value):
                        constraint_check_failed = True
                elif operator == 'NOT_CONTAINS':
                    # Assumes product_value is iterable (e.g., list of strings) and expected_value is a single item
                    if not (expected_value not in product_value):
                        constraint_check_failed = True
                else:
                    self.logger.warning(f"Unsupported operator '{operator}' in constraint: {constraint}")
                    constraint_check_failed = True # Treat unsupported operator as failure

                if constraint_check_failed:
                    self.xai_logger.log_decision(
                        product_id=product_id,
                        decision="REJECTED",
                        gate="HARD_CONSTRAINT",
                        reason=reason if 'reason' in locals() else f"Hard constraint '{attribute_path}' ({operator} {expected_value}) failed.",
                        evidence=constraint
                    )
                    is_compliant = False
                    break # No need to check further constraints for this product
            
            if is_compliant:
                filtered_products.append(product_dict)

        return filtered_products


# Example Usage (for testing purposes, would be called by orchestrator) - Not part of the class implementation
if __name__ == '__main__':
    # Mock implementations for demonstration
    class MockVCValidator:
        def validate_claims(self, claim):
            class MockVCValidationResult(VCValidationResult):
                def __init__(self, is_valid, status, reason, score):
                    self.is_valid = is_valid
                    self.status = status
                    self.reason = reason
                    self.score = score
            if "Organic" in str(claim): # Simple mock logic
                return MockVCValidationResult(is_valid=True, status="VALID", reason="Mock organic claim is valid.", score=1.0)
            elif "Fair Trade" in str(claim):
                return MockVCValidationResult(is_valid=False, status="REVOKED", reason="Mock fair trade claim is revoked.", score=0.0)
            else:
                return MockVCValidationResult(is_valid=False, status="INVALID_SIGNATURE", reason="Mock claim signature invalid.", score=0.0)

    class MockUnitPriceNormalizer:
        def normalize_price(self, price_spec):
            class MockNormalizedPrice(NormalizedPrice):
                 def __init__(self, value, base_unit, currency):
                    self.value = value
                    self.base_unit = base_unit
                    self.currency = currency

            # Mock normalization logic: Price per 100g or 100ml
            price = price_spec.get('price', 0)
            unit = price_spec.get('referenceQuantity', {}).get('unitCode', '')
            value = price_spec.get('referenceQuantity', {}).get('value', 1)

            if unit.lower() in ['g', 'kg', 'oz', 'lb', 'gram', 'kilogram', 'ounce', 'pound']:
                # Convert to grams first if kg, oz, lb
                if unit.lower() in ['kg', 'kilogram']:
                    value *= 1000
                elif unit.lower() in ['oz', 'ounce']:
                    value *= 28.3495
                elif unit.lower() in ['lb', 'pound']:
                    value *= 453.592
                
                normalized_value = (price / value) * 100 # Price per 100g
                return MockNormalizedPrice(value=normalized_value, base_unit="100g", currency=price_spec.get('priceCurrency', 'USD'))
            elif unit.lower() in ['ml', 'l', 'fl_oz', 'gallon']:
                 # Convert to ml first if l, fl_oz, gal
                if unit.lower() in ['l', 'liter']:
                    value *= 1000
                elif unit.lower() in ['fl_oz', 'fluid_ounce']:
                    value *= 29.5735
                elif unit.lower() in ['gal', 'gallon']:
                    value *= 3785.41
                normalized_value = (price / value) * 100 # Price per 100ml
                return MockNormalizedPrice(value=normalized_value, base_unit="100ml", currency=price_spec.get('priceCurrency', 'USD'))
            elif unit.lower() in ['pce', 'pc', 'piece', 'count', 'ct', 'ea', 'each']:
                normalized_value = price # Price per piece
                return MockNormalizedPrice(value=normalized_value, base_unit="piece", currency=price_spec.get('priceCurrency', 'USD'))
            else:
                raise ValueError(f"Unknown unit: {unit}")

    class MockExplainabilityLogger:
        def __init__(self):
            self.log_entries = []
            self.logger = logging.getLogger('XAI_Logger')
            if not self.logger.handlers:
                self.logger.setLevel(logging.INFO)
                self.logger.addHandler(logging.StreamHandler())

        def log_decision(self, product_id, decision, gate, reason, evidence=None):
            entry = {
                "product_id": product_id,
                "decision": decision,
                "gate": gate,
                "reason": reason,
                "evidence": evidence or {},
                "timestamp": "mock_timestamp"
            }
            self.log_entries.append(entry)
            self.logger.info(f"XAI Log: {entry}")

    # Sample Product Data (mock DigitalProductPassport objects)
    # Need to create mock DigitalProductPassport objects that have .model_dump() and GTIN.
    # For simplicity, using dicts that mimic the structure.
    class MockDigitalProductPassport(Dict[str, Any]):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.gtin = kwargs.get('gtin') # Ensure GTIN is accessible
            # Mock certification_claims to be a list of strings for simplicity in mock validator
            self.certification_claims = kwargs.get('certification_claims', [])
            # Mock unit_pricing to be a dict for simplicity in mock normalizer
            self.unit_pricing = kwargs.get('unit_pricing', {})
        
        def model_dump(self):
            return dict(self)

    mock_products = [
        MockDigitalProductPassport( 
            gtin="1234567890123", 
            name="Organic Oat Milk", 
            certification_claims=["USDA Organic", "Non-GMO Project Verified"],
            unit_pricing={'price': 3.99, 'priceCurrency': 'USD', 'referenceQuantity': {'value': 1, 'unitCode': 'L'}},
            gs1_allergenInformation=["Dairy", "Gluten"]
        ),
        MockDigitalProductPassport( 
            gtin="9876543210987", 
            name="Regular Oat Milk", 
            certification_claims=["Fair Trade Certified"],
            unit_pricing={'price': 2.99, 'priceCurrency': 'USD', 'referenceQuantity': {'value': 1, 'unitCode': 'L'}},
            gs1_allergenInformation=["Dairy"]
        ),
        MockDigitalProductPassport( 
            gtin="1122334455667", 
            name="Premium Organic Soy Milk", 
            certification_claims=["USDA Organic"],
            unit_pricing={'price': 4.50, 'priceCurrency': 'USD', 'referenceQuantity': {'value': 0.946, 'unitCode': 'L'}},
            gs1_allergenInformation=["Soy", "Gluten"]
        ),
        MockDigitalProductPassport( 
            gtin="7788990011223", 
            name="Gluten-Free Bread", 
            certification_claims=["Certified Gluten-Free"],
            unit_pricing={'price': 5.99, 'priceCurrency': 'USD', 'referenceQuantity': {'value': 500, 'unitCode': 'g'}},
            gs1_allergenInformation=["Gluten"]
        )
    ]

    # Mock structured query
    mock_structured_query = {
        "gpc_category_code": "10000000",
        "hard_constraints": [
            {"attribute": "gs1_allergenInformation", "operator": "NOT_CONTAINS", "value": "Gluten"},
            {"attribute": "unit_pricing.price", "operator": "LESS_THAN_OR_EQUAL_TO", "value": 4.00}
        ],
        "soft_preferences": [
            # Not used in this basic example, but would be for ranking
        ]
    }

    # Instantiate mocks
    mock_vc_validator = MockVCValidator()
    mock_unit_price_normalizer = MockUnitPriceNormalizer()
    mock_explainability_logger = MockExplainabilityLogger()

    # Instantiate orchestrator
    orchestrator = ShortlistingOrchestrator(
        vc_validator=mock_vc_validator,
        unit_price_normalizer=mock_unit_price_normalizer,
        explainability_logger=mock_explainability_logger
    )

    # Run the shortlisting
    shortlisted = orchestrator.shortlist_products(mock_products, mock_structured_query)

    print("\n--- Shortlisted Products --- ")
    for product in shortlisted:
        print(f"- GTIN: {product.get('gtin')}, Name: {product.get('name')}")

    print("\n--- XAI Log Entries ---")
    for entry in mock_explainability_logger.log_entries:
        print(entry)
