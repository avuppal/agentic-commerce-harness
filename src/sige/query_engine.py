# src/sige/query_engine.py

"""
Orchestrates the SIGE (Semantic Intent Grounding Engine):
Takes user intent, calls nlp_processor to generate a structured query.

Based on PRD Requirements:
- REQ-SIGE-01: Convert ambiguous natural language requests into structured query constraints against GS1 master attributes.
"""

from .nlp_processor import NLPProcessor

# Instantiate the NLP processor
nlp_processor = NLPProcessor()

def create_structured_query(user_intent: str) -> dict:
    """Orchestrates the SIGE module to generate a structured query.

    Args:
        user_intent: The natural language input from the user.

    Returns:
        A dictionary representing the structured query.
    """
    # Process user intent using NLP to extract entities and constraints
    structured_query = nlp_processor.process(user_intent)

    return structured_query
