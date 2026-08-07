import time
from typing import List, Dict, Any

# It's crucial to use the same embedding model as the NLP processor.
# We can assume it will be injected upon initialization.
# from sige.nlp_processor import SemanticVectorEmbedding # Hypothetical import

# Placeholder for a real Vector DB client
class VectorDatabaseClient:
    def add_vector(self, shopper_id: str, vector: List[float], metadata: Dict):
        print(f"Adding vector for {shopper_id} with metadata {metadata}")
        pass

    def query_vector(self, shopper_id: str, query_vector: List[float], top_k: int) -> List[Dict]:
        print(f"Querying similar purchases for {shopper_id}")
        return []

class ShopperHistoryManager:
    """Manages shopper purchase history using a vector database."""

    def __init__(self, vector_db_client: VectorDatabaseClient, embedding_model: Any):
        """
        Initializes the manager with a vector database client and a semantic embedding model.
        
        Args:
            vector_db_client: Client for interacting with the vector DB.
            embedding_model: The semantic embedding model (shared with NLPProcessor).
        """
        self.vector_db_client = vector_db_client
        self.embedding_model = embedding_model

    def add_purchase(self, shopper_id: str, purchase_event: Dict[str, Any]):
        """
        Adds a purchase event to the shopper's history.

        Args:
            shopper_id: The unique identifier for the shopper.
            purchase_event: A dictionary containing purchase details like
                            'product_name', 'category', 'price', 'quantity'.
        """
        purchase_vector = self._create_purchase_vector(purchase_event)
        
        metadata = {
            "product_name": purchase_event.get("product_name"),
            "timestamp": time.time(),
            "price": purchase_event.get("price"),
            "quantity": purchase_event.get("quantity")
        }
        
        self.vector_db_client.add_vector(shopper_id, purchase_vector, metadata)

    def _create_purchase_vector(self, purchase_event: Dict[str, Any]) -> List[float]:
        """
        Creates a hybrid vector representing a purchase event.

        The vector combines a semantic representation of the product with
        normalized transactional data.
        """
        # 1. Generate semantic vector from product text.
        # Concatenating key fields gives the model rich context.
        product_text = (
            f"{purchase_event.get('product_name', '')} "
            f"category: {purchase_event.get('category', '')} "
            f"attributes: {','.join(purchase_event.get('attributes', []))}"
        )
        # The embedding_model should have an 'embed' or similar method.
        semantic_vector = self.embedding_model.embed(product_text)

        # 2. Normalize transactional features to a consistent scale (e.g., 0 to 1).
        # This prevents features with large ranges from dominating the vector distance.
        normalized_price = self._normalize_feature(purchase_event.get('price', 0.0), max_val=200.0) # Assume max price
        normalized_quantity = self._normalize_feature(purchase_event.get('quantity', 1), max_val=50.0) # Assume max quantity

        # 3. Combine into a single hybrid vector.
        purchase_vector = semantic_vector + [normalized_price, normalized_quantity]
        
        return purchase_vector

    def _normalize_feature(self, value: float, max_val: float) -> float:
        """A simple min-max scaling to a [0, 1] range."""
        if max_val == 0:
            return 0.0
        # Ensure value doesn't exceed 1.0
        return min(value / max_val, 1.0)

    def find_similar_purchases(self, shopper_id: str, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Queries the vector database for past purchases similar to the query vector.
        """
        return self.vector_db_client.query_vector(shopper_id, query_vector, top_k)
