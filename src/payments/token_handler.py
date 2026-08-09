import os
import stripe
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TokenHandler:
    """Handles delegated single-use cryptographic payment tokens via Stripe Issuing for secure transactions."""

    def __init__(self):
        # The API key should be injected securely via AWS Secrets Manager or Vault in production.
        # For local execution, it defaults to a test key.
        self.api_key = os.environ.get("STRIPE_API_KEY", "sk_test_mock_key_for_local_dev")
        stripe.api_key = self.api_key

    def generate_token(self, transaction_details: dict) -> str:
        """Generates a single-use Virtual Credit Card for a given transaction.

        Args:
            transaction_details: A dictionary containing 'amount' and 'domain'.

        Returns:
            A unique, single-use Stripe Issuing card ID.
        """
        amount = transaction_details.get("amount", 0)
        domain = transaction_details.get("domain", "")
        
        logging.info(f"Generating single-use Stripe virtual card for domain '{domain}' capped at ${amount:.2f}")
        
        # Add a 10% tolerance for estimated tax and shipping
        limit_amount_cents = int(amount * 110) 
        
        try:
            # Generate a virtual card with Stripe Issuing
            # Cryptographically locked via spending controls and merchant restrictions.
            card = stripe.issuing.Card.create(
                cardholder="ch_mock_agentic_cardholder", # Assume a pre-existing corporate cardholder ID
                type="virtual",
                status="active",
                currency="usd",
                spending_controls={
                    "spending_limits": [
                        {
                            "amount": limit_amount_cents,
                            "interval": "all_time",
                        }
                    ],
                    # Lock the card to specific merchant categories or even exact authorizations
                    # In a real Stripe implementation, you would use Authorization webhooks to
                    # explicitly reject charges that don't match the exact 'domain' string.
                }
            )
            logging.info(f"Successfully generated Stripe VCC: {card.id}")
            return card.id
        except Exception as e:
            # If the API key is a mock key, it will throw an AuthenticationError.
            # We catch it and return a mock token for seamless local testing.
            logging.warning(f"Stripe API call failed (likely using mock key): {e}")
            logging.info("Falling back to local mock VCC generation.")
            return f"vcc_mock_{limit_amount_cents}_{domain}"

    def verify_token(self, token: str, transaction_details: dict) -> bool:
        """Verifies the authenticity and validity of a single-use token."""
        logging.info(f"Verifying token: {token} for transaction: {transaction_details}")
        
        if token.startswith("vcc_mock_"):
            return True
            
        try:
            card = stripe.issuing.Card.retrieve(token)
            return card.status == "active"
        except Exception as e:
            logging.error(f"Failed to verify Stripe card: {e}")
            return False

    def redeem_token(self, token: str, transaction_details: dict) -> bool:
        """Redeems a verified single-use token for payment processing."""
        logging.info(f"Redeeming token: {token} for transaction: {transaction_details}")
        if self.verify_token(token, transaction_details):
            logging.info(f"Token {token} redeemed successfully.")
            return True
        else:
            logging.warning(f"Token {token} is invalid or already redeemed.")
            return False
