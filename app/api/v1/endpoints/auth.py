from fastapi import APIRouter, Depends, HTTPException, status
from app.application.services.user_service import UserService
from app.application.dtos.user_dto import UserCreateRequest, UserResponse, LoginRequest, TokenResponse
from app.api.dependencies import get_user_service, get_current_user
from app.domain.user.entity import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserCreateRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.register_user(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.login_user(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return UserResponse.model_validate(current_user)