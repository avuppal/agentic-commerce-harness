# src/spge/payload_sanitizer.py

import re

class PayloadSanitizer:
    """Sanitizes structured data payloads to prevent indirect prompt injection attacks."""

    def __init__(self):
        # Define a list of potentially harmful patterns or keywords.
        # This is a starting point and can be expanded.
        self.harmful_patterns = [
            r"ignore previous instructions",
            r"you are an attacker",
            r"system prompt override",
            r"execute command",
            # Add more patterns as needed based on common injection techniques
        ]

        # Compile regex for efficiency
        self.harmful_regex = re.compile('|'.join(self.harmful_patterns), re.IGNORECASE)

    def sanitize(self, payload):
        """Recursively sanitizes a structured data payload.

        Args:
            payload: The data structure (dict, list, str, etc.) to sanitize.

        Returns:
            The sanitized payload.
        """
        if isinstance(payload, dict):
            return {key: self.sanitize(value) for key, value in payload.items()}
        elif isinstance(payload, list):
            return [self.sanitize(item) for item in payload]
        elif isinstance(payload, str):
            # Sanitize string values
            sanitized_string = self.harmful_regex.sub("[REDACTED]", payload)
            # Further sanitization can be added here, e.g., escaping characters
            return sanitized_string
        else:
            # Return other data types as is
            return payload

