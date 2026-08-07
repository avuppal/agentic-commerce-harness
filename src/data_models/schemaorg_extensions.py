from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class UnitPriceSpecification(BaseModel):
    """
    Represents a unit price specification, similar to schema.org/UnitPriceSpecification.
    """
    price: float = Field(..., description="The price of the item.")
    price_currency: str = Field(..., description="The currency of the price (e.g., 'USD', 'EUR').")
    unit_code: str = Field(..., description="A UN/CEFACT Common Code for the unit (e.g., 'GRM' for gram, 'MLT' for milliliter, 'KGM' for kilogram, 'LTR' for liter).")
    reference_quantity: float = Field(1.0, description="The quantity to which the price refers (e.g., if price is per 100g, reference_quantity would be 100).")
    unit_name: Optional[str] = Field(None, description="The name of the unit (e.g., 'gram', 'milliliter').")


class MerchantReputation(BaseModel):
    """
    Represents merchant reputation data.
    """
    domain_name: str
    trust_score: float = Field(..., ge=0.0, le=1.0, description="A normalized trust score from 0.0 to 1.0.")
    average_rating: Optional[float] = Field(None, description="The average rating from review platforms.")
    review_count: Optional[int] = Field(None, description="The total number of reviews.")
    sources: List[str] = Field(default_factory=list, description="List of sources for the reputation data (e.g., ['TrustPilot', 'Google Reviews']).")
