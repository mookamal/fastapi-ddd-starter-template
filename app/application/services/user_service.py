from typing import Optional
import uuid
from app.domain.user.entity import User
from app.domain.user.repository import UserRepository
from app.domain.user.service import AuthService
from app.application.dtos.user_dto import UserCreateRequest, UserResponse, LoginRequest, TokenResponse
from app.infrastructure.security.auth import JWTManager


class UserService:
    def __init__(
        self, 
        user_repository: UserRepository, 
        auth_service: AuthService,
        jwt_manager: JWTManager
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.jwt_manager = jwt_manager
    
    async def register_user(self, request: UserCreateRequest) -> UserResponse:
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create user using domain service
        user = self.auth_service.create_user(
            name=request.name,
            email=request.email,
            password=request.password
        )
        
        # Save user
        created_user = await self.user_repository.create(user)
        
        return UserResponse.model_validate(created_user)
    
    async def login_user(self, request: LoginRequest) -> TokenResponse:
        # Get user by email
        user = await self.user_repository.get_by_email(request.email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Verify password
        if not self.auth_service.verify_password(user, request.password):
            raise ValueError("Invalid credentials")
        
        # Generate JWT token
        access_token = self.jwt_manager.create_access_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )
        
        return TokenResponse(access_token=access_token)
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserResponse]:
        user = await self.user_repository.get_by_id(user_id)
        if user:
            return UserResponse.model_validate(user)
        return None