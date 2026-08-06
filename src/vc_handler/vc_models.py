# src/vc_handler/vc_models.py

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field

class Issuer(BaseModel):
    id: str = Field(..., alias="@id")
    type: Optional[Union[List[str], str]] = None
    name: Optional[str] = None

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

class Proof(BaseModel):
    type: str
    created: str
    proof_purpose: str = Field(..., alias="proofPurpose")
    verification_method: str = Field(..., alias="verificationMethod")
    proof_value: str = Field(..., alias="proofValue")

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

# Base model for a Verifiable Credential
class VerifiableCredential(BaseModel):
    context: Union[List[str], str] = Field(..., alias="@context")
    id: Optional[str] = Field(None, alias="id")
    type: List[str]
    issuer: Union[Issuer, str]
    issuance_date: str = Field(..., alias="issuanceDate")
    credential_subject: Dict[str, Any] = Field(..., alias="credentialSubject")
    proof: Proof
    expiration_date: Optional[str] = Field(None, alias="expirationDate")
    credential_status: Optional[Dict[str, Any]] = Field(None, alias="credentialStatus")

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

# Specific Credential Subjects based on PRD requirements

class EnvironmentalClaimSubject(BaseModel):
    type: str = "EnvironmentalClaim"
    carbon_footprint_kg_co2e: Optional[float] = Field(None, alias="carbonFootprintKgCO2e")
    recycled_content_percentage: Optional[float] = Field(None, alias="recycledContentPercentage")

    model_config = {
        "populate_by_name": True
    }

class SafetyClaimSubject(BaseModel):
    type: str = "SafetyClaim"
    is_non_toxic: Optional[bool] = Field(None, alias="isNonToxic")

    model_config = {
        "populate_by_name": True
    }

class DietaryClaimSubject(BaseModel):
    type: str = "DietaryClaim"
    is_gluten_free: Optional[bool] = Field(None, alias="isGlutenFree")
    is_vegan: Optional[bool] = Field(None, alias="isVegan")
    is_halal: Optional[bool] = Field(None, alias="isHalal")

    model_config = {
        "populate_by_name": True
    }

# Union of specific claim subjects that can be part of a Product Certification VC
ProductClaimSubject = Union[
    EnvironmentalClaimSubject,
    SafetyClaimSubject,
    DietaryClaimSubject,
    Dict[str, Any]
]

# A more specific VC model for Product Certifications
class ProductCertificationVC(VerifiableCredential):
    type: List[str] = ["VerifiableCredential", "ProductCertification"]
    credential_subject: ProductClaimSubject
