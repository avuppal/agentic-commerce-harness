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
    Placeholder for an intent classifier.
    This class identifies the user's intent and extracts structured data
    like GPC category codes, hard constraints, and soft preferences.
    """
    def classify(self, query: str) -> dict:
        structured_intent = {
            "gs1:gpcCategoryCode": None,
            "hard_constraints": {},
            "soft_preferences": []
        }
        text_lower = query.lower()

        # Extract GPC Category Code (simplified keyword matching)
        if "oat milk" in text_lower or "milk substitute" in text_lower:
            structured_intent["gs1:gpcCategoryCode"] = "50160000" # GPC for Milk/Milk Substitutes
        elif "strawberries" in text_lower or "strawberry" in text_lower:
            structured_intent["gs1:gpcCategoryCode"] = "50405020" # GPC for Strawberries
        elif "cookie" in text_lower or "cookies" in text_lower:
            structured_intent["gs1:gpcCategoryCode"] = "50130000" # GPC for Biscuits/Cookies

        # Extract Hard Constraints (Allergens & Nutrients)
        if "gluten-free" in text_lower or "gluten free" in text_lower:
            if "gs1:allergenInformation" not in structured_intent["hard_constraints"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"] = []
            if "FREE_FROM:Gluten" not in structured_intent["hard_constraints"]["gs1:allergenInformation"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"].append("FREE_FROM:Gluten")

        if "nut-free" in text_lower or "nut free" in text_lower:
            if "gs1:allergenInformation" not in structured_intent["hard_constraints"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"] = []
            if "FREE_FROM:Nuts" not in structured_intent["hard_constraints"]["gs1:allergenInformation"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"].append("FREE_FROM:Nuts")

        if "sugar-free" in text_lower or "sugar free" in text_lower:
            if "gs1:nutrientInformation" not in structured_intent["hard_constraints"]:
                structured_intent["hard_constraints"]["gs1:nutrientInformation"] = []
            if "SUGAR_FREE" not in structured_intent["hard_constraints"]["gs1:nutrientInformation"]:
                structured_intent["hard_constraints"]["gs1:nutrientInformation"].append("SUGAR_FREE")

        # Extract Soft Preferences (Claims & Locations)
        if "organic" in text_lower:
            if "Organic" not in structured_intent["soft_preferences"]:
                structured_intent["soft_preferences"].append("Organic")
        if "local" in text_lower:
            if "Local" not in structured_intent["soft_preferences"]:
                structured_intent["soft_preferences"].append("Local")

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
