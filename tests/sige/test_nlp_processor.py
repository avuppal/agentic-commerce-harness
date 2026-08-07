# tests/sige/test_nlp_processor.py
import pytest
from src.sige.nlp_processor import process_query

def test_process_query_organic_oat_milk():
    """
    Tests the full NLP pipeline for a specific query: "Organic gluten-free oat milk".
    It verifies that the query is correctly classified into GPC code, hard constraints, and soft preferences.
    """
    query = "Organic gluten-free oat milk"
    
    expected_intent = {
        "gs1:gpcCategoryCode": "50160000",
        "hard_constraints": {
            "gs1:allergenInformation": ["FREE_FROM:Gluten"]
        },
        "soft_preferences": ["Organic"]
    }
    
    actual_intent = process_query(query)
    
    assert actual_intent == expected_intent
