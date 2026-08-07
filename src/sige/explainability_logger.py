# src/sige/explainability_logger.py

import logging
from typing import List, Dict, Any

# It's good practice to create a dedicated logger for this specific functionality.
# This allows us to route XAI logs to a separate file or system if needed.
xai_logger = logging.getLogger('XAI_Logger')
# You can configure handlers and formatting in config/logging_config.py later.
if not xai_logger.handlers:
    xai_logger.addHandler(logging.StreamHandler())
    xai_logger.setLevel(logging.INFO)

class ExplainabilityLogger:
    """
    Generates and logs human-readable explanations for an agent's purchasing decisions,
    fulfilling the Post-Purchase Explainability (XAI) requirement from the PRD.
    """

    @staticmethod
    def log_decision(
        shortlisted_product: Dict[str, Any],
        rejected_products: List[Dict[str, Any]],
        reasons: Dict[str, str]
    ):
        """
        Logs the detailed reasoning for shortlisting one product and rejecting others.

        Args:
            shortlisted_product (Dict[str, Any]): The product data for the chosen item.
            rejected_products (List[Dict[str, Any]]): A list of products that were considered but rejected.
            reasons (Dict[str, str]): A dictionary mapping a product's '@id' to the reason for its acceptance or rejection.
        """
        shortlisted_id = shortlisted_product.get('@id', 'Unknown Product')
        shortlist_reason = reasons.get(shortlisted_id, "No specific reason provided.")

        # Construct the explanation based on the PRD's example format.
        explanation = f"Product {shortlisted_id} was shortlisted because {shortlist_reason}."

        for product in rejected_products:
            product_id = product.get('@id', 'Unknown Product')
            rejection_reason = reasons.get(product_id, "No specific reason provided.")
            explanation += f" Product {product_id} was rejected because {rejection_reason}."

        xai_logger.info(explanation)
        return explanation
