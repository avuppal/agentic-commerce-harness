class Tokenizer:
    """
    Placeholder for a tokenizer that breaks text into lemma tokens.
    For simplicity, this version will just split words and convert to lowercase.
    A real implementation would involve more sophisticated NLP techniques.
    """
    def process(self, text: str) -> list[str]:
        # Basic tokenization: split by whitespace and convert to lowercase
        tokens = text.lower().split()
        # In a real scenario, lemmatization would happen here.
        # For now, we return the split words as tokens.
        return tokens

class SemanticVectorEmbedding:
    """
    Placeholder for a semantic vector embedding model.
    This class would typically use a pre-trained model (e.g., Word2Vec, GloVe, Sentence-BERT)
    to convert tokens or sentences into dense vector representations.
    """
    def embed(self, tokens: list[str]) -> list[float]:
        # In a real implementation, this would return a numerical vector.
        # For this placeholder, we can return a dummy list or raise NotImplementedError.
        # For now, returning a dummy based on token count.
        return [float(len(tokens) * 0.1)] * 10 # Dummy embedding of size 10

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

        # Extract Hard Constraints (Allergens)
        if "gluten-free" in text_lower:
            if "gs1:allergenInformation" not in structured_intent["hard_constraints"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"] = []
            # Ensure it's a list before appending if the key already exists with a non-list value
            if not isinstance(structured_intent["hard_constraints"]["gs1:allergenInformation"], list):
                 structured_intent["hard_constraints"]["gs1:allergenInformation"] = []
            if "FREE_FROM:Gluten" not in structured_intent["hard_constraints"]["gs1:allergenInformation"]:
                structured_intent["hard_constraints"]["gs1:allergenInformation"].append("FREE_FROM:Gluten")

        # Extract Soft Preferences (Claims)
        if "organic" in text_lower:
            if "Organic" not in structured_intent["soft_preferences"]:
                structured_intent["soft_preferences"].append("Organic")

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

    # Stage 1: Tokenization
    tokens = tokenizer.process(query)

    # Stage 2: Semantic Vector Embedding
    # The embedding is not directly used by the current placeholder classifier
    # but is part of the pipeline as per the PRD.
    embedding = embedder.embed(tokens)

    # Stage 3: Intent Classification
    # The placeholder classifier uses the raw query text for simplicity.
    # In a real implementation, it would leverage the 'embedding'.
    intent = classifier.classify(query)

    # The final output should align with the structure expected by downstream systems.
    # Ensure the output matches the expected schema, including the case where no
    # constraints are found.
    
    # The `IntentClassifier.classify` method already handles ensuring all keys exist.
    # We just need to return its result.
    return intent
