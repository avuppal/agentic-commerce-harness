from typing import List, Optional
from pydantic import BaseModel, Field

class Material(BaseModel):
    """
    Represents a single material within the Bill of Materials (BOM) of a product.
    """
    materialName: str = Field(
        ...,
        description="The common name of the material.",
        examples=["Recycled PET", "Organic Cotton"]
    )
    recycledContentPercentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="The percentage of the material that is from recycled sources."
    )

class CarbonFootprint(BaseModel):
    """
    Represents the carbon footprint of the product.
    """
    value: float = Field(
        ...,
        description="The numerical value of the carbon footprint."
    )
    unit: str = Field(
        default="kgCO2e",
        description="The unit of measurement for the carbon footprint, typically kilograms of CO2 equivalent."
    )

class Repairability(BaseModel):
    """
    Represents the repairability index of a product.
    """
    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="The repairability score, often on a scale of 0 to 10."
    )

class DPP(BaseModel):
    """
    The main Digital Product Passport (DPP) model, aggregating all relevant sustainability
    and circularity data extracted from a JSON-LD payload.
    """
    billOfMaterials: Optional[List[Material]] = Field(
        None,
        description="A list of materials and their recycled content percentages."
    )
    carbonFootprint: Optional[CarbonFootprint] = Field(
        None,
        description="The product's carbon footprint."
    )
    repairabilityIndex: Optional[Repairability] = Field(
        None,
        description="An index or score indicating the ease of repair for the product."
    )
    circularityInstructions: Optional[str] = Field(
        None,
        description="Human-readable instructions for disassembly, reuse, or recycling."
    )
