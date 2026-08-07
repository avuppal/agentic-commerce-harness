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
