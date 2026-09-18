# TODO: Implement PostgresUserRepository which implements UserRepositoryProtocol
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models import User as DomainUser
from app.infrastructure.models import UserORM

class PostgresUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        
        if not orm_user:
            return None
            
        # Map ORM -> Domain Entity
        return DomainUser(
            id=orm_user.id,
            email=orm_user.email,
            hashed_password=orm_user.hashed_password,
            is_active=orm_user.is_active,
        )

    async def save(self, user: DomainUser) -> DomainUser:
        orm_user = UserORM(
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
        )
        self.session.add(orm_user)
        # flush() sends SQL to DB to obtain auto-generated ID without committing transaction
        await self.session.flush()
        
        user.id = orm_user.id
        return user