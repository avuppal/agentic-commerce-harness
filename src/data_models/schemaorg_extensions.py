# -*- coding: utf-8 -*-
"""Schema.org extensions for GS1 compliance."""

from dataclasses import dataclass, field
from typing import List, Optional


class GS1Vocabulary:
    """Base class for GS1 vocabulary terms."""
    pass


@dataclass
class AllergenInformation(GS1Vocabulary):
    """Represents allergen information for a product."""
    status: str  # e.g., CONTAINED_IN, FREE_FROM, MAY_CONTAIN
    allergen: str
    description: Optional[str] = None


@dataclass
class NutritionalAttribute(GS1Vocabulary):
    """Represents a single nutritional attribute per serving."""
    name: str
    value: float
    unit: str
    serving_size: str


@dataclass
class NetContent(GS1Vocabulary):
    """Represents the net content of a product."""
    value: float
    unit: str


@dataclass
class Product(GS1Vocabulary):
    """Extensions to Schema.org Product for GS1 requirements."""
    gtin: str
    gpc_category_code: Optional[str] = None
    net_content: Optional[NetContent] = None
    allergen_information: List[AllergenInformation] = field(default_factory=list)
    nutritional_attributes: List[NutritionalAttribute] = field(default_factory=list)
    country_of_origin: Optional[str] = None


@dataclass
class Offer(GS1Vocabulary):
    """Extensions to Schema.org Offer for GS1 requirements."""
    # Add relevant GS1 attributes for Offer if any are specified
    pass


@dataclass
class Organization(GS1Vocabulary):
    """Extensions to Schema.org Organization for GS1 requirements."""
    # Add relevant GS1 attributes for Organization if any are specified
    pass


@dataclass
class Place(GS1Vocabulary):
    """Extensions to Schema.org Place for GS1 requirements."""
    # Add relevant GS1 attributes for Place if any are specified
    pass


# Example of how these might be used (optional, for clarity)
if __name__ == "__main__":
    # Example Product
    product = Product(
        gtin="01234567890123",
        gpc_category_code="10000042",
        net_content=NetContent(value=500.0, unit="g"),
        allergen_information=[
            AllergenInformation(status="CONTAINED_IN", allergen="Milk", description="Contains dairy")
        ],
        nutritional_attributes=[
            NutritionalAttribute(name="Energy", value=250.0, unit="kcal", serving_size="100g")
        ],
        country_of_origin="DE"
    )
    print(product)

    # Example Offer
    offer = Offer()
    print(offer)

    # Example Organization
    organization = Organization()
    print(organization)

    # Example Place
    place = Place()
    print(place)
