import logging
from typing import Dict, Any, Optional

# Import StateEmitter from its correct location
from src.utils.state_emitter import StateEmitter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UnitPriceNormalizer:
    """
    Normalizes unit prices across varying package sizes using gs1:netContent and standard unit measures
    to enable agent unit-price benchmarking (REQ-SIGE-03).
    """

    def __init__(self, state_emitter: StateEmitter):
        """
        Initializes the UnitPriceNormalizer with a StateEmitter instance.

        Args:
            state_emitter: An instance of StateEmitter for emitting events.
        """
        self.state_emitter = state_emitter

    # Conversion factor map to normalize units to base units (e.g. grams, milliliters, pieces)
    # Corrected duplicate 'kilograms' entry and ensured consistent formatting.
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

    def calculate_normalized_price(self, product: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calculates the normalized price for a product.

        Args:
            product: A dictionary representing the product data, expected to contain 'price',
                     'netContent' (with 'value' and 'unitCode'), and 'sku'.

        Returns:
            A dictionary with the normalized price information (e.g., {'price': 0.5, 'unit': 'g'})
            or None if normalization fails.
        """
        price = product.get('price')
        net_content = product.get('netContent')
        sku = product.get('sku')

        if price is None or net_content is None or sku is None:
            logging.warning(f"Skipping normalization for product {sku or 'unknown'}: Missing price, netContent, or sku.")
            return None

        try:
            value = float(net_content.get('value'))
            unit = net_content.get('unitCode', '').lower()
        except (ValueError, TypeError):
            logging.warning(f"Skipping normalization for product {sku}: Invalid netContent value or unitCode.")
            return None

        conversion_factor = self.UNIT_CONVERSIONS.get(unit)

        if conversion_factor is None:
            logging.warning(f"UnitPriceNormalizer: Could not find unit conversion for unit code '{unit}' for product SKU '{sku}'. Product price cannot be normalized.")
            return None

        # Determine base unit and perform conversion
        # For simplicity, assuming common units map directly to base units or their multiples
        # More complex logic might be needed for units like 'oz' vs 'lb' if not handled by conversion_factor alone
        base_unit = "g" # Defaulting mass to grams
        if unit in ["ml", "milliliter", "milliliters", "l", "liter", "liters", "fl_oz", "fluid_ounce", "fluid_ounces", "gal", "gallon", "gallons"]:
            base_unit = "ml" # Defaulting volume to milliliters
        elif unit in ["pce", "pc", "piece", "pieces", "count", "ct", "ea", "each"]:
            base_unit = "pce" # Defaulting count to pieces

        normalized_price_value = (price / value) * conversion_factor

        # Log success event using state_emitter
        event_data = {
            "product_sku": sku,
            "original_price": price,
            "original_value": value,
            "original_unit": unit,
            "normalized_price": round(normalized_price_value, 4), # Round for cleaner output
            "base_unit": base_unit
        }
        self.state_emitter.emit("UnitPriceNormalized", event_data, level="info")

        logging.info(f"UnitPriceNormalizer: Successfully normalized price for SKU '{sku}'. Original: {price}/{value}{unit}. Normalized: {round(normalized_price_value, 4)}/{base_unit}.")

        return {"price": round(normalized_price_value, 4), "unit": base_unit}
