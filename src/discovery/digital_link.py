# src/discovery/digital_link.py

import re
from urllib.parse import urlparse, parse_qs

class DigitalLinkParser:
    def __init__(self):
        # Regex to capture GTIN, BATCH, and SERIAL from the canonical URI structure
        # Example: https://id.brand.com/01/{GTIN}/10/{BATCH}/21/{SERIAL}
        self.uri_pattern = re.compile(
            r"^https://[^/]+/01/([^/]+)/10/([^/]+)/21/([^/]+)$"
        )

    def parse_uri(self, uri: str) -> dict:
        """Parses a GS1 Digital Link URI to extract components.

        Args:
            uri: The GS1 Digital Link URI string.

        Returns:
            A dictionary containing extracted components (gtin, batch, serial) or None if parsing fails.
        """
        match = self.uri_pattern.match(uri)
        if match:
            gtin, batch, serial = match.groups()
            return {
                "gtin": gtin,
                "batch": batch,
                "serial": serial,
            }
        # Fallback for URIs that might not strictly follow the canonical pattern, but still contain query parameters.
        # This part might need refinement based on more examples.
        parsed_url = urlparse(uri)
        query_params = parse_qs(parsed_url.query)
        
        components = {}
        if "01" in query_params:
            components["gtin"] = query_params["01"][0]
        if "10" in query_params:
            components["batch"] = query_params["10"][0]
        if "21" in query_params:
            components["serial"] = query_params["21"][0]

        if components:
            return components
        
        return None

    def resolve_content(self, uri: str, accept_header: str) -> str:
        """Resolves the content based on the Accept header.

        Args:
            uri: The GS1 Digital Link URI.
            accept_header: The value of the Accept header (e.g., 'application/ld+json').

        Returns:
            The resolved content as a string.
        """
        parsed_components = self.parse_uri(uri)
        if not parsed_components:
            return "Error: Invalid URI"

        # TODO: Implement actual data fetching logic based on parsed_components and accept_header.
        # This will likely involve calling other services or modules.
        
        if accept_header == "application/ld+json":
            # Placeholder for GS1 Web Vocabulary JSON-LD graph
            return f"{{ '@context': 'http://schema.org/', '@type': 'Product', 'gtin': '{parsed_components.get('gtin')}', 'batch': '{parsed_components.get('batch')}', 'serial': '{parsed_components.get('serial')}', 'description': 'GS1 Web Vocabulary JSON-LD data placeholder' }}"
        elif accept_header == "application/vc+ld+json":
            # Placeholder for Verifiable Credentials (VC)
            return f"{{ '@context': 'https://www.w3.org/2018/credentials/v1', '@type': 'VerifiableCredential', 'credentialSubject': {{ 'gtin': '{parsed_components.get('gtin')}' }}, 'description': 'Verifiable Credential data placeholder' }}"
        elif accept_header == "text/html":
            # Placeholder for human-optimized visual PDP
            return f"<html><body><h1>Product Details for {parsed_components.get('gtin')}</h1><p>Batch: {parsed_components.get('batch')}</p><p>Serial: {parsed_components.get('serial')}</p><p>Human-readable Product Detail Page placeholder.</p></body></html>"
        else:
            # Handle other Accept headers or default behavior
            return f"Unsupported Accept header: {accept_header}"

    def handle_linkset_redirection(self, uri: str, rel_type: str) -> str:
        """Handles Linkset Redirection based on rel types.

        Args:
            uri: The GS1 Digital Link URI.
            rel_type: The rel type (e.g., 'gs1:pip', 'gs1:dpp').

        Returns:
            A URL or information related to the redirection.
        """
        parsed_components = self.parse_uri(uri)
        if not parsed_components:
            return "Error: Invalid URI for redirection"

        # TODO: Implement logic to construct or fetch redirection URLs based on rel_type
        # For example, gs1:pip might construct a canonical product page URL.
        # gs1:dpp would fetch the Digital Product Passport.
        # gs1:certificationInfo would fetch VC issuer endpoint.

        base_url = f"https://id.brand.com/01/{parsed_components.get('gtin')}" # Example base

        if rel_type == "gs1:pip":
            return f"{base_url}/info"
        elif rel_type == "gs1:dpp":
            return f"{base_url}/dpp"
        elif rel_type == "gs1:certificationInfo":
            return f"{base_url}/certinfo"
        else:
            return f"Unknown rel type for redirection: {rel_type}"

# Example Usage (for testing purposes, not part of the final module structure)
# if __name__ == "__main__":
#     parser = DigitalLinkParser()
#     test_uri = "https://id.brand.com/01/40123456789012/10/ABC/21/XYZ"
#     
#     # Test URI parsing
#     components = parser.parse_uri(test_uri)
#     print(f"Parsed components: {components}")
# 
#     # Test content resolution
#     ld_json_content = parser.resolve_content(test_uri, "application/ld+json")
#     print(f"\nJSON-LD Content:\n{ld_json_content}")
# 
#     vc_content = parser.resolve_content(test_uri, "application/vc+ld+json")
#     print(f"\nVC Content:\n{vc_content}")
# 
#     html_content = parser.resolve_content(test_uri, "text/html")
#     print(f"\nHTML Content:\n{html_content}")
# 
#     # Test linkset redirection
#     pip_url = parser.handle_linkset_redirection(test_uri, "gs1:pip")
#     print(f"\nGS1 PIP URL: {pip_url}")
# 
#     dpp_url = parser.handle_linkset_redirection(test_uri, "gs1:dpp")
#     print(f"\nGS1 DPP URL: {dpp_url}")
