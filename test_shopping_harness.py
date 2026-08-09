import sys
import os
import json
import logging

# Ensure src/ is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.sige.query_engine import QueryEngine
from src.vc_handler.vc_validator import VerifiableCredentialValidator
from src.sige.unit_price_normalizer import UnitPriceNormalizer
from src.approval_manager.approval_trigger import ApprovalTrigger

def run_shopping_test():
    prompt = "all the ingredients to shop a vegetarian pizza organic and gluten free"
    
    print("=========================================================================================")
    print("                 LIVE END-TO-END AUTONOMOUS SHOPPING PIPELINE                            ")
    print("=========================================================================================")
    print(f"User Shopping Prompt : '{prompt}'")
    print("Starting automated query translation, shortlisting, verification, and checkout checks...\n")
    
    # -------------------------------------------------------------------------------------------
    # Step 1: Query Grounding (SIGE)
    # -------------------------------------------------------------------------------------------
    print("[1] Grounding Shopping Prompt via NLP Processor...")
    query_engine = QueryEngine()
    structured_query = query_engine.create_structured_query(prompt)
    
    print(f" -> Grounded GPC Category : {structured_query.gpc_category_code} (Pizzas/Ingredients)")
    print(f" -> Hard Constraints      : {json.dumps(structured_query.hard_constraints)}")
    print(f" -> Soft Preferences     : {json.dumps(structured_query.soft_preferences)}")
    print(" [✔] Prompt grounding completed successfully.\n")

    # -------------------------------------------------------------------------------------------
    # Step 2: Catalog Filtering (Shortlist Selection)
    # -------------------------------------------------------------------------------------------
    print("[2] Evaluating Candidate Ingredients from Global Merchant Catalog...")
    
    # Mock product catalog matching our dynamic GS1 & W3C structures
    mock_catalog = [
        {
            "sku": "GF-CRUST-001",
            "name": "Gluten-Free Organic Pizza Crust",
            "price": 6.99,
            "netContent": {"value": 14, "unitCode": "oz"},
            "allergens": ["None"],
            "claims": ["Organic", "Gluten-Free", "Vegetarian"],
            "vcs": [{
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", "ProductCertificationCredential"],
                "issuer": "did:key:z6MkpTHR8VNsBxR",
                "issuance_date": "2026-08-01T12:00:00Z",
                "credential_subject": {
                    "@id": "urn:product:GF-CRUST-001",
                    "certificationName": "Organic & GF Certificate",
                    "certificationStatus": "verified"
                },
                "proof": {
                    "type": "Ed25519Signature2020",
                    "created": "2026-08-01T12:05:00Z",
                    "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                    "jws": "fake_signature_for_crust"
                }
            }]
        },
        {
            "sku": "TOMATO-SAUCE-002",
            "name": "Organic Pizza Tomato Sauce",
            "price": 3.49,
            "netContent": {"value": 15, "unitCode": "oz"},
            "allergens": ["None"],
            "claims": ["Organic", "Vegetarian", "Gluten-Free"],
            "vcs": [{
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", "ProductCertificationCredential"],
                "issuer": "did:key:z6MkpTHR8VNsBxR",
                "issuance_date": "2026-08-01T12:00:00Z",
                "credential_subject": {
                    "@id": "urn:product:TOMATO-SAUCE-002",
                    "certificationName": "Organic Sauce Certificate",
                    "certificationStatus": "verified"
                },
                "proof": {
                    "type": "Ed25519Signature2020",
                    "created": "2026-08-01T12:05:00Z",
                    "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                    "jws": "fake_signature_for_sauce"
                }
            }]
        },
        {
            "sku": "MOZZARELLA-003",
            "name": "Vegetarian Mozzarella Cheese (Gluten-Free)",
            "price": 4.99,
            "netContent": {"value": 8, "unitCode": "oz"},
            "allergens": ["Milk"],
            "claims": ["Vegetarian", "Gluten-Free"],
            "vcs": [{
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", "ProductCertificationCredential"],
                "issuer": "did:key:z6MkpTHR8VNsBxR",
                "issuance_date": "2026-08-01T12:00:00Z",
                "credential_subject": {
                    "@id": "urn:product:MOZZARELLA-003",
                    "certificationName": "Vegetarian Dairy Certificate",
                    "certificationStatus": "verified"
                },
                "proof": {
                    "type": "Ed25519Signature2020",
                    "created": "2026-08-01T12:05:00Z",
                    "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                    "jws": "fake_signature_for_cheese"
                }
            }]
        },
        {
            "sku": "PEPPERONI-004",
            "name": "Spicy Meat Pepperoni Topping",
            "price": 5.49,
            "netContent": {"value": 6, "unitCode": "oz"},
            "allergens": ["Pork"],
            "claims": ["Pork"],
            "vcs": []  # No VC verification for vegetarian
        }
    ]

    selected_ingredients = []
    total_cost = 0.0
    all_claims_verified = True
    
    # NLP grounding mapped FREE_FROM:Gluten, Organic, Vegetarian
    required_allergens = structured_query.hard_constraints.get("gs1:allergenInformation", [])
    required_preferences = structured_query.soft_preferences

    from src.utils.state_emitter import StateEmitter
    validator = VerifiableCredentialValidator()
    emitter = StateEmitter()
    normalizer = UnitPriceNormalizer(emitter)

    for item in mock_catalog:
        print(f" -> Inspecting: '{item['name']}' (${item['price']})")
        
        # Filter Non-Vegetarian items (strict check against 'Vegetarian' request preference)
        if "Vegetarian" in required_preferences and "Vegetarian" not in item["claims"]:
            print(f"    [X] REJECTED: Not Vegetarian (Violates soft-preference boundary).")
            continue
            
        # Filter non-gluten-free items if Gluten-Free hard allergen constraint was grounded
        if "FREE_FROM:Gluten" in required_allergens and "Gluten-Free" not in item["claims"]:
            print(f"    [X] REJECTED: Contains Gluten (Hard constraint violation).")
            continue

        # -------------------------------------------------------------------------------------------
        # Step 3: W3C Cryptographic Claim Verification
        # -------------------------------------------------------------------------------------------
        claim_status = validator.validate_claims(item)
        if claim_status == 1:
            print("    [✔] W3C Signature Verified: Cryptographically authentic ecological & dietary claims.")
        elif claim_status == -1:
            print("    [X] REJECTED: Verifiable Credentials have been REVOKED.")
            all_claims_verified = False
            continue
        else:
            print("    [!] WARNING: Unverified or Missing Cryptographic claims.")
            all_claims_verified = False

        # -------------------------------------------------------------------------------------------
        # Step 4: SIGE Unit Price Normalization
        # -------------------------------------------------------------------------------------------
        normalized = normalizer.calculate_normalized_price(item)
        norm_str = f"${normalized['price']}/{normalized['unit']}" if normalized else "Unable to normalize"
        print(f"    [✔] Unit Normalized Price : {norm_str}")
        
        selected_ingredients.append(item)
        total_cost += item["price"]

    print(f"\n [✔] Shopping Shortlist Compiled successfully with {len(selected_ingredients)} verified vegetarian ingredients.")
    print("-----------------------------------------------------------------------------------------")
    for idx, item in enumerate(selected_ingredients):
        print(f" {idx + 1}. {item['name']} - ${item['price']}")
    print(f" -> TOTAL BASKET VALUE: ${total_cost:.2f}")
    print("-----------------------------------------------------------------------------------------\n")

    # -------------------------------------------------------------------------------------------
    # Step 5: Purchase Policy & Checkout Approvals (SPGE)
    # -------------------------------------------------------------------------------------------
    print("[5] Evaluating Cart Compliance against Organization Spending Policies...")
    approval_config = {
        'cost_threshold': 15.00,  # Auto-checkout threshold set to $15.00
        'min_claim_verification_score': 100.0,
        'unverified_domains': ['untrusted-merchant.com']
    }
    
    trigger = ApprovalTrigger(approval_config)
    requires_approval = trigger.should_trigger_approval(
        order_cost=total_cost,
        claim_verification_score=100.0 if all_claims_verified else 0.0,
        domain="organic-retail.com"
    )

    print("\n=========================================================================================")
    print("                                   FINAL TRANSACTION DECISION                            ")
    print("=========================================================================================")
    if requires_approval:
        print(" [🚨] HUMAN VISUAL STEP-UP APPROVAL TRIGGERED!")
        print(f"      Reason: Cart Total (${total_cost:.2f}) exceeds spend threshold (${approval_config['cost_threshold']:.2f}) or claims failed validation.")
        print("      Status: Cart suspended. Awaiting human visual sign-off via Dual-Surface portal.")
    else:
        print(" [✔] AUTO-CHECKOUT AUTHORIZED!")
        print("      Status: Transaction securely approved and routed to Payment Token issuer.")
    print("=========================================================================================\n")

if __name__ == "__main__":
    run_shopping_test()
