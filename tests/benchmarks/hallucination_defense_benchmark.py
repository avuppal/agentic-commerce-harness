import unittest
import time
from typing import Dict, Any, List

# Constants representing validation outcomes.
# Assuming VerifiableCredentialValidator.validate_claims returns distinct integer statuses.
CLAIM_VERIFIED = 1
CLAIM_REJECTED = 0
CLAIM_REVOKED = -1

# Import the validator
# Assuming the path is correct relative to the project root
from src.vc_handler.vc_validator import VerifiableCredentialValidator

class TestHallucinationDefense(unittest.TestCase):
    """
    Tests for defending against hallucinated or invalid claims using Verifiable Credentials.
    """

    def setUp(self):
        """Set up test environment."""
        self.validator = VerifiableCredentialValidator()

        # Mock product with a false claim but no associated Verifiable Credential.
        # The validator should reject any claims if no VC is present for verification.
        self.mock_product_with_false_claim_no_vc = {
            "id": "product-false-claim-001",
            "description": "A product that claims to be '100% Certified Organic' but has no VC.",
            "claims": [
                {"type": "Organic", "value": "Certified", "source": "label"}
            ],
            # No 'vcs' field, so validator cannot verify the claim.
        }

        # Mock a revoked Verifiable Credential.
        # This VC includes a 'credentialStatus' indicating revocation, simulated via statusListIndex.
        # The validator is expected to check this status during claim validation.
        self.mock_revoked_vc_data = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiableCredential", "ProductCertificationCredential"],
            "issuer": "did:key:z6MkpTHR8VNsBxR", # A trusted issuer
            "issuance_date": "2026-08-01T12:00:00Z",
            "credential_subject": {
                "@id": "urn:product:1234567890123",
                "type": ["ProductCertificationSubject"],
                "certificationName": "USDA Organic Certificate",
                "certificationStatus": "revoked", # Might be redundant if statusListIndex is primary
                "issuanceDate": "2026-08-01T00:00:00Z"
            },
            "credentialStatus": {
                "id": "https://example.com/status/revoked-list",
                "type": "StatusList2021",
                "statusListIndex": 99  # Simulating a revoked status based on StatusList2021
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "created": "2026-08-01T12:05:00Z",
                "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                "jws": "fake_signature_for_revoked_vc" # Placeholder for actual signature
            }
        }

        # Mock product data containing the revoked VC.
        self.mock_product_with_revoked_vc = {
            "id": "product-revoked-vc-789",
            "description": "A product with a revoked organic certification.",
            "vcs": [self.mock_revoked_vc_data] # Assuming VCs are passed as a list within product data
        }

        # Mock a valid Verifiable Credential for baseline testing.
        self.mock_valid_vc_data = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiableCredential", "ProductCertificationCredential"],
            "issuer": "did:key:z6MkpTHR8VNsBxR", # A trusted issuer
            "issuance_date": "2026-08-01T12:00:00Z",
            "credential_subject": {
                "@id": "urn:product:9876543210987",
                "type": ["ProductCertificationSubject"],
                "certificationName": "USDA Organic Certificate",
                "certificationStatus": "verified",
                "issuanceDate": "2026-08-01T00:00:00Z"
            },
            "credentialStatus": {
                "id": "https://example.com/status/valid-list",
                "type": "StatusList2021",
                "statusListIndex": 5 # Assuming index 5 is not revoked
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "created": "2026-08-01T12:05:00Z",
                "verificationMethod": "did:key:z6MkpTHR8VNsBxR#key-1",
                "jws": "fake_signature_for_valid_vc" # Placeholder for actual signature
            }
        }

        self.mock_product_with_valid_vc = {
            "id": "product-valid-vc-101",
            "description": "A product with a valid organic certification.",
            "vcs": [self.mock_valid_vc_data]
        }


    def test_claim_rejected_without_vc(self):
        """
        Test that a claim without an associated Verifiable Credential is rejected.
        This checks the defense against hallucinated claims where no proof is provided.
        """
        print("\n--- Running test_claim_rejected_without_vc ---")
        # The validator should reject the claim because no VC was provided for verification.
        result = self.validator.validate_claims(self.mock_product_with_false_claim_no_vc)

        self.assertEqual(result, CLAIM_REJECTED, 
                         "Claim should be rejected when no Verifiable Credential is present.")
        print(f"Result: {result}, Expected: {CLAIM_REJECTED}")

    def test_claim_revoked_vc(self):
        """
        Test that a claim associated with a revoked Verifiable Credential is rejected.
        This checks the defense against using credentials that are no longer valid.
        """
        print("\n--- Running test_claim_revoked_vc ---")
        # The validator should detect the revoked status of the VC using credentialStatus.
        result = self.validator.validate_claims(self.mock_product_with_revoked_vc)

        self.assertEqual(result, CLAIM_REVOKED, 
                         "Claim should be rejected due to a revoked Verifiable Credential.")
        print(f"Result: {result}, Expected: {CLAIM_REVOKED}")

    def test_claim_verified_with_valid_vc(self):
        """
        Test that a claim associated with a valid Verifiable Credential is verified.
        This is a baseline test to ensure valid credentials are processed correctly.
        """
        print("\n--- Running test_claim_verified_with_valid_vc ---")
        result = self.validator.validate_claims(self.mock_product_with_valid_vc)
        self.assertEqual(result, CLAIM_VERIFIED, 
                         "Claim should be verified with a valid Verifiable Credential.")
        print(f"Result: {result}, Expected: {CLAIM_VERIFIED}")

if __name__ == '__main__':
    unittest.main()
