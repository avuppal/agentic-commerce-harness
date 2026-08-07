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
