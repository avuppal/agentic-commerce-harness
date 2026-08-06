# src/discovery/content_negotiation.py

class ContentNegotiator:
    """
    Handles content negotiation based on the HTTP Accept header as specified in the PRD.
    """
    SUPPORTED_MEDIA_TYPES = {
        "application/ld+json": "json-ld",       # GS1 Web Vocabulary JSON-LD graph for AI Agents
        "application/vc+ld+json": "vc-ld",      # Verifiable Credentials set for claims & DPP
        "text/html": "html"                      # Human-optimized visual PDP with enhanced content
    }

    @classmethod
    def negotiate(cls, accept_header: str) -> str:
        """
        Determines the content type based on the Accept header.
        
        Args:
            accept_header (str): The value of the HTTP Accept header.
            
        Returns:
            str: The negotiated format identifier ('json-ld', 'vc-ld', or 'html'). Default is 'json-ld' for AI agents.
        """
        if not accept_header:
            return "json-ld"

        # Check for exact matches or partial matches
        for media_type, format_name in cls.SUPPORTED_MEDIA_TYPES.items():
            if media_type in accept_header:
                return format_name

        # Default fallback is JSON-LD for AI Agents as per PRD dual-surface priorities
        return "json-ld"
