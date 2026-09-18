from pydantic import BaseModel, Field, field_validator, ValidationError

class UserRegistration(BaseModel):
    # TODO: Define username with length constraint 3..20
    # TODO: Define age with ge=18 constraint
    # TODO: Define email as str
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=18)
    email: str
    

    # TODO: Add a @field_validator for 'email'
    # Check if '@' is in value and if it ends with '.com' or '.org'
    # Raise ValueError if invalid.
    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str) -> str:
        if "@" not in value or not (value.endswith(".com") or value.endswith(".org")):
            raise ValueError("Email must contain '@' and end with '.com' or '.org'")
        return value
    

def run_user_checks():
    invalid_payload = {
        "username": "al",
        "age": 16,
        "email": "invalid_email.net"
    }
    # TODO: Try creating UserRegistration and handle ValidationError
    try:
        UserRegistration(**invalid_payload)
    except ValidationError as e:
        print("Validation errors caught correctly:\n", e)

if __name__ == "__main__":
    run_user_checks()