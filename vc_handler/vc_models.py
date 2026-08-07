# src/vc_handler/vc_models.py

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field

class Issuer(BaseModel):
    """
    Represents the 'issuer' of the Verifiable Credential.
    Can be a simple string (DID) or a complex object.
    """
    id: str = Field(..., alias="@id", description="The unique identifier of the issuer, typically a DID.")
    type: Optional[Union[List[str], str]] = Field(None, description="The type of the issuer.")
    name: Optional[str] = Field(None, description="The name of the issuer.")

    model_config = {
        "populate_by_name": True,
        "extra": "allow"  # Allow other fields as per the spec.
    }

class Proof(BaseModel):
    """
    Represents the cryptographic 'proof' attached to the Verifiable Credential.
    """
    type: str = Field(..., description="The type of the proof, e.g., 'Ed25519Signature2020'.")
    created: str = Field(..., description="ISO8601 timestamp of when the proof was created.")
    proof_purpose: str = Field(..., alias="proofPurpose", description="The purpose of the proof, e.g., 'assertionMethod'.")
    verification_method: str = Field(..., alias="verificationMethod", description="Identifier of the public key used for verification.")
    proof_value: str = Field(..., alias="proofValue", description="The digital signature value.")

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

class CredentialSubject(BaseModel):
    """
    Represents the 'credentialSubject' which contains the claims about the subject.
    This model is designed to be flexible, as claims can vary widely.
    """
    id: Optional[str] = Field(None, description="A unique identifier for the subject, often a DID.")
    
    model_config = {
        "extra": "allow"  # This is crucial to allow any arbitrary claims.
    }

class CredentialStatus(BaseModel):
    """
    Represents the 'credentialStatus' field, used for revocation checking.
    """
    id: str = Field(..., description="URL to the credential status information (e.g., a status list).")
    type: str = Field(..., description="The type of the status check method, e.g., 'StatusList2021'.")

    model_config = {
        "extra": "allow"
    }

class VerifiableCredential(BaseModel):
    """
    A Pydantic model for a W3C Verifiable Credential (VC).
    This model covers the core properties as defined in the W3C VC Data Model v1.1.
    """
    context: Union[List[str], str] = Field(..., alias="@context", description="The JSON-LD context(s) of the credential.")
    id: Optional[str] = Field(None, description="A unique URI for the credential.")
    type: List[str] = Field(..., description="A list of types, with 'VerifiableCredential' as the first entry.")
    issuer: Union[str, Issuer] = Field(..., description="The issuer of the credential, can be a DID string or an object.")
    issuance_date: str = Field(..., alias="issuanceDate", description="ISO8601 timestamp of when the credential was issued.")
    credential_subject: Union[CredentialSubject, Dict[str, Any]] = Field(..., alias="credentialSubject", description="The claims made about the subject.")
    proof: Proof = Field(..., description="The cryptographic proof associated with the credential.")
    credential_status: Optional[CredentialStatus] = Field(None, alias="credentialStatus", description="Information on how to check the credential's current status.")

    model_config = {
        "populate_by_name": True,
        "extra": "allow" # The VC data model allows for additional properties.
    }
