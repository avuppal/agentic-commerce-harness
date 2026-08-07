# src/data_models/gs1_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional

class QuantitativeValue(BaseModel):
    """
    Represents a quantitative value with a unit, e.g., for gs1:netContent.
    Example: { "gs1:value": 1, "gs1:unitCode": "LTR" }
    """
    value: float = Field(..., alias="gs1:value")
    unit_code: str = Field(..., alias="gs1:unitCode")

class AllergenInfo(BaseModel):
    """
    Represents allergen information, specifying the type and level of containment.
    Example: { "gs1:allergenType": "Gluten", "gs1:levelOfContainment": "FREE_FROM" }
    """
    allergen_type: str = Field(..., alias="gs1:allergenType")
    level_of_containment: str = Field(..., alias="gs1:levelOfContainment") # e.g., "CONTAINS", "FREE_FROM"

class NutritionalAttribute(BaseModel):
    """
    Represents a single nutritional attribute.
    Example: { "gs1:nutrientType": "Fat", "gs1:quantity": "10g" }
    """
    nutrient_type: str = Field(..., alias="gs1:nutrientType")
    quantity: str = Field(..., alias="gs1:quantity")

class GS1Product(BaseModel):
    """
    A Pydantic model representing the core GS1 product data structure.
    This model enforces the mandatory fields required by the GS1FidelityChecker
    and the W3C Agentic Shopping Algorithm's filtering logic.
    """
    gtin: str = Field(..., alias="gs1:gtin", description="Global Trade Item Number.")
    gpc_category_code: str = Field(..., alias="gs1:gpcCategoryCode", description="Global Product Classification code.")
    net_content: List[QuantitativeValue] = Field(..., alias="gs1:netContent", description="The net content of the product.")
    allergen_information: List[AllergenInfo] = Field(..., alias="gs1:allergenInformation", description="List of allergens the product contains or is free from.")
    nutritional_attribute: Optional[List[NutritionalAttribute]] = Field(None, alias="gs1:nutritionalAttribute", description="Nutritional information for the product.")
    country_of_origin: str = Field(..., alias="gs1:countryOfOrigin", description="The country where the product was produced.")
    
    class Config:
        # Allows using field names (e.g., gtin) instead of aliases (gs1:gtin) for access
        allow_population_by_field_name = True
        # Ensures that aliases are used for serialization (when converting model to dict)
        by_alias = True
