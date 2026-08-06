# tests/benchmarks/vc_validation_benchmark.py

import time
import unittest
from src.vc_handler.vc_validator import VerifiableCredentialValidator

class TestVerifiableCredentialLatencyBenchmark(unittest.TestCase):
    """
    Measures Verifiable Credential cryptographic validation latency,
    aiming for < 15ms per credential proof validation as specified in the NFRs.
    """

    def setUp(self):
        self.validator = VerifiableCredentialValidator()
        self.mock_vc = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://www.gs1.org/voc/"
            ],
            "@id": "urn:uuid:5bc1a23c-83b4-432d-9876-0f9c21ef9a13",
            "type": ["VerifiableCredential", "ProductCertificationCredential"],
            "issuer": {
                "@id": "did:key:z6MkpTHR8VNsBxR",
                "type": ["Organization"],
                "name": "Organic Trade Association Certification Body"
            },
            "issuance_date": "2026-08-01T12:00:00Z",
            "credential_subject": {
                "@id": "urn:product:1234567890123",
                "type": ["ProductCertificationSubject"],
                "certificationName": "USDA Organic Certificate",
                "certificationStatus": "verified",
                "issuanceDate": "2026-08-01T00:00:00Z"
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "created": "2026-08-01T12:05:00Z",
                "proof_purpose": "assertionMethod",
                "verification_method": "did:key:z6MkpTHR8VNsBxR#key-1",
                "proof_value": "z6MkmLgYvW5vE99zD8699g39ff2kskd9f82kdsk3929dkaskf938faskdf8"
            }
        }

    def test_latency_performance(self):
        start_time = time.perf_counter()
        
        # Run 100 validation iterations to simulate throughput and measure average latency
        iterations = 100
        for _ in range(iterations):
            result = self.validator.validate(self.mock_vc)
            self.assertEqual(result, "CLAIM_VERIFIED")

        end_time = time.perf_counter()
        total_duration_ms = (end_time - start_time) * 1000.0
        average_latency_ms = total_duration_ms / iterations

        print(f"\n--- VC Cryptographic Latency Benchmark ---")
        print(f"Total time for {iterations} validations: {total_duration_ms:.2f} ms")
        print(f"Average latency per proof verification: {average_latency_ms:.2f} ms")
        print(f"PRD NFR Latency Target: < 15.00 ms")
        print(f"-------------------------------------------")

        # Assert that the latency is well below the 15ms NFR threshold
        self.assertLess(average_latency_ms, 15.0)

if __name__ == "__main__":
    unittest.main()
