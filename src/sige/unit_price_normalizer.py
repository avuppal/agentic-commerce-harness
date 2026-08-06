# src/sige/unit_price_normalizer.py

import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UnitPriceNormalizer:
    """
    Normalizes unit prices across varying package sizes using gs1:netContent and standard unit measures
    to enable agent unit-price benchmarking (REQ-SIGE-03).
    """

    # Conversion factor map to normalize units to base units (e.g. grams, milliliters, pieces)
    UNIT_CONVERSIONS = {
        # Mass (base: gram - g)
        "g": 1.0,
        "gr": 1.0,
        "gram": 1.0,
        "grams": 1.0,
        "kg": 1000.0,
        "kilogram": 1000.0,
        "kilograms": 1000.0,
        "oz": 28.3495,
        "ounce": 28.3495,
        "ounces": 28.3495,
        "lb": 453.592,
        "pound": 453.592,
        "pounds": 453.592,

        # Volume (base: milliliter - ml)
        "ml": 1.0,
        "milliliter": 1.0,
        "milliliters": 1.0,
        "l": 1000.0,
        "liter": 1000.0,
        "liters": 1000.0,
        "fl_oz": 29.5735,
        "fluid_ounce": 29.5735,
        "fluid_ounces": 29.5735,
        "gal": 3785.41,
        "gallon": 3785.41,
        "gallons": 3785.41,

        # Count (base: item/piece - pce)
        "pce": 1.0,
        "pc": 1.0,
        "piece": 1.0,
        "pieces": 1.0,
        "count": 1.0,
        "ct": 1.0,
        "ea": 1.0,
        "each": 1.0
    }

    @classmethod
    def parse_net_content(cls, net_content: Any) -> Optional[Dict[str, Any]]:
        """
        Parses various gs1:netContent structures (e.g., direct string, dict, QuantitativeValue)
        into a standardized value and unit.
        """
        if not net_content:
            return None

        # Scenario 1: QuantitativeValue as dictionary
        if isinstance(net_content, dict):
            val = net_content.get("gs1:value") or net_content.get("value")
            unit = net_content.get("gs1:unitCode") or net_content.get("unitCode") or net_content.get("unit")
            if val is not None and unit is not None:
                try:
                    return {"value": float(val), "unit": str(unit).lower().strip()}
                except ValueError:
                    return None

        # Scenario 2: String representation (e.g. "100 g", "1.5 Liters")
        if isinstance(net_content, str):
            parts = net_content.strip().split()
            if len(parts) >= 2:
                try:
                    val = float(parts[0])
                    unit = "".join(parts[1:]).lower().strip()
                    return {"value": val, "unit": unit}
                except ValueError:
                    return None

        return None

    @classmethod
    def get_base_unit_category(cls, unit: str) -> Optional[str]:
        """
        Determines the category (mass, volume, count) of a unit.
        """
        # Mass units
        if unit in ["g", "gr", "gram", "grams", "kg", "kilogram", "kilograms", "oz", "ounce", "ounces", "lb", "pound", "pounds"]:
            return "mass"
        # Volume units
        if unit in ["ml", "milliliter", "milliliters", "l", "liter", "liters", "fl_oz", "fluid_ounce", "fluid_ounces", "gal", "gallon", "gallons"]:
            return "volume"
        # Count units
        if unit in ["pce", "pc", "piece", "pieces", "count", "ct", "ea", "each"]:
            return "count"
        return None

    def normalize(self, price: float, net_content: Any) -> Optional[Dict[str, Any]]:
        """
        Normalizes a price to a standard unit (per gram, per milliliter, or per piece).
        
        Args:
            price (float): The retail price of the offer.
            net_content (Any): The net content description (QuantitativeValue dict or string).
            
        Returns:
            dict: Containing normalized price, normalized value, normalized unit, and category.
        """
        parsed = self.parse_net_content(net_content)
        if not parsed:
            logging.warning(f"Could not parse net content: {net_content}")
            return None

        value = parsed["value"]
        unit = parsed["unit"]

        if value <= 0:
            logging.warning(f"Invalid net content value: {value}")
            return None

        conversion_factor = self.UNIT_CONVERSIONS.get(unit)
        if not conversion_factor:
            logging.warning(f"Unsupported unit for normalization: {unit}")
            return None

        category = self.get_base_unit_category(unit)
        if not category:
            return None

        # Convert to base unit quantity
        base_quantity = value * conversion_factor
        normalized_price = price / base_quantity

        # Determine standard representation
        if category == "mass":
            base_unit = "g"
            standard_repr = f"${normalized_price:.4f}/g"
        elif category == "volume":
            base_unit = "ml"
            standard_repr = f"${normalized_price:.4f}/ml"
        else:
            base_unit = "pce"
            standard_repr = f"${normalized_price:.4f}/count"

        logging.info(f"Normalized price {price} for {value} {unit} -> {standard_repr}")
        return {
            "normalized_price": normalized_price,
            "base_quantity": base_quantity,
            "base_unit": base_unit,
            "standard_repr": standard_repr,
            "category": category
        }
