# TODO: Implement RegisterUserUseCase receiving UserRepositoryProtocol
# TODO: Raise ValueError if user email already exists
import hashlib
from app.domain.models import User
from app.domain.repositories import UserRepositoryProtocol

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo

    async def execute(self, email: str, raw_password: str) -> User:
        # 1. Check if user already exists
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists.")

        # 2. Hash password (simple SHA-256 for demo purposes)
        hashed_pw = hashlib.sha256(raw_password.encode()).hexdigest()

        # 3. Create domain entity
        new_user = User(email=email, hashed_password=hashed_pw)

        # 4. Save via repository protocol
        return await self.user_repo.save(new_user)

class GetUserByEmailUseCase:
    def __init__(self, user_repo: UserRepositoryProtocol):
        self.user_repo = user_repo

    async def execute(self, email: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError(f"User with email '{email}' not found.")
        return user