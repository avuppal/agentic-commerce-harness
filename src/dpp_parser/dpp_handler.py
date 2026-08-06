import json

class DPPHandler:
    """Handles parsing of Digital Product Passport (DPP) JSON-LD payloads."""

    def __init__(self):
        self.bill_of_materials = None
        self.recycled_content = None
        self.carbon_footprint = None
        self.repairability_index = None
        self.circularity_instructions = None

    def parse_payload(self, payload: dict):
        """Parses a DPP JSON-LD payload and extracts relevant information.

        Args:
            payload (dict): The JSON-LD payload to parse.
        """
        if not isinstance(payload, dict):
            raise TypeError("Payload must be a dictionary.")

        # Extract Bill of Materials (BOM) and recycled content
        if 'dpp:billOfMaterials' in payload and isinstance(payload['dpp:billOfMaterials'], list):
            self.bill_of_materials = []
            for item in payload['dpp:billOfMaterials']:
                if isinstance(item, dict):
                    material_name = item.get('dpp:materialName')
                    recycled_percentage = item.get('dpp:recycledContentPercentage')
                    if material_name and recycled_percentage is not None:
                        self.bill_of_materials.append({
                            'materialName': material_name,
                            'recycledContentPercentage': recycled_percentage
                        })
            # If BOM is present, derive overall recycled content if possible or store it directly if provided
            # For now, we assume 'recycledContent' might be a top-level key or calculated from BOM
            if 'dpp:recycledContent' in payload and isinstance(payload['dpp:recycledContent'], (int, float)):
                self.recycled_content = payload['dpp:recycledContent']
            elif self.bill_of_materials: # Basic calculation if BOM is available
                total_recycled = sum(item['recycledContentPercentage'] for item in self.bill_of_materials if isinstance(item.get('recycledContentPercentage'), (int, float)))
                if total_recycled > 0:
                    self.recycled_content = total_recycled / len(self.bill_of_materials)

        # Extract Carbon Footprint
        if 'dpp:carbonFootprint' in payload and isinstance(payload['dpp:carbonFootprint'], dict):
            self.carbon_footprint = payload['dpp:carbonFootprint']

        # Extract Repairability Index
        if 'dpp:repairabilityIndex' in payload and isinstance(payload['dpp:repairabilityIndex'], (int, float)):
            self.repairability_index = payload['dpp:repairabilityIndex']

        # Extract Circularity Instructions
        if 'dpp:circularityInstructions' in payload and isinstance(payload['dpp:circularityInstructions'], str):
            self.circularity_instructions = payload['dpp:circularityInstructions']

    def get_bom(self) -> list | None:
        """Returns the Bill of Materials."""
        return self.bill_of_materials

    def get_recycled_content(self) -> float | None:
        """Returns the recycled content percentage."""
        return self.recycled_content

    def get_carbon_footprint(self) -> dict | None:
        """Returns the carbon footprint data."""
        return self.carbon_footprint

    def get_repairability_index(self) -> float | None:
        """Returns the repairability index."""
        return self.repairability_index

    def get_circularity_instructions(self) -> str | None:
        """Returns the circularity instructions."""
        return self.circularity_instructions

    def to_dict(self) -> dict:
        """Returns the parsed DPP data as a dictionary."""
        return {
            "bill_of_materials": self.bill_of_materials,
            "recycled_content": self.recycled_content,
            "carbon_footprint": self.carbon_footprint,
            "repairability_index": self.repairability_index,
            "circularity_instructions": self.circularity_instructions
        }

# Example usage (for testing purposes):
if __name__ == '__main__':
    # Example DPP JSON-LD payload based on the PRD and previous guidance
    example_payload = {
      "@context": "http://schema.org",
      "@type": "Product",
      "@id": "urn:uuid:YOUR_PRODUCT_UUID",
      "gs1:gtin": "YOUR_GTIN",
      "dpp:billOfMaterials": [
        {
          "dpp:materialName": "Recycled Plastic",
          "dpp:recycledContentPercentage": 75
        },
        {
          "dpp:materialName": "Aluminum",
          "dpp:recycledContentPercentage": 50
        }
      ],
      "dpp:carbonFootprint": {
        "dpp:cradleToGate": {
          "@type": "QuantitativeValue",
          "value": 5.5,
          "unitCode": "KG",
          "description": "kg CO2e per product unit"
        },
        "dpp:cradleToGrave": {
          "@type": "QuantitativeValue",
          "value": 7.0,
          "unitCode": "KG",
          "description": "kg CO2e per product unit"
        }
      },
      "dpp:repairabilityIndex": 8,
      "dpp:circularityInstructions": "Please disassemble and recycle all components according to local regulations. Refer to www.example.com/circularity for detailed instructions."
    }

    handler = DPPHandler()
    handler.parse_payload(example_payload)

    print("Parsed DPP Data:")
    print(f"  Bill of Materials: {handler.get_bom()}")
    print(f"  Recycled Content: {handler.get_recycled_content()}%")
    print(f"  Carbon Footprint: {handler.get_carbon_footprint()}")
    print(f"  Repairability Index: {handler.get_repairability_index()}")
    print(f"  Circularity Instructions: {handler.get_circularity_instructions()}")
    print(f"  To Dict: {handler.to_dict()}")

    # Example with missing fields
    incomplete_payload = {
      "@context": "http://schema.org",
      "@type": "Product",
      "gs1:gtin": "ANOTHER_GTIN",
      "dpp:repairabilityIndex": 5
    }
    print("\nParsing incomplete payload:")
    handler.parse_payload(incomplete_payload)
    print(f"  Bill of Materials: {handler.get_bom()}")
    print(f"  Recycled Content: {handler.get_recycled_content()}%")
    print(f"  Carbon Footprint: {handler.get_carbon_footprint()}")
    print(f"  Repairability Index: {handler.get_repairability_index()}")
    print(f"  Circularity Instructions: {handler.get_circularity_instructions()}")
    print(f"  To Dict: {handler.to_dict()}")
