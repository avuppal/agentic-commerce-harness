import re
from urllib.parse import urlparse, parse_qs

class DigitalLinkParser:
    def parse_uri(self, uri: str) -> dict:
        """
        Parses a GS1 Digital Link URI to extract key-value pairs of Application Identifiers.
        This is a flexible implementation that handles optional and out-of-order AIs
        from both the path and query string.
        
        Example: https://id.brand.com/01/1234567890123/10/BATCH123
        Returns: {'01': '1234567890123', '10': 'BATCH123'}
        """
        parsed_uri = urlparse(uri)
        # Clean leading/trailing slashes and split path into segments
        path_segments = parsed_uri.path.strip('/').split('/')
        
        gs1_data = {}
        
        # Use an iterator to process path segments in (key, value) pairs
        segment_iterator = iter(path_segments)
        for key in segment_iterator:
            try:
                # The value is the next segment in the path
                value = next(segment_iterator)
                if key.isdigit():
                    gs1_data[key] = value
            except StopIteration:
                # This handles an odd number of path segments; the last segment is ignored.
                break
                
        # The standard also allows for AIs to be in the query string
        query_params = parse_qs(parsed_uri.query)
        for key, value_list in query_params.items():
            # Take the first value if multiple are present for the same key
            if key.isdigit() and value_list:
                gs1_data[key] = value_list[0]
                
        return gs1_data


class DigitalLink:
    def __init__(self, uri: str):
        self.uri = uri
        self.parser = DigitalLinkParser()

    def parse(self) -> dict:
        """
        Parses the URI and returns a normalized dictionary of extracted Application Identifiers.
        To support clients expecting both standard GS1 AI codes ('01', '10', '21') and friendly keys
        ('gtin', 'batch', 'serial'), we provide both mapping representations.
        """
        raw_components = self.parser.parse_uri(self.uri)
        normalized = {}
        if not raw_components:
            return normalized

        # Map standard GS1 AI keys to friendly names for ease of use
        if '01' in raw_components:
            normalized['gtin'] = raw_components['01']
        if '10' in raw_components:
            normalized['batch'] = raw_components['10']
        if '21' in raw_components:
            normalized['serial'] = raw_components['21']
            
        # Keep original numeric keys for standard compliance
        for k, v in raw_components.items():
            normalized[k] = v
            
        return normalized

    def route(self) -> dict:
        """
        Determines the redirection paths and acceptable content negotiation headers
        for standard relationship types (gs1:pip, gs1:dpp, gs1:certificationInfo)
        as defined in docs/discovery/digital_link.md.
        """
        parsed = self.parse()
        gtin = parsed.get("gtin") or parsed.get("01") or "unknown"
        
        # Parse URI to construct domain-specific base URLs dynamically
        parsed_uri = urlparse(self.uri)
        domain = parsed_uri.netloc or "id.brand.com"
        scheme = parsed_uri.scheme or "https"
        base_url = f"{scheme}://{domain}/01/{gtin}"
        
        return {
            "acceptable_headers": [
                "application/ld+json",
                "application/vc+ld+json",
                "text/html"
            ],
            "redirection_links": {
                "gs1:pip": f"{base_url}/info",
                "gs1:dpp": f"{base_url}/dpp",
                "gs1:certificationInfo": f"{base_url}/certinfo"
            }
        }
