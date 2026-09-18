# TODO: Define a UserRepositoryProtocol using typing.Protocol with get_by_email and save methods
from typing import Protocol, Optional
from app.domain.models import User

class UserRepositoryProtocol(Protocol):
    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by email address."""
        ...

    async def save(self, user: User) -> User:
        """Persist a user entity and return the updated entity with ID."""
        ...