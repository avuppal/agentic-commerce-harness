import os
import json
import logging

class Tokenizer:
    """
    Placeholder for a tokenizer that breaks text into lemma tokens.
    For simplicity, this version will just split words and convert to lowercase.
    A real implementation would involve more sophisticated NLP techniques.
    """
    def process(self, text: str) -> list[str]:
        # Basic tokenization: split by whitespace and convert to lowercase
        tokens = text.lower().split()
        return tokens

class SemanticVectorEmbedding:
    """
    Placeholder for a semantic vector embedding model.
    This class would typically use a pre-trained model to convert tokens or sentences
    into dense vector representations.
    """
    def embed(self, tokens: list[str]) -> list[float]:
        return [float(len(tokens) * 0.1)] * 10

class IntentClassifier:
    """
    Dynamic Intent Classifier mapping standard GS1 ontology/vocabularies from configuration files
    rather than hard-coding them in Python logic.
    """
    def __init__(self):
        # Default fallback vocabulary mapping
        self.vocabulary_map = {
            "categories": {
                "oat milk": "50160000",
                "milk substitute": "50160000",
                "strawberries": "50405020",
                "strawberry": "50405020",
                "cookie": "50130000",
                "cookies": "50130000"
            },
            "hard_constraints": {
                "gluten-free": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM:Gluten"},
                "gluten free": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM:Gluten"},
                "nut-free": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM:Nuts"},
                "nut free": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM:Nuts"},
                "sugar-free": {"attribute": "gs1:nutrientInformation", "value": "SUGAR_FREE"},
                "sugar free": {"attribute": "gs1:nutrientInformation", "value": "SUGAR_FREE"}
            },
            "soft_preferences": {
                "organic": "Organic",
                "local": "Local"
            }
        }
        
        # Load from config directory if present
        config_path = os.path.join(os.getcwd(), "config", "gs1_vocabulary_map.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    self.vocabulary_map = json.load(f)
                logging.info("Successfully loaded dynamic GS1 vocabulary mapping from config.")
            except Exception as e:
                logging.warning(f"Failed to load dynamic GS1 vocabulary map, using default. Error: {e}")

    def classify(self, query: str) -> dict:
        structured_intent = {
            "gs1:gpcCategoryCode": None,
            "hard_constraints": {},
            "soft_preferences": []
        }
        text_lower = query.lower()

        # 1. Dynamically match categories (GPC Brick Codes)
        for keyword, category_code in self.vocabulary_map.get("categories", {}).items():
            if keyword in text_lower:
                structured_intent["gs1:gpcCategoryCode"] = category_code
                break

        # 2. Dynamically match hard constraints (Allergens, Nutrients, Dietaries)
        for keyword, spec in self.vocabulary_map.get("hard_constraints", {}).items():
            if keyword in text_lower:
                attr = spec.get("attribute")
                val = spec.get("value")
                if attr and val:
                    if attr not in structured_intent["hard_constraints"]:
                        structured_intent["hard_constraints"][attr] = []
                    if val not in structured_intent["hard_constraints"][attr]:
                        structured_intent["hard_constraints"][attr].append(val)

        # 3. Dynamically match soft preferences (Claims, Origins, Brands)
        for keyword, preference in self.vocabulary_map.get("soft_preferences", {}).items():
            if keyword in text_lower:
                if preference not in structured_intent["soft_preferences"]:
                    structured_intent["soft_preferences"].append(preference)

        # Clean up empty lists/dicts if no constraints were found
        if not structured_intent["hard_constraints"]:
            structured_intent["hard_constraints"] = {}
        if not structured_intent["soft_preferences"]:
            structured_intent["soft_preferences"] = []
        
        # Ensure all keys exist as per schema, even if empty
        if "gs1:gpcCategoryCode" not in structured_intent:
             structured_intent["gs1:gpcCategoryCode"] = None
        if "hard_constraints" not in structured_intent:
            structured_intent["hard_constraints"] = {}
        if "soft_preferences" not in structured_intent:
            structured_intent["soft_preferences"] = []

        return structured_intent

def process_query(query: str) -> dict:
    """
    Full NLP pipeline to process a raw user query.
    Orchestrates Tokenization, Semantic Vector Embedding, and Intent Classification.
    """
    tokenizer = Tokenizer()
    embedder = SemanticVectorEmbedding()
    classifier = IntentClassifier()

    tokens = tokenizer.process(query)
    embedding = embedder.embed(tokens)
    intent = classifier.classify(query)

    return intent

class NLPProcessor:
    def process(self, query: str) -> dict:
        return process_query(query)
