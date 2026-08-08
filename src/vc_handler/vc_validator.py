# src/vc_handler/vc_validator.py

import logging
from typing import Dict, Any, Optional
from src.vc_handler.vc_models import VerifiableCredential

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VerifiableCredentialValidator:
    """
    Implements verification logic for W3C Verifiable Credentials.
    Supports signature verification, issuer DID checking, and StatusList2021 revocation checks.
    """

    def __init__(self, trusted_did_issuers: Optional[list] = None):
        """
        Initializes the validator with an optional list of trusted issuer DIDs.
        """
        self.trusted_did_issuers = trusted_did_issuers or ["did:key:z6MkpTHR8VNsBxR", "did:web:certification-body.org"]

    def resolve_did_document(self, did: str) -> Dict[str, Any]:
        """
        Simulates resolving a DID Document to get the public key for signature validation.
        """
        logging.info(f"Resolving DID Document for issuer: {did}")
        # Return mock public key info
        return {
            "id": f"{did}#key-1",
            "type": "Ed25519VerificationKey2020",
            "controller": did,
            "publicKeyMultibase": "z6MkmLgYvW5vE99zD"
        }

    def verify_cryptographic_signature(self, credential: VerifiableCredential, public_key_info: Dict[str, Any]) -> bool:
        """
        Simulates cryptographic signature verification (Ed25519Signature2020 / ECDSA).
        """
        proof = credential.proof
        logging.info(f"Verifying signature with method {proof.verification_method} using type {proof.type}")
        # In a production environment, we would use a library like jwcrypto or cryptography.
        # For the prototype, we verify that the proof has a signature value.
        sig = proof.proof_value or proof.jws
        if sig and len(sig) > 10:
            logging.info("Cryptographic signature verified successfully.")
            return True
        logging.warning("Cryptographic signature verification failed: invalid or empty proof value.")
        return False

    def check_status_list_revocation(self, credential: VerifiableCredential) -> bool:
        """
        Simulates checking StatusList2021 for VC revocation.
        """
        if credential.credential_status:
            status_id = credential.credential_status.get("id")
            status_type = credential.credential_status.get("type")
            status_list_index = credential.credential_status.get("statusListIndex")
            logging.info(f"Checking StatusList2021: {status_id} at index {status_list_index} (Type: {status_type})")
            
            # Simulate a simple revocation check rule (e.g. index 99 is revoked for testing)
            if status_list_index == 99:
                logging.warning(f"Credential has been REVOKED at index {status_list_index}.")
                return False
        logging.info("Credential status check: ACTIVE.")
        return True

    def validate(self, credential_data: Dict[str, Any]) -> str:
        """
        Executes the agent verification workflow as defined in the PRD Section 3.3.
        
        Workflow:
        1. Parse into VerifiableCredential model
        2. Extract Claim Issuer DID
        3. Verify Cryptographic Signature against DID Document
        4. Check StatusList2021 Revocation
        5. Return CLAIM_VERIFIED or CLAIM_REJECTED / CLAIM_REVOKED
        """
        try:
            # 1. Parse and validate structure
            credential = VerifiableCredential(**credential_data)
            logging.info(f"Validating VC ID: {credential.id}")

            # 2. Extract Claim Issuer DID
            if isinstance(credential.issuer, str):
                issuer_did = credential.issuer
            else:
                issuer_did = credential.issuer.id

            if not issuer_did or not issuer_did.startswith("did:"):
                logging.warning(f"Rejecting credential: Issuer ID {issuer_did} is not a valid DID.")
                return "CLAIM_REJECTED"

            # 3. Resolve DID Document and Verify Signature
            pub_key = self.resolve_did_document(issuer_did)
            if not self.verify_cryptographic_signature(credential, pub_key):
                return "CLAIM_REJECTED"

            # 4. Check StatusList2021 Revocation status
            if not self.check_status_list_revocation(credential):
                return "CLAIM_REVOKED"

            # 5. Return success signal
            logging.info(f"Verifiable Credential {credential.id} successfully validated.")
            return "CLAIM_VERIFIED"

        except Exception as e:
            logging.error(f"Error validating Verifiable Credential: {e}")
            return "CLAIM_REJECTED"

    def validate_claims(self, product_data: Dict[str, Any]) -> int:
        """
        Validates claims inside a product payload based on attached Verifiable Credentials.
        Returns:
            1 (CLAIM_VERIFIED) if at least one VC is attached and all attached VCs are valid.
            0 (CLAIM_REJECTED) if no VCs are attached or if any VC is rejected.
            -1 (CLAIM_REVOKED) if any attached VC has been revoked.
        """
        vcs = product_data.get("vcs")
        if not vcs or not isinstance(vcs, list):
            logging.warning("No VCs attached to product data.")
            return 0  # CLAIM_REJECTED

        revoked_found = False
        verified_found = False

        for vc_data in vcs:
            status = self.validate(vc_data)
            if status == "CLAIM_REVOKED":
                revoked_found = True
            elif status == "CLAIM_REJECTED":
                return 0  # Any rejection immediately rejects
            elif status == "CLAIM_VERIFIED":
                verified_found = True

        if revoked_found:
            return -1  # CLAIM_REVOKED
        if verified_found:
            return 1  # CLAIM_VERIFIED
        return 0  # CLAIM_REJECTED
