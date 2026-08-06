from decimal import Decimal

# Define default thresholds and scores
DEFAULT_ORDER_COST_THRESHOLD = Decimal('1000.00')
MINIMUM_CLAIM_VERIFICATION_SCORE = Decimal('100.00')

def requires_human_approval(order_cost: Decimal, claim_verification_score: Decimal, is_unverified_domain: bool) -> bool:
    """
    Determines if human approval is required based on order cost, claim verification score, or domain.

    Args:
        order_cost (Decimal): The total cost of the order.
        claim_verification_score (Decimal): The score representing the verification of claims (e.g., 0-100%).
        is_unverified_domain (bool): True if the purchase is from an unverified domain, False otherwise.

    Returns:
        bool: True if human approval is required, False otherwise.
    """
    if order_cost > DEFAULT_ORDER_COST_THRESHOLD:
        print(f"Approval required: Order cost ${order_cost} exceeds threshold of ${DEFAULT_ORDER_COST_THRESHOLD}")
        return True

    if claim_verification_score < MINIMUM_CLAIM_VERIFICATION_SCORE:
        print(f"Approval required: Claim verification score {claim_verification_score}% is below threshold of {MINIMUM_CLAIM_VERIFICATION_SCORE}%")
        return True

    if is_unverified_domain:
        print("Approval required: Purchase is from an unverified domain.")
        return True

    return False

