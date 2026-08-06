from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Base model for JSON-LD context and type
class GS1BaseModel(BaseModel):
    class Config:
        # This is a placeholder, actual context and type might need to be more dynamic
        # or managed at a higher level depending on the application's JSON-LD strategy.
        json_schema_extra = {
            "@context": "http://gs1.org/voc/",
        }

    def model_dump_json(self, **kwargs) -> str:
        # Custom dump to include @type in the root if not already present, and handle context
        data = super().model_dump(by_alias=True, exclude_none=True)
        if "@type" in self.model_extra.get("json_schema_extra", {}):
            data["@type"] = self.model_extra["json_schema_extra"]["@type"]
        if "@context" in self.model_extra.get("json_schema_extra", {}):
            data["@context"] = self.model_extra["json_schema_extra"]["@context"]
        
        # Pydantic v2 way to get schema, might need adjustment for JSON-LD context management
        # For simplicity here, we're manually adding context and type to the dump.
        # A more robust solution might involve a custom encoder or a dedicated JSON-LD library.
        import json
        return json.dumps(data, **kwargs)

    def model_extra(self, *args, **kwargs):
        # Helper to access Config.json_schema_extra
        return self.Config.json_schema_extra


class Quantity(GS1BaseModel):
    value: float
    unit: str

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "Quantity",
            "@context": "http://gs1.org/voc/"
        }


class AllergenInfo(GS1BaseModel):
    allergen: str
    status: str # e.g., "CONTAINED_IN", "FREE_FROM", "MAY_CONTAIN"

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "AllergenInfo",
            "@context": "http://gs1.org/voc/"
        }


class NutritionalAttribute(GS1BaseModel):
    serving_size: Optional[str] = None
    calories: Optional[Quantity] = None
    protein: Optional[Quantity] = None
    fat: Optional[Quantity] = None
    carbohydrates: Optional[Quantity] = None
    # Add other common nutritional attributes as needed

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "NutritionalAttribute",
            "@context": "http://gs1.org/voc/"
        }


class Product(GS1BaseModel):
    gtin: str = Field(..., alias="gs1:gtin")
    gpcCategoryCode: str = Field(..., alias="gs1:gpcCategoryCode")
    netContent: Optional[Quantity] = Field(None, alias="gs1:netContent")
    allergenInformation: List[AllergenInfo] = Field([], alias="gs1:allergenInformation")
    nutritionalAttribute: Optional[NutritionalAttribute] = Field(None, alias="gs1:nutritionalAttribute")
    countryOfOrigin: Optional[str] = Field(None, alias="gs1:countryOfOrigin")
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "Product",
            # "@context" will be inherited from GS1BaseModel
        }


class Organization(GS1BaseModel):
    name: str
    gln: Optional[str] = Field(None, alias="gs1:gln") # Global Location Number
    # Add other relevant organization attributes like legal name, address etc.

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "Organization",
        }


class Place(GS1BaseModel):
    name: str
    address: Optional[str] = None
    # Add other relevant place attributes like geo-coordinates, type etc.

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "Place",
        }


class Offer(GS1BaseModel):
    price: float
    priceCurrency: str = Field(..., alias="gs1:priceCurrency")
    offeredBy: Optional[Organization] = Field(None, alias="gs1:offeredBy")
    seller: Optional[Organization] = Field(None, alias="gs1:seller") # Alias for offeredBy for broader compatibility
    includesObject: Optional[Product] = Field(None, alias="gs1:includesObject")
    # Add other relevant offer attributes like valid from/to, discounts etc.

    class Config(GS1BaseModel.Config):
        json_schema_extra = {
            "@type": "Offer",
        }


# Example of how to use the models (for testing/demonstration)
if __name__ == "__main__":
    # Example Product
    product_data = {
        "gs1:gtin": "01234567890123",
        "gs1:gpcCategoryCode": "10000042",
        "gs1:netContent": {"value": 500, "unit": "ml"},
        "gs1:allergenInformation": [
            {"allergen": "peanuts", "status": "CONTAINED_IN"},
            {"allergen": "gluten", "status": "FREE_FROM"}
        ],
        "gs1:nutritionalAttribute": {
            "serving_size": "100ml",
            "calories": {"value": 150, "unit": "kcal"},
            "protein": {"value": 10, "unit": "g"},
            "fat": {"value": 5, "unit": "g"}
        },
        "gs1:countryOfOrigin": "DE",
        "name": "Example Organic Juice",
        "brand": "Healthy Drinks Inc."
    }
    product = Product(**product_data)
    print("--- Product JSON ---")
    # Using custom dump_json for better JSON-LD compatibility
    print(product.model_dump_json(indent=2))

    # Example Offer
    seller_org = Organization(name="SuperMart", gln="0123456789012")
    offer_data = {
        "price": 2.50,
        "gs1:priceCurrency": "EUR",
        "gs1:offeredBy": seller_org,
        "gs1:includesObject": product
    }
    offer = Offer(**offer_data)
    print("\n--- Offer JSON ---")
    print(offer.model_dump_json(indent=2))
