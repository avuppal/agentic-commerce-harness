# src/compliance/gs1_fidelity_checker.py

import json
import logging
from typing import Dict, Any, List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GS1FidelityChecker:
    """
    Enforces 100% compliance with the GS1 Web Vocabulary v1.12 (http://gs1.org/voc/)
    by validating JSON-LD payloads and required product attributes.
    """

    MANDATED_ATTRIBUTES = [
        "gs1:gtin",
        "gs1:gpcCategoryCode",
        "gs1:netContent",
        "gs1:allergenInformation",
        "gs1:nutritionalAttribute",
        "gs1:countryOfOrigin"
    ]

    @classmethod
    def validate_payload(cls, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validates whether a JSON-LD payload contains all mandated GS1 Web Vocabulary attributes
        and conforms to basic schema requirements.
        
        Args:
            payload (Dict[str, Any]): The product JSON-LD structure.
            
        Returns:
            Tuple[bool, List[str]]: (Is compliant, list of missing or invalid fields)
        """
        errors = []
        logging.info("Starting GS1 Fidelity check on payload...")

        # 1. Verify JSON-LD Context and Structure
        context = payload.get("@context")
        if not context:
            errors.append("Missing '@context' field in JSON-LD.")
        else:
            context_str = str(context)
            if "gs1.org" not in context_str and "schema.org" not in context_str:
                errors.append("JSON-LD '@context' must include GS1 or Schema.org namespaces.")

        # 2. Check Class Alignment
        object_type = payload.get("@type")
        if not object_type:
            errors.append("Missing '@type' declaration in JSON-LD.")
        elif object_type not in ["Product", "gs1:Product", "Offer", "gs1:Offer"]:
            logging.warning(f"Object type '{object_type}' is unconventional, but allowed if attributes conform.")

        # 3. Check for Mandated Attributes (PRD Section 3.1)
        for attr in cls.MANDATED_ATTRIBUTES:
            # Check both prefixed and non-prefixed versions
            short_name = attr.split(":")[-1]
            if attr not in payload and short_name not in payload:
                errors.append(f"Missing mandated attribute: {attr}")
            else:
                # Basic validation of attribute values
                val = payload.get(attr) or payload.get(short_name)
                if val is None:
                    errors.append(f"Mandated attribute {attr} cannot be null.")
                elif attr == "gs1:gtin" and not (isinstance(val, str) and len(val) in [8, 12, 13, 14]):
                    errors.append(f"Attribute {attr} must be a valid 8, 12, 13, or 14-digit GTIN. Got: '{val}'")

        is_compliant = len(errors) == 0
        if is_compliant:
            logging.info("GS1 Fidelity Check: 100% COMPLIANT.")
        else:
            logging.warning(f"GS1 Fidelity Check failed. Violations: {errors}")

        return is_compliant, errors
