import spacy
import subprocess
import sys

def load_spacy_model(model_name="en_core_web_sm"):
    try:
        spacy.load(model_name)
        print(f"spaCy model '{model_name}' loaded successfully.")
    except OSError:
        print(f"spaCy model '{model_name}' not found. Downloading...")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            print(f"spaCy model '{model_name}' downloaded and installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading spaCy model '{model_name}': {e}")
            raise
    return spacy.load(model_name)

# Load the spaCy model
nlp = load_spacy_model()

# Define your mapping from keywords to GS1 attributes and values
# This is a simplified example and would need to be expanded significantly
# based on the GS1 Web Vocabulary and common user requests.
GS1_MAPPING = {
    "organic": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM"}, # Example mapping
    "gluten-free": {"attribute": "gs1:allergenInformation", "value": "FREE_FROM"}, # Example mapping
    "protein": {"attribute": "gs1:nutritionalAttribute", "value": {"nutrient": "protein"}}, # Example mapping
    "fat": {"attribute": "gs1:nutritionalAttribute", "value": {"nutrient": "fat"}},
    "sugar": {"attribute": "gs1:nutritionalAttribute", "value": {"nutrient": "sugar"}},
    "calories": {"attribute": "gs1:nutritionalAttribute", "value": {"nutrient": "energy"}}, # Assuming 'energy' maps to calories
}

# Define GS1 attributes that expect specific values or structures
# This helps in structuring the output correctly.
GS1_ATTRIBUTE_STRUCTURES = {
    "gs1:allergenInformation": {"type": "enum", "enum_values": ["CONTAINED_IN", "FREE_FROM", "MAY_CONTAIN"]},
    "gs1:nutritionalAttribute": {"type": "object", "properties": {"nutrient": "string", "quantity": "number", "unit": "string"}},
    "gs1:netContent": {"type": "object", "properties": {"value": "number", "unit": "string"}},
}

class NLProcessor:
    def __init__(self):
        self.nlp = nlp
        self.gs1_mapping = GS1_MAPPING
        self.gs1_attribute_structures = GS1_ATTRIBUTE_STRUCTURES

    def parse_request(self, request_text: str) -> dict:
        """Parses natural language request into structured GS1 query constraints."""
        doc = self.nlp(request_text.lower())
        query_constraints = []

        # Basic keyword and entity matching for demonstration
        for token in doc:
            if token.text in self.gs1_mapping:
                mapping_info = self.gs1_mapping[token.text]
                attribute = mapping_info["attribute"]
                value = mapping_info["value"]
                
                constraint = {"attribute": attribute}

                # Basic validation and structuring based on expected GS1 attribute structures
                if attribute in self.gs1_attribute_structures:
                    structure = self.gs1_attribute_structures[attribute]
                    if structure["type"] == "enum":
                        if value in structure["enum_values"]:
                             constraint["value"] = value
                             query_constraints.append(constraint)
                    elif structure["type"] == "object":
                        # More complex object structuring would be needed here.
                        # For nutritional attributes, we'd need to extract quantity and unit.
                        # Example: "20g protein"
                        if attribute == "gs1:nutritionalAttribute":
                            # This is a placeholder - actual extraction would be more complex
                            # It would involve looking for quantity/unit tokens near the nutrient keyword.
                            extracted_quantity = None
                            extracted_unit = None
                            
                            # Example: Look for a number followed by a unit after the nutrient token
                            for i, t in enumerate(doc):
                                if t.text == token.text and i + 1 < len(doc):
                                    next_token = doc[i+1]
                                    if next_token.like_num:
                                        extracted_quantity = float(next_token.text)
                                        # Try to infer unit from next token or a known list
                                        if i + 2 < len(doc):
                                            potential_unit = doc[i+2].text
                                            if potential_unit in ["g", "kg", "ml", "l", "mg"]:
                                                extracted_unit = potential_unit
                                        elif next_token.nbor(1) and next_token.nbor(1).text in ["g", "kg", "ml", "l", "mg"]:
                                            extracted_unit = next_token.nbor(1).text

                                        break # Found quantity, stop searching for this nutrient

                            if extracted_quantity is not None and extracted_unit is not None:
                                constraint["value"] = {"nutrient": value["nutrient"], "quantity": extracted_quantity, "unit": extracted_unit}
                                query_constraints.append(constraint)
                            elif "quantity" in value: # If the mapping has a default quantity, use it (less ideal)
                                constraint["value"] = value
                                query_constraints.append(constraint)

                        elif attribute == "gs1:netContent":
                            # Placeholder for net content extraction (e.g., "1 liter", "500g")
                            # Similar logic to nutritional attributes would apply.
                            pass

                else:
                    # For attributes without a defined structure, add directly
                    constraint["value"] = value
                    query_constraints.append(constraint)

        # Log and return the structured query constraints
        print(f"Parsed request: '{request_text}' into constraints: {query_constraints}")
        return {
            "query_constraints": query_constraints,
            "original_request": request_text
        }

# Example Usage:
if __name__ == "__main__":
    processor = NLProcessor()
    
    request1 = "Find organic, gluten-free products with high protein"
    result1 = processor.parse_request(request1)
    print(f"Request: {request1}\nResult: {result1}\n")

    request2 = "Show me products with 20g of protein and 5g of fat"
    result2 = processor.parse_request(request2)
    print(f"Request: {request2}\nResult: {result2}\n")

    request3 = "I need a 1 liter bottle of water"
    # Note: 'water' is not in GS1_MAPPING, and '1 liter' needs netContent parsing.
    # This demonstrates current limitations.
    result3 = processor.parse_request(request3)
    print(f"Request: {request3}\nResult: {result3}\n")

    request4 = "Show me sugar-free options"
    result4 = processor.parse_request(request4)
    print(f"Request: {request4}\nResult: {result4}\n")
