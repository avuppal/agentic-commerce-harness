import unittest
from src.sige.query_engine import QueryEngine
from src.data_models.gs1_schema import StructuredIntentQuery

class TestIntentMatchingAccuracy(unittest.TestCase):
    def setUp(self):
        """
        Initialize the QueryEngine which handles the NLP processing.
        """
        self.query_engine = QueryEngine()

    def test_prompt_with_multiple_constraints(self):
        """
        Tests a prompt from the PRD with both dietary and allergen constraints.
        Verifies that "sugar-free gluten-free oat milk" is correctly translated
        into a structured query with the appropriate hard constraints.
        """
        prompt = "sugar-free gluten-free oat milk"
        
        # The QueryEngine processes the prompt and returns a structured query object.
        structured_query: StructuredIntentQuery = self.query_engine.create_structured_query(prompt)
        
        # Define the expected output structure
        expected_gpc_code = "50160000"  # GS1 GPC for Milk & Cream (and substitutes)
        expected_hard_constraints = {
            "gs1:allergenInformation": ["FREE_FROM:Gluten"],
            "gs1:nutrientInformation": ["SUGAR_FREE"]
        }
        
        # Assert that the structured query matches the expected output
        self.assertEqual(structured_query.gpc_category_code, expected_gpc_code)
        self.assertDictEqual(structured_query.hard_constraints, expected_hard_constraints)
        self.assertEqual(len(structured_query.soft_preferences), 0)

    def test_prompt_with_soft_preference(self):
        """
        Tests a prompt that includes a soft preference (e.g., a brand or certification).
        """
        prompt = "local organic strawberries"

        structured_query: StructuredIntentQuery = self.query_engine.create_structured_query(prompt)

        expected_gpc_code = "50405020" # GS1 GPC for Strawberries
        expected_soft_preferences = ["Organic", "Local"]

        self.assertEqual(structured_query.gpc_category_code, expected_gpc_code)
        self.assertEqual(len(structured_query.hard_constraints), 0)
        # Using assertCountEqual to ignore order of preferences
        self.assertCountEqual(structured_query.soft_preferences, expected_soft_preferences)

    def test_nut_free_cookie_allergen_constraint(self):
        """
        Tests that a prompt for "nut-free cookies" correctly maps to the
        gs1:allergenInformation hard constraint via the QueryEngine.
        """
        prompt = "nut-free cookies"
        
        # The QueryEngine processes the prompt and returns a structured query object.
        structured_query: StructuredIntentQuery = self.query_engine.create_structured_query(prompt)
        
        # Define the expected output structure
        expected_gpc_code = "50130000"  # GS1 GPC for Biscuits/Cookies (Sweet)
        expected_hard_constraints = {
            "gs1:allergenInformation": ["FREE_FROM:Nuts"]
        }
        
        # Assert that the structured query matches the expected output
        self.assertEqual(structured_query.gpc_category_code, expected_gpc_code)
        self.assertDictEqual(structured_query.hard_constraints, expected_hard_constraints)
        self.assertEqual(len(structured_query.soft_preferences), 0)


if __name__ == '__main__':
    unittest.main()
