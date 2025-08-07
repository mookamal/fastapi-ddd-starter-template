from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from app.domain.user.entity import User


class UserRepository(ABC):
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        pass
    
    @abstractmethod
    async def list_all(self) -> List[User]:
        pass