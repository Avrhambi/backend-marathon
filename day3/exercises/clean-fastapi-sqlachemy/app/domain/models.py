# TODO: Define a User dataclass with id, email, hashed_password, and is_active
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    hashed_password: str
    id: Optional[int] = None
    is_active: bool = True
