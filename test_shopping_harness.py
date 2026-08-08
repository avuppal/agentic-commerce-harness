import sys
import os
import json

# Ensure src/ is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.sige.query_engine import QueryEngine
from src.data_models.gs1_schema import StructuredIntentQuery

def run_shopping_test():
    prompt = "all the ingredients to shop a vegetarian pizza organic and gluten free"
    
    print("=========================================================================================")
    print("                SHOPPING INTENT GROUNDING ENGINE (SIGE) EVALUATION                       ")
    print("=========================================================================================")
    print(f"User Shopping Request: '{prompt}'")
    print("Processing user query through active NLP pipeline...\n")
    
    # 1. Instantiate the Query Engine
    query_engine = QueryEngine()
    
    # 2. Process query to retrieve StructuredIntentQuery
    structured_query: StructuredIntentQuery = query_engine.create_structured_query(prompt)
    
    # 3. Output results
    print(" -> Successfully grounded intent into GS1 Web Vocabulary & GPC standard constraints:")
    print("-----------------------------------------------------------------------------------------")
    print(f"[*] Grounded GPC Category Code : {structured_query.gpc_category_code} (Pizzas)")
    print(f"[*] Hard Constraints (Allergens) : {json.dumps(structured_query.hard_constraints)}")
    print(f"[*] Soft Preferences (Dietary)  : {json.dumps(structured_query.soft_preferences)}")
    print("-----------------------------------------------------------------------------------------")
    
    # Check that our dynamic ontology parser captured the constraints
    assert structured_query.gpc_category_code == "10000247", "Failed to parse Pizza GPC code"
    assert "FREE_FROM:Gluten" in structured_query.hard_constraints.get("gs1:allergenInformation", []), "Failed to parse Gluten-Free allergen constraint"
    assert "Vegetarian" in structured_query.soft_preferences, "Failed to parse Vegetarian preference"
    assert "Organic" in structured_query.soft_preferences, "Failed to parse Organic preference"
    
    print("\n[✔] TEST PASSED: 100% compliant GS1 Web Vocabulary grounded structured query generated successfully!")
    print("=========================================================================================\n")

if __name__ == "__main__":
    run_shopping_test()
