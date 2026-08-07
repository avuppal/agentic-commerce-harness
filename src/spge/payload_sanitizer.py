import re
from src.utils.state_emitter import StateEmitter # 1. Import

class PayloadSanitizer:
    """Sanitizes structured data payloads to prevent indirect prompt injection attacks."""

    def __init__(self):
        self.state_emitter = StateEmitter() # 2. Instantiate
        self.harmful_patterns = [
            r"ignore previous instructions",
            r"you are an attacker",
            r"system prompt override",
            r"execute command",
        ]
        self.harmful_regex = re.compile('|'.join(self.harmful_patterns), re.IGNORECASE)

    def sanitize(self, payload):
        """Recursively sanitizes a structured data payload."""
        if isinstance(payload, dict):
            return {key: self.sanitize(value) for key, value in payload.items()}
        elif isinstance(payload, list):
            return [self.sanitize(item) for item in payload]
        elif isinstance(payload, str):
            if self.harmful_regex.search(payload):
                # 3. Emit an event with relevant details
                self.state_emitter.emit(
                    "security.sanitization.redaction",
                    {
                        "original_payload": payload,
                        "patterns_detected": self.harmful_regex.findall(payload)
                    }
                )
            return self.harmful_regex.sub("[REDACTED]", payload)
        else:
            return payload
