from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db import get_db_session
from app.infrastructure.repositories import PostgresUserRepository
from app.application.use_cases import GetUserByEmailUseCase, RegisterUserUseCase

def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> PostgresUserRepository:
    return PostgresUserRepository(session)

def get_register_use_case(
    repo: PostgresUserRepository = Depends(get_user_repository),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo=repo)

def get_by_email_use_case(
    repo: PostgresUserRepository = Depends(get_user_repository),
) -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase(user_repo=repo)