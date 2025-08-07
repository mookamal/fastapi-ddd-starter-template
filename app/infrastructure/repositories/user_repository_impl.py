from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.user.entity import User
from app.domain.user.repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            created_at=entity.created_at
        )
    
    async def create(self, user: User) -> User:
        user_model = self._entity_to_model(user)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return self._model_to_entity(user_model)
    
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return self._model_to_entity(user_model) if user_model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._model_to_entity(user_model) if user_model else None
    
    async def update(self, user: User) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one()
        
        user_model.name = user.name
        user_model.email = user.email
        user_model.password_hash = user.password_hash
        user_model.is_active = user.is_active
        
        await self.session.commit()
        await self.session.refresh(user_model)
        return self._model_to_entity(user_model)
    
    async def delete(self, user_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            await self.session.delete(user_model)
            await self.session.commit()
            return True
        return False
    
    async def list_all(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        user_models = result.scalars().all()
        return [self._model_to_entity(model) for model in user_models]