import os

# Placeholder for UI rendering function, to be called by the orchestrator
# if human approval is triggered.
def trigger_human_approval(product_candidate: dict, spend_cap: float, domain_whitelist: list) -> bool:
    """
    Checks if a product candidate requires human approval based on cost, claims, and domain.
    
    Args:
        product_candidate (dict): A dictionary containing product details, including:
                                  'total_cost' (float),
                                  'claim_verification_score' (float, 0-100),
                                  'purchase_domain' (str).
        spend_cap (float): The maximum autonomous spending limit.
        domain_whitelist (list): A list of trusted merchant domains.
        
    Returns:
        bool: True if human approval is needed, False otherwise.
    """
    
    requires_approval = False
    
    # Check 1: Order Cost Threshold
    if product_candidate.get('total_cost', 0) > spend_cap:
        print(f"Approval required: Total cost ${product_candidate.get('total_cost')} exceeds spend cap ${spend_cap}.")
        requires_approval = True

    # Check 2: Claim Verification Score
    # Assuming score is 0-100. If missing, default to 0 to trigger approval.
    claim_score = product_candidate.get('claim_verification_score', 0)
    if claim_score < 100:
        print(f"Approval required: Claim verification score {claim_score} is below 100%")
        requires_approval = True

    # Check 3: Unverified Purchase Domains
    purchase_domain = product_candidate.get('purchase_domain')
    if purchase_domain not in domain_whitelist:
        print(f"Approval required: Purchase domain '{purchase_domain}' is not on the whitelist.")
        requires_approval = True
        
    return requires_approval


# Example of how this might be called (for illustrative purposes, not part of the function itself)
# if __name__ == "__main__":
#     # Mock data
#     product_to_check = {
#         'name': 'Organic Coffee Beans',
#         'total_cost': 150.00,
#         'claim_verification_score': 85.0,
#         'purchase_domain': 'new-organic-store.com',
#         # ... other potential fields for UI rendering like product_image_url, etc.
#     }
#     
#     autonomous_spend_limit = 100.00
#     trusted_domains = ['trusted-store.com', 'amazon.com']
#     
#     if trigger_human_approval(product_to_check, autonomous_spend_limit, trusted_domains):
#         print("Human approval is necessary. Initiating UI workflow...")
#         # In a real application, you would call a UI rendering function here
#         # e.g., ui_renderer.render_approval_ui(product_to_check, reasons_for_approval)
#     else:
#         print("Autonomous checkout can proceed.")
