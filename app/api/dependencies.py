from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.connection import get_db_session
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.user.service import AuthService
from app.application.services.user_service import UserService
from app.infrastructure.security.password import PasswordManager
from app.infrastructure.security.auth import JWTManager


security = HTTPBearer()


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


def get_password_manager() -> PasswordManager:
    return PasswordManager()


def get_jwt_manager() -> JWTManager:
    return JWTManager()


def get_auth_service(
    password_manager: PasswordManager = Depends(get_password_manager)
) -> AuthService:
    return AuthService(password_manager)


async def get_user_service(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> UserService:
    return UserService(user_repository, auth_service, jwt_manager)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
    user_repository: UserRepositoryImpl = Depends(get_user_repository)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = jwt_manager.decode_access_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = await user_repository.get_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user