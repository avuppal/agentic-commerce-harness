import logging
from src.utils.db_handler import create_pending_approval

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApprovalTrigger:
    """
    Manages the logic for triggering human visual approval based on various criteria.
    """
    def __init__(self, config: dict):
        self.cost_threshold = config.get('cost_threshold', 1000.0)
        self.min_claim_verification_score = config.get('min_claim_verification_score', 100.0)
        self.unverified_domains = config.get('unverified_domains', [])
        logging.info(f"ApprovalTrigger initialized with cost_threshold={self.cost_threshold}, "
                     f"min_claim_verification_score={self.min_claim_verification_score}, "
                     f"unverified_domains={self.unverified_domains}")

    def should_trigger_approval(self, order_cost: float, claim_verification_score: float, domain: str, session_id: str = "default_session", cart_data: dict = None) -> bool:
        """
        Determines if human visual approval should be triggered for a given order.
        If required, persists the cart to PostgreSQL via db_handler.
        """
        logging.info(f"Checking approval for order_cost={order_cost}, claim_score={claim_verification_score}, domain='{domain}'")

        trigger_required = False

        if order_cost > self.cost_threshold:
            logging.warning(f"Approval triggered: Order cost ${order_cost} exceeds threshold ${self.cost_threshold}")
            trigger_required = True
        elif claim_verification_score < self.min_claim_verification_score:
            logging.warning(f"Approval triggered: Claim verification score {claim_verification_score} is below minimum {self.min_claim_verification_score}")
            trigger_required = True
        elif domain in self.unverified_domains:
            logging.warning(f"Approval triggered: Purchase from unverified domain '{domain}'")
            trigger_required = True

        if trigger_required:
            if cart_data is None:
                cart_data = {}
            # Persist to database queue
            try:
                order_id = create_pending_approval(session_id, cart_data, order_cost, claim_verification_score)
                logging.info(f"Cart suspended and queued for human approval. Database Order ID: {order_id}")
            except Exception as e:
                logging.error(f"Failed to queue pending approval: {e}")
            return True

        logging.info("No human approval required.")
        return False
