# src/sige/query_engine.py

"""
Orchestrates the SIGE (Semantic Intent Grounding Engine):
Takes user intent, calls nlp_processor to generate a structured query.

Based on PRD Requirements:
- REQ-SIGE-01: Convert ambiguous natural language requests into structured query constraints against GS1 master attributes.
"""

from src.data_models.gs1_schema import StructuredIntentQuery
from .nlp_processor import NLPProcessor

# Instantiate the NLP processor
nlp_processor = NLPProcessor()

class QueryEngine:
    def __init__(self):
        self.nlp_processor = NLPProcessor()

    def create_structured_query(self, user_intent: str) -> StructuredIntentQuery:
        """Orchestrates the SIGE module to generate a structured query.

        Args:
            user_intent: The natural language input from the user.

        Returns:
            A StructuredIntentQuery representing the structured query.
        """
        intent_dict = self.nlp_processor.process(user_intent)
        return StructuredIntentQuery(
            gpc_category_code=intent_dict.get("gs1:gpcCategoryCode"),
            hard_constraints=intent_dict.get("hard_constraints", {}),
            soft_preferences=intent_dict.get("soft_preferences", [])
        )

def create_structured_query(user_intent: str) -> dict:
    """Orchestrates the SIGE module to generate a structured query dictionary.

    Args:
        user_intent: The natural language input from the user.

    Returns:
        A dictionary representing the structured query.
    """
    engine = QueryEngine()
    return engine.create_structured_query(user_intent).model_dump(by_alias=True)
