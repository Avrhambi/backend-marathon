from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    # TODO: Define attributes:
    # - id: int
    # - name: str
    # - price: float
    # - is_available: bool
    id: int
    name: str
    price: float
    is_available: bool

def test_product_parsing():
    raw_payload = {
        "id": "101",          # String that should coerce to int
        "name": "Mechanical Keyboard",
        "price": "99.99",     # String that should coerce to float
        "is_available": "true" # String that should coerce to bool, change this to a number will cause error
    }

    # TODO: Instantiate Product with raw_payload unpacked (**raw_payload)
    # TODO: Print the parsed model and verify types (type(product.id), etc.)
    try:
        product = Product(**raw_payload)
        print("Successfully Parsed Model:", product)
        print("Coerced Types:", type(product.id), type(product.price), type(product.is_available))
        # Output: <class 'int'> <class 'float'> <class 'bool'>
    except ValidationError as e:
        print("Validation failed:", e)

if __name__ == "__main__":
    test_product_parsing()