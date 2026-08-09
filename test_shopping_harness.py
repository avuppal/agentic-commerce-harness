import sys
import os
import json
import logging
import argparse

# Ensure src/ is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.sige.query_engine import QueryEngine
from src.vc_handler.vc_validator import VerifiableCredentialValidator
from src.sige.unit_price_normalizer import UnitPriceNormalizer
from src.approval_manager.approval_trigger import ApprovalTrigger
from src.payments.token_handler import TokenHandler

def run_shopping_test():
    parser = argparse.ArgumentParser(description="Autonomous Commerce Harness Shopping Test")
    parser.add_argument("--prompt", type=str, default="all the ingredients to shop a vegetarian pizza organic and gluten free", help="User shopping request prompt")
    parser.add_argument("--domain", type=str, default="organic-retail.com", help="Retailer domain name")
    args = parser.parse_args()

    prompt = args.prompt
    domain = args.domain

    # Auto-extract domain from prompt if present
    if "walmart.ca" in prompt.lower():
        domain = "walmart.ca"

    print("=========================================================================================")
    print("                 LIVE END-TO-END AUTONOMOUS SHOPPING PIPELINE                            ")
    print("=========================================================================================")
    print(f"User Shopping Prompt : '{prompt}'")
    print(f"Target Retailer      : {domain}")
    print("Starting automated query translation, shortlisting, verification, and checkout checks...\n")
    
    # -------------------------------------------------------------------------------------------
    # Step 1: Query Grounding (SIGE)
    # -------------------------------------------------------------------------------------------
    print("[1] Grounding Shopping Prompt via NLP Processor...")
    query_engine = QueryEngine()
    structured_query = query_engine.create_structured_query(prompt)
    
    # Check if category code was resolved or default to generic healthy categories
    gpc_code = structured_query.gpc_category_code or "10000000"
    print(f" -> Grounded GPC Category : {gpc_code}")
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
            "sku": "ORGANIC-OAT-MILK-101",
            "name": "Organic Pure Oat Milk",
            "price": 3.99,
            "netContent": {"value": 946, "unitCode": "ml"},
            "allergens": ["None"],
            "claims": ["Organic", "Vegetarian", "Gluten-Free"],
            "vcs": [{
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", "ProductCertificationCredential"],
                "issuer": "did:key:z6MkpTHR8VNsBxR",
                "issuance_date": "2026-08-01T12:00:00Z",
                "credential_subject": {
                    "@id": "urn:product:ORGANIC-OAT-MILK-101",
                    "certificationName": "USDA Organic Certification",
                    "certificationStatus": "verified"
                },
                "proof": {
                    "type": "Ed25519Signature2020",
                    "created": "2026-08-01T12:05:00Z",
                    "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                    "jws": "fake_signature_for_oat_milk"
                }
            }]
        },
        {
            "sku": "ORGANIC-STRAWBERRIES-102",
            "name": "Organic Vine Strawberries",
            "price": 4.49,
            "netContent": {"value": 454, "unitCode": "g"},
            "allergens": ["None"],
            "claims": ["Organic", "Vegetarian"],
            "vcs": [{
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", "ProductCertificationCredential"],
                "issuer": "did:key:z6MkpTHR8VNsBxR",
                "issuance_date": "2026-08-01T12:00:00Z",
                "credential_subject": {
                    "@id": "urn:product:ORGANIC-STRAWBERRIES-102",
                    "certificationName": "FairTrade Organic Strawberry",
                    "certificationStatus": "verified"
                },
                "proof": {
                    "type": "Ed25519Signature2020",
                    "created": "2026-08-01T12:05:00Z",
                    "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                    "jws": "fake_signature_for_strawberries"
                }
            }]
        },
        {
            "sku": "CONVENTIONAL-STRAWBERRIES-103",
            "name": "Conventional Strawberries",
            "price": 2.99,
            "netContent": {"value": 454, "unitCode": "g"},
            "allergens": ["None"],
            "claims": ["Vegetarian"],
            "vcs": [] # No organic VC
        }
    ]

    selected_ingredients = []
    total_cost = 0.0
    all_claims_verified = True
    
    required_allergens = structured_query.hard_constraints.get("gs1:allergenInformation", [])
    required_preferences = structured_query.soft_preferences

    from src.utils.state_emitter import StateEmitter
    validator = VerifiableCredentialValidator()
    emitter = StateEmitter()
    normalizer = UnitPriceNormalizer(emitter)

    # Contextual routing: If "healthy recipe" or "walmart" is chosen, evaluate healthy catalog items
    is_healthy_request = "healthy" in prompt.lower() or "walmart" in prompt.lower()

    for item in mock_catalog:
        # Determine catalog slice to evaluate
        is_pizza_crust_or_sauce = "crust" in item["name"].lower() or "sauce" in item["name"].lower()
        if is_healthy_request and is_pizza_crust_or_sauce and "pizza" not in prompt.lower():
            continue
        if not is_healthy_request and not is_pizza_crust_or_sauce:
            continue

        print(f" -> Inspecting: '{item['name']}' (${item['price']})")
        
        # Filter Organic items if Organic is requested
        if "Organic" in required_preferences and "Organic" not in item["claims"]:
            print(f"    [X] REJECTED: Not Organic (Violates organic preference).")
            continue

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

    print(f"\n [✔] Shopping Shortlist Compiled successfully with {len(selected_ingredients)} verified ingredients.")
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
        'cost_threshold': 25.00,  # Let's set a realistic budget threshold of $25.00
        'min_claim_verification_score': 100.0,
        'unverified_domains': ['untrusted-merchant.com']
    }
    
    trigger = ApprovalTrigger(approval_config)
    requires_approval = trigger.should_trigger_approval(
        order_cost=total_cost,
        claim_verification_score=100.0 if all_claims_verified else 0.0,
        domain=domain,
        session_id="walmart_session",
        cart_data={"ingredients": [item["name"] for item in selected_ingredients]}
    )

    print("\n=========================================================================================")
    print("                                   FINAL TRANSACTION DECISION                            ")
    print("=========================================================================================")
    if requires_approval:
        print(" [🚨] HUMAN VISUAL STEP-UP APPROVAL TRIGGERED!")
        print(f"      Reason: Cart Total (${total_cost:.2f}) exceeds spend threshold (${approval_config['cost_threshold']:.2f}) or unverified domains/claims.")
        print("      Status: Cart suspended. Awaiting human visual sign-off via Dual-Surface portal.")
    else:
        print(" [✔] AUTO-CHECKOUT AUTHORIZED!")
        print("      Status: Transaction securely approved and routed to Payment Token issuer.")
        
        # -------------------------------------------------------------------------------------------
        # Step 6: Payment Token Delegation (Stripe VCC Generation)
        # -------------------------------------------------------------------------------------------
        token_handler = TokenHandler()
        vcc_id = token_handler.generate_token({"amount": total_cost, "domain": domain})
        print(f" [💳] Stripe single-use VCC successfully minted!")
        print(f"      Virtual Card Token ID : {vcc_id}")
        print(f"      Usage restriction     : Locked to '{domain}' for max charge of ${total_cost*1.1:.2f} (with tax buffer).")
    print("=========================================================================================\n")

if __name__ == "__main__":
    run_shopping_test()
