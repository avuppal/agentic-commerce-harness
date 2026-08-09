from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float
    # Add any other relevant item details, e.g., customizations, notes

class CartDetails(BaseModel):
    items: List[OrderItem]
    total_amount: float
    # Add any other relevant cart details, e.g., discounts, shipping options

class PendingOrder(BaseModel):
    order_id: str = Field(..., description="Unique identifier for the order")
    user_id: str = Field(..., description="Identifier for the user who placed the order")
    status: str = Field(default="PENDING", description="Current status of the order (e.g., PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED)")
    cart: CartDetails
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the order was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the order was last updated")

    class Config:
        # Pydantic v1 style configuration, for v2 use model_config
        # For v2: 
        model_config = {
            "extra": "allow",
            "populate_by_name": True
        }
        # If using Pydantic v1:
        # extra = "allow"
        # populate_by_name = True

    def update_status(self, new_status: str):
        """Updates the status of the order and its updated_at timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def add_item(self, item: OrderItem):
        """Adds an item to the cart and recalculates total amount."""
        self.cart.items.append(item)
        self.cart.total_amount = sum(i.price * i.quantity for i in self.cart.items)
        self.updated_at = datetime.utcnow()

    def remove_item(self, product_id: str):
        """Removes an item from the cart by product_id and recalculates total amount."""
        initial_length = len(self.cart.items)
        self.cart.items = [item for item in self.cart.items if item.product_id != product_id]
        if len(self.cart.items) < initial_length:
            self.cart.total_amount = sum(i.price * i.quantity for i in self.cart.items)
            self.updated_at = datetime.utcnow()
        # Optionally, you might want to raise an error if the item wasn't found

