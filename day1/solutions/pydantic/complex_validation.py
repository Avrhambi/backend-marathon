from typing import List
from pydantic import BaseModel, Field

class Customer(BaseModel):
    name: str
    email: str

class OrderItem(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)
    price_per_unit: float = Field(gt=0)

class Order(BaseModel):
    order_id: str
    customer: Customer
    items: List[OrderItem]

    # TODO: Add a computed property 'total_price' that sums (quantity * price_per_unit) for all items
    @property
    def total_price(self) -> float:
        return sum(item.quantity * item.price_per_unit for item in self.items)

def test_nested_order():
    raw_order_data = {
        "order_id": "ORD-9921",
        "customer": {"name": "Alice", "email": "alice@example.com"},
        "items": [
            {"item_id": 1, "quantity": 2, "price_per_unit": 15.0},
            {"item_id": 2, "quantity": 1, "price_per_unit": 50.0}
        ]
    }

    # TODO: Parse raw_order_data into Order
    # TODO: Calculate total price
    order = Order(**raw_order_data)
    print("Parsed Order:", order)
    print("Total Order Price:", order.total_price)

    # TODO: Export the model to a Python dict using model_dump()
    # Serialization:
    order_dict = order.model_dump()
    print("Serialized Dict:", order_dict)
 
if __name__ == "__main__":
    test_nested_order()