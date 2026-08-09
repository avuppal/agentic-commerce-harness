import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import logging

# Configure logging for the script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Placeholder for ChromaDBHandler ---
# In a real application, this handler would be in a separate module (e.g., src/chroma_db_handler.py)
# and imported. For this script, we define a simplified version.
class ChromaDBHandler:
    def __init__(self, collection_name: str = "product_data", db_path: str = "./chroma_db"):
        """
        Initializes the ChromaDB handler.
        Args:
            collection_name (str): The name of the ChromaDB collection.
            db_path (str): The path to the persistent ChromaDB storage.
        """
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Ensure the directory exists
        os.makedirs(self.db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Get or create the collection
        try:
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            logging.info(f"ChromaDB collection '{self.collection_name}' ready at {self.db_path}.")
        except Exception as e:
            logging.error(f"Failed to get or create ChromaDB collection: {e}")
            raise

        # Initialize embedding model
        # Using a readily available model. Consider a more specialized one for production.
        # Model choice impacts embedding quality and performance.
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logging.info("SentenceTransformer model 'all-MiniLM-L6-v2' loaded.")
        except Exception as e:
            logging.error(f"Failed to load SentenceTransformer model: {e}")
            logging.error("Please ensure 'sentence-transformers' is installed and the model is accessible.")
            raise

    def add_products(self, products: List[Dict[str, Any]]):
        """
        Adds a list of product dictionaries to the ChromaDB collection.
        Embeds the product data and stores it along with metadata.
        Args:
            products (List[Dict[str, Any]]): A list of product dictionaries.
        """
        if not products:
            logging.warning("No products provided to add.")
            return

        documents_to_embed = []
        metadatas_to_store = []
        ids_to_store = []

        logging.info(f"Preparing {len(products)} products for embedding and storage.")
        
        for i, product in enumerate(products):
            # Create a unique ID for each product.
            # Prioritize GTIN if available, otherwise use a generated ID.
            product_id = str(product.get("gtin", f"generated_id_{i}")) # Ensure ID is a string
            ids_to_store.append(product_id)

            # Create a searchable document string.
            # Serializing the entire JSON-LD object is a common approach for rich embedding.
            # Alternatively, specific fields could be concatenated.
            try:
                document_text = json.dumps(product, ensure_ascii=False, indent=2)
                documents_to_embed.append(document_text)
            except TypeError as e:
                logging.warning(f"Could not serialize product {product_id} to JSON: {e}. Skipping this product's document text.")
                documents_to_embed.append("") # Append empty string to maintain list length

            # Store the original product dictionary as metadata for potential filtering/retrieval.
            metadatas_to_store.append(product)

        # Embed documents using the SentenceTransformer model
        try:
            logging.info("Embedding product documents...")
            embeddings = self.model.encode(documents_to_embed).tolist()
            logging.info("Embedding complete.")
        except Exception as e:
            logging.error(f"Error during embedding process: {e}")
            return

        # Add embeddings, documents, and metadata to ChromaDB collection
        try:
            # ChromaDB requires specific data structures for add operation
            self.collection.add(
                embeddings=embeddings,
                documents=documents_to_embed,
                metadatas=metadatas_to_store,
                ids=ids_to_store
            )
            logging.info(f"Successfully added {len(products)} products to ChromaDB collection '{self.collection_name}'.")
        except Exception as e:
            logging.error(f"Error adding products to ChromaDB: {e}")
            logging.error("Please check if IDs are unique and data formats are correct.")

import requests

def fetch_live_retailer_data() -> List[Dict[str, Any]]:
    """
    Queries a live simulated retailer API (FakeStore API) and translates its
    proprietary product schema into standard GS1 JSON-LD representations.
    """
    logging.info("Fetching live product data from retailer API...")
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        retailer_products = response.json()
    except Exception as e:
        logging.error(f"Failed to fetch live data from {url}: {e}")
        return []

    gs1_products = []
    for item in retailer_products:
        # Proprietary to GS1 Schema Translation
        gs1_product = {
            "@context": [
                "http://schema.org/",
                "https://www.gs1.org/voc/",
                {"@vocab": "http://schema.org/"}
            ],
            "@type": "Product",
            "gtin": f"00000000{item.get('id', 0):05d}", # Simulated GTIN
            "name": item.get('title', 'Unknown Product'),
            "description": item.get('description', ''),
            "brand": {"@type": "Organization", "name": "FakeStoreRetail"},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": str(item.get('price', '0.00')),
                "availability": "https://schema.org/InStock",
                "seller": {"@type": "Organization", "name": "FakeStore"}
            },
            "gpcCategoryCode": "10000000", # Generic GPC
            "netContent": {"@type": "QuantitativeValue", "value": 1, "unitCode": "EA"},
            "countryOfOrigin": "US"
        }
        gs1_products.append(gs1_product)
        
    logging.info(f"Successfully fetched and translated {len(gs1_products)} products to GS1 schema.")
    return gs1_products

# --- Data Generation Functions ---
def load_sample_product_data(num_samples: int = 100) -> List[Dict[str, Any]]:
    """
    Generates a list of sample GS1 JSON-LD product data.
    In a real application, this function would load data from files, a database, or an API.
    It uses simplified templates and variations to simulate diverse product profiles.
    
    Args:
        num_samples (int): The number of sample product profiles to generate.
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a product profile in JSON-LD format.
    """
    logging.info(f"Generating {num_samples} sample GS1 JSON-LD product profiles...")
    sample_data = []

    # Define base templates inspired by examples in the project context
    # These templates cover different product types and attribute structures.
    templates = [
        {
            "@context": [
                "http://schema.org/",
                "https://www.gs1.org/voc/",
                {"@vocab": "http://schema.org/"}
            ],
            "@type": "Product",
            "gtin": "00123456789012", # Example GTIN
            "name": "Example Widget",
            "description": "A high-quality widget for all your needs, built with precision.",
            "brand": {"@type": "Organization", "name": "Acme Corp"},
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": "19.99",
                "availability": "https://schema.org/InStock",
                "seller": {"@type": "Organization", "name": "Global Retail Solutions"}
            },
            "gpcCategoryCode": "10000001", # Example GPC code for 'Hardware'
            "netContent": {"@type": "QuantitativeValue", "value": 1, "unitCode": "PCE"}, # Piece
            "countryOfOrigin": "US",
            "nutritionalAttribute": [],
            "allergenInformation": []
        },
        {
            "@context": ["https://schema.org/", "https://www.gs1.org/voc/"],
            "@type": "Product",
            "gs1:gtin": "00987654321098", # Example GTIN
            "gs1:brandName": "OrganicHarvest",
            "gs1:description": "100% Organic Cold Pressed Almond Milk. Rich in Vitamin E. Verified Non-GMO.",
            "gs1:gpcCategoryCode": "50131700",  # Milk/Milk Substitutes
            "gs1:netContent": {"@type": "QuantitativeValue", "gs1:value": 946, "gs1:unitCode": "ml"}, # Milliliter
            "gs1:countryOfOrigin": "US",
            "gs1:allergenInformation": [{"@type": "AllergenInfo", "gs1:allergen": "Almonds", "gs1:allergenContains": "Free From"}]
        },
        {
            "@context": ["https://schema.org/", "https://www.gs1.org/voc/"],
            "@type": "Product",
            "gs1:gtin": "1122334455667", # Example GTIN
            "gs1:brandName": "EcoLiving",
            "gs1:description": "Sustainable Bamboo Toothbrush - Medium Bristle. Ergonomic design for comfortable grip.",
            "gs1:gpcCategoryCode": "46241200", # Personal Care Appliances -> Oral Care
            "gs1:netContent": {"@type": "QuantitativeValue", "gs1:value": 1, "gs1:unitCode": "PCE"}, # Piece
            "gs1:countryOfOrigin": "CN",
            "gs1:environmentalClaim": ["USDA Organic", "Biodegradable", "Recycled Packaging"]
        },
        {
            "@context": ["https://schema.org/", "https://www.gs1.org/voc/"],
            "@type": "Product",
            "gs1:gtin": "4455667788990",
            "gs1:brandName": "GourmetFoods",
            "gs1:description": "Artisan Dark Chocolate Bar with Sea Salt - 70% Cacao",
            "gs1:gpcCategoryCode": "40000000", # Food & Beverage
            "gs1:netContent": {"@type": "QuantitativeValue", "gs1:value": 100, "gs1:unitCode": "G"}, # Gram
            "gs1:countryOfOrigin": "CH",
            "gs1:nutritionalAttribute": [
                {"@type": "NutritionInformation", "gs1:servingSize": {"gs1:value": 30, "gs1:unitCode": "G"}},
                {"@type": "NutritionInformation", "gs1:calories": {"gs1:value": 150, "gs1:unitCode": "KCAL"}}
            ],
            "gs1:allergenInformation": [{"@type": "AllergenInfo", "gs1:allergen": "Milk", "gs1:allergenContains": "May Contain"}, {"@type": "AllergenInfo", "gs1:allergen": "Soy", "gs1:allergenContains": "May Contain"}]
        }
    ]

    for i in range(num_samples):
        # Cycle through templates and add variations to ensure diversity
        template_index = i % len(templates)
        new_product = templates[template_index].copy() # Deep copy might be safer if nested structures are modified heavily

        # Generate unique GTINs and update other fields to ensure uniqueness and variety
        unique_gtin_base = f"{i:012d}" # Generates 000...000 to 000...099 for 100 samples
        new_product["gtin"] = unique_gtin_base
        
        # Update other fields to make each entry more distinct
        if "@id" in new_product:
             new_product["@id"] = f"https://example.com/product/{unique_gtin_base}"
        
        if "gs1:gtin" in new_product:
            new_product["gs1:gtin"] = unique_gtin_base
        
        # Vary brand and product names slightly
        brand_suffix = f" Batch {i % 5}"
        if "gs1:brandName" in new_product:
            new_product["gs1:brandName"] = f"{new_product['gs1:brandName']}{brand_suffix}"
        if "name" in new_product:
            new_product["name"] = f"{new_product['name']} {brand_suffix}"
            
        # Vary description and price
        if "gs1:description" in new_product:
            new_product["gs1:description"] = f"{new_product['gs1:description']} - Batch {i}."
        if "name" in new_product and "description" not in new_product: # For widgets
            new_product["description"] = f"Enhanced description for {new_product['name']}."
            
        if "offers" in new_product and "price" in new_product["offers"]:
            # Vary price slightly around a base, e.g., add a small random amount or increment
            base_price = float(templates[template_index]["offers"]["price"])
            new_price = base_price + (i * 0.05) + (i % 3 * 0.1) # Small increments
            new_product["offers"]["price"] = f"{new_price:.2f}"
            
        # Ensure netContent value is also varied if relevant
        if "gs1:netContent" in new_product and "gs1:value" in new_product["gs1:netContent"]:
             if new_product["gtin"].endswith("000"): # Example: vary net content for specific GTINs
                 new_product["gs1:netContent"]["gs1:value"] = templates[template_index]["gs1:netContent"]["gs1:value"] + (i // 10)
             else:
                 new_product["gs1:netContent"]["gs1:value"] = templates[template_index]["gs1:netContent"]["gs1:value"]

        sample_data.append(new_product)
    
    logging.info(f"Generated {len(sample_data)} sample product profiles.")
    return sample_data

def main():
    """
    Main function to orchestrate the product data ingestion process.
    """
    logging.info("Starting product data ingestion script...")
    
    # Define ChromaDB configuration
    CHROMA_DB_PATH = "./chroma_product_db" # Directory to store ChromaDB files
    COLLECTION_NAME = "gs1_product_profiles" # Name of the collection for product data
    NUM_SAMPLES_TO_INGEST = 100 # Number of sample product profiles to generate and ingest
    
    # Initialize ChromaDBHandler
    try:
        handler = ChromaDBHandler(collection_name=COLLECTION_NAME, db_path=CHROMA_DB_PATH)
    except Exception as e:
        logging.error(f"Critical error: Could not initialize ChromaDBHandler. Exiting. Details: {e}")
        return

    # Load live product data
    product_data = fetch_live_retailer_data()
    
    # Fallback to generated samples if live fetch failed or returned empty
    if not product_data:
        logging.info("Falling back to simulated product data generation...")
        product_data = load_sample_product_data(num_samples=NUM_SAMPLES_TO_INGEST)
    
    if product_data:
        # Add products to ChromaDB
        handler.add_products(product_data)
    else:
        logging.warning("No product data was generated or loaded. Skipping ingestion.")

    logging.info("Product data ingestion script finished.")

if __name__ == "__main__":
    # Check for required libraries and provide installation instructions if missing.
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
        import json
        import os
    except ImportError as e:
        logging.error(f"Missing required library: {e}")
        logging.error("Please install the necessary libraries:")
        logging.error("pip install chromadb sentence-transformers")
        exit(1)
        
    main()
