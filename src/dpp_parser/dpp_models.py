from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Import VerifiableCredential from vc_handler
from src.vc_handler.vc_models import VerifiableCredential

# Import schema extensions
from src.data_models.schemaorg_extensions import UnitPriceSpecification, MerchantReputation


class RecycledContent(BaseModel):
    percentage: float
    material: str
    source: Optional[str] = None  # e.g., 'post-consumer', 'pre-consumer'


class BillOfMaterials(BaseModel):
    components: List[str]
    recycled_content: List[RecycledContent]


class CarbonFootprint(BaseModel):
    lifecycle_phase: str  # e.g., 'manufacturing', 'use', 'end-of-life'
    value_kg_co2e: float
    standard: Optional[str] = 'ISO 14067 / GHG Protocol'


class RepairabilityIndex(BaseModel):
    score: float  # Score from 1 to 10
    criteria: Optional[List[str]] = None


class CircularityInstructions(BaseModel):
    disassembly: Optional[str] = None
    recycling: Optional[str] = None
    reuse: Optional[str] = None
    repair: Optional[str] = None


class DigitalProductPassport(BaseModel):
    bill_of_materials: BillOfMaterials
    carbon_footprint: List[CarbonFootprint]
    repairability_index: RepairabilityIndex
    circularity_instructions: CircularityInstructions
    
    # Fields for W3C Agentic Shopping Algorithm
    certification_claims: List[VerifiableCredential]
    unit_pricing: UnitPriceSpecification
    merchant_reputation: MerchantReputation

    # Add other relevant DPP fields as needed, e.g., material composition, energy efficiency, etc.
    # For example:
    # material_composition: List[str]
    # energy_efficiency_rating: Optional[str] = None
