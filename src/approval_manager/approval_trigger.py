import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApprovalTrigger:
    """
    Manages the logic for triggering human visual approval based on various criteria.
    """
    def __init__(self, config: dict):
        """
        Initializes the ApprovalTrigger with configuration settings.

        Args:
            config (dict): A dictionary containing configuration parameters.
                           Expected keys:
                           - 'cost_threshold' (float): The maximum order cost before triggering approval.
                           - 'min_claim_verification_score' (float): The minimum claim verification score (e.g., 100.0 for 100%).
                           - 'unverified_domains' (list): A list of domain names considered unverified.
        """
        # Set default values if not provided in config
        self.cost_threshold = config.get('cost_threshold', 1000.0)  # Default to $1000 if not provided
        self.min_claim_verification_score = config.get('min_claim_verification_score', 100.0)
        self.unverified_domains = config.get('unverified_domains', [])
        logging.info(f"ApprovalTrigger initialized with cost_threshold={self.cost_threshold}, "
                     f"min_claim_verification_score={self.min_claim_verification_score}, "
                     f"unverified_domains={self.unverified_domains}")

    def should_trigger_approval(self, order_cost: float, claim_verification_score: float, domain: str) -> bool:
        """
        Determines if human visual approval should be triggered for a given order.

        Args:
            order_cost (float): The total cost of the order.
            claim_verification_score (float): The verification score of the claims made for the order.
            domain (str): The domain of the purchase.

        Returns:
            bool: True if human approval is required, False otherwise.
        """
        logging.info(f"Checking approval for order_cost={order_cost}, claim_score={claim_verification_score}, domain='{domain}'")

        # Trigger if order cost exceeds threshold
        if order_cost > self.cost_threshold:
            logging.warning(f"Approval triggered: Order cost ${order_cost} exceeds threshold ${self.cost_threshold}")
            return True

        # Trigger if claim verification score is below the minimum required
        if claim_verification_score < self.min_claim_verification_score:
            logging.warning(f"Approval triggered: Claim verification score {claim_verification_score} is below minimum {self.min_claim_verification_score}")
            return True

        # Trigger if the purchase is from an unverified domain
        if domain in self.unverified_domains:
            logging.warning(f"Approval triggered: Purchase from unverified domain '{domain}'")
            return True

        logging.info("No human approval required.")
        return False

# Example of how this might be used (can be removed or kept for demonstration)
if __name__ == "__main__":
    # Example configuration
    approval_config = {
        'cost_threshold': 500.0,
        'min_claim_verification_score': 95.0,
        'unverified_domains': ['malicious-store.com', 'phishing-site.net']
    }

    trigger = ApprovalTrigger(approval_config)

    # Test cases
    print("\n--- Test Cases ---")

    # Case 1: Order cost exceeds threshold
    cost1, score1, domain1 = 600.0, 100.0, "trusted-retailer.com"
    print(f"Test Case 1: Cost={cost1}, Score={score1}, Domain={domain1}")
    print(f"Requires Approval: {trigger.should_trigger_approval(cost1, score1, domain1)}") # Expected: True

    # Case 2: Claim verification score is low
    cost2, score2, domain2 = 400.0, 80.0, "trusted-retailer.com"
    print(f"\nTest Case 2: Cost={cost2}, Score={score2}, Domain={domain2}")
    print(f"Requires Approval: {trigger.should_trigger_approval(cost2, score2, domain2)}") # Expected: True

    # Case 3: Purchase from unverified domain
    cost3, score3, domain3 = 300.0, 100.0, "malicious-store.com"
    print(f"\nTest Case 3: Cost={cost3}, Score={score3}, Domain={domain3}")
    print(f"Requires Approval: {trigger.should_trigger_approval(cost3, score3, domain3)}") # Expected: True

    # Case 4: All conditions met, no approval needed
    cost4, score4, domain4 = 200.0, 98.0, "trusted-retailer.com"
    print(f"\nTest Case 4: Cost={cost4}, Score={score4}, Domain={domain4}")
    print(f"Requires Approval: {trigger.should_trigger_approval(cost4, score4, domain4)}") # Expected: False

    # Case 5: Using default configuration values
    print("\n--- Test Cases with Default Config ---")
    default_trigger = ApprovalTrigger({})
    cost5, score5, domain5 = 1500.0, 100.0, "some-domain.com"
    print(f"Test Case 5 (default): Cost={cost5}, Score={score5}, Domain={domain5}")
    print(f"Requires Approval: {default_trigger.should_trigger_approval(cost5, score5, domain5)}") # Expected: True (due to default cost threshold)
