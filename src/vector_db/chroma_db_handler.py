import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

class ChromaDBHandler:
    """Manages a persistent local ChromaDB vector database."""

    def __init__(self, persistence_directory: str = "./chroma_db_data", collection_name: str = "documents"):
        """
        Initializes the ChromaDB handler.

        Args:
            persistence_directory: The directory to store ChromaDB data persistently.
            collection_name: The name of the collection to use.
        """
        self.persistence_directory = persistence_directory
        self.collection_name = collection_name

        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=self.persistence_directory,
            settings=Settings()
        )

        # Get or create the collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        """
        Adds documents (text content, metadata, and unique IDs) to the collection.

        Args:
            documents: A list of text documents to add.
            metadatas: A list of dictionaries, where each dictionary contains metadata for a document.
            ids: A list of unique identifiers for each document.
        """
        if not (len(documents) == len(metadatas) == len(ids)):
            raise ValueError("The lengths of documents, metadatas, and ids must be the same.")

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Successfully added {len(ids)} documents to collection '{self.collection_name}'.")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            # Depending on requirements, you might want to re-raise or handle differently.
            raise

    def query_by_text(self, query_text: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Queries the collection using a text string.

        Args:
            query_text: The text to use for the query.
            n_results: The number of similar results to return.
            where: A dictionary for filtering results based on metadata.

        Returns:
            A list of dictionaries, where each dictionary represents a query result.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )
            
            # ChromaDB query returns nested structure. We want a flat list of results.
            # results structure: {'ids': [['id1', 'id2']], 'documents': [['doc1', 'doc2']], 'metadatas': [[{...}, {...}]]}
            if results and results.get('ids') and results['ids'][0]:
                formatted_results = []
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i]
                    })
                return formatted_results
            else:
                return []
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return []

    def count_documents(self) -> int:
        """
        Returns the total number of documents in the collection.
        """
        return self.collection.count()

    def delete_collection(self) -> None:
        """
        Deletes the entire collection.
        Use with caution!
        """
        try:
            self.client.delete_collection(name=self.collection_name)
            print(f"Collection '{self.collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting collection '{self.collection_name}': {e}")

# Example Usage (for testing purposes):
if __name__ == "__main__":
    # Initialize with a temporary directory for demonstration
    handler = ChromaDBHandler(persistence_directory="./temp_chroma_data_handler", collection_name="example_collection")

    # Add some documents
    documents_to_add = [
        "This is the first document about apples.",
        "This document is about bananas and other fruits.",
        "This is about oranges, a citrus fruit.",
        "Apples are a healthy snack."
    ]
    metadatas_to_add = [
        {"source": "doc1.txt", "category": "fruit"},
        {"source": "doc2.txt", "category": "fruit"},
        {"source": "doc3.txt", "category": "fruit"},
        {"source": "doc4.txt", "category": "fruit"}
    ]
    ids_to_add = [f"doc_{i+1}" for i in range(len(documents_to_add))]

    handler.add_documents(documents_to_add, metadatas_to_add, ids_to_add)

    print(f"Total documents in collection: {handler.count_documents()}")

    # Query for documents related to 'apples'
    query_results_apples = handler.query_by_text("apples")
    print("\nQuery results for 'apples':")
    for result in query_results_apples:
        print(result)

    # Query for documents related to 'citrus'
    query_results_citrus = handler.query_by_text("citrus fruit")
    print("\nQuery results for 'citrus fruit':")
    for result in query_results_citrus:
        print(result)

    # Query with metadata filter
    query_results_banana_fruit = handler.query_by_text("banana", where={"category": "fruit"})
    print("\nQuery results for 'banana' with category 'fruit':")
    for result in query_results_banana_fruit:
        print(result)

    # Clean up the temporary collection (optional)
    # handler.delete_collection()
    # print(f"Collection '{handler.collection_name}' deleted.")
