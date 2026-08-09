# src/security/jwt_handler.py

import logging
from typing import Dict, Any, Optional

from jwcrypto import jwt, jwk
from jwcrypto.common import JWException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JWTHandler:
    """
    Handles decoding and validation of OIDC JWTs.
    """

    def __init__(self, jwks_url: str):
        """
        Initializes the JWTHandler with the URL to the JSON Web Key Set (JWKS).

        Args:
            jwks_url: The URL of the OIDC provider's JWKS endpoint.
        """
        self.jwks_url = jwks_url
        self._load_jwks()

    def _load_jwks(self):
        """
        Loads the JSON Web Key Set from the provided URL.
        In a real-world scenario, this would fetch the keys from the URL.
        For this implementation, we will use a mock key set.
        """
        logging.info(f"Loading JWKS from {self.jwks_url}")
        # This is a placeholder. In a real application, you would fetch this
        # from the URL and cache it.
        # For example:
        # response = requests.get(self.jwks_url)
        # self.jwk_set = jwk.JWKSet.from_json(response.text)
        # For now, let's create a mock key for demonstration.
        key = jwk.JWK.generate(kty='EC', crv='P-256')
        self.jwk_set = jwk.JWKSet()
        self.jwk_set.add(key)
        # Let's log the public key so we know what to use for signing/testing
        logging.info(f"Mock public JWK generated: {key.export(private_key=False)}")

    def decode_and_validate_jwt(self, token: str, issuer: str, audience: str) -> Optional[Dict[str, Any]]:
        """
        Decodes a JWT and validates its signature, expiry, issuer, and audience.

        Args:
            token: The JWT string.
            issuer: The expected issuer of the token.
            audience: The expected audience of the token.

        Returns:
            The decoded claims as a dictionary if the token is valid, otherwise None.
        """
        if not isinstance(token, str):
            logging.error("Invalid token format: token must be a string.")
            return None

        try:
            # Load the token with the key set for signature verification
            decoded_token = jwt.JWT(key=self.jwk_set, jwt=token)

            # Access claims after decoding
            claims = decoded_token.claims

            # Manual validation of standard claims
            if claims.get('iss') != issuer:
                logging.warning(f"Invalid issuer. Expected: {issuer}, Got: {claims.get('iss')}")
                return None

            if claims.get('aud') != audience:
                logging.warning(f"Invalid audience. Expected: {audience}, Got: {claims.get('aud')}")
                return None
            
            # The jwcrypto library automatically validates signature and expiry against the key.
            # If we reach here, the token is considered valid.
            logging.info("JWT successfully decoded and validated.")
            return claims

        except JWException as e:
            logging.error(f"JWT validation failed: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred during JWT processing: {e}")
            return None

if __name__ == '__main__':
    # Example usage (for demonstration and testing)
    
    # 1. Setup the handler
    # In a real app, this would be a real OIDC provider URL
    mock_jwks_url = "https://idp.example.com/.well-known/jwks.json"
    jwt_handler = JWTHandler(mock_jwks_url)

    # 2. Generate a sample token (normally an OIDC provider does this)
    # Get the key from the handler's mock key set
    signing_key = next(iter(jwt_handler.jwk_set))
    
    header = {'alg': 'ES256', 'kid': signing_key.key_id}
    claims = {
        'iss': 'https://idp.example.com',
        'aud': 'mcp-api',
        'sub': 'user-123',
        'exp': 9999999999, # A timestamp far in the future
        'iat': 1616239022
    }
    
    token_to_sign = jwt.JWT(header=header, claims=claims)
    token_to_sign.make_signed_token(signing_key)
    signed_token = token_to_sign.serialize()
    
    print(f"Generated sample token: {signed_token}")

    # 3. Decode and validate the token
    expected_issuer = 'https://idp.example.com'
    expected_audience = 'mcp-api'
    
    decoded_claims = jwt_handler.decode_and_validate_jwt(signed_token, expected_issuer, expected_audience)

    if decoded_claims:
        print("\nToken is valid!")
        print("Decoded Claims:")
        import json
        print(json.dumps(decoded_claims, indent=2))
    else:
        print("\nToken is invalid.")
        
    # Example of a token with a bad issuer
    print("\n--- Testing with bad issuer ---")
    bad_issuer_claims = jwt_handler.decode_and_validate_jwt(signed_token, "https://bad-issuer.com", expected_audience)
    if not bad_issuer_claims:
        print("Correctly identified bad issuer.")
