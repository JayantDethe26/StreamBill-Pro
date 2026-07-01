from fastapi import APIRouter
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    UserRegister,
    UserResponse,
    LoginRequest,
    TokenResponse
)
from app.services.auth_service import (
    create_user,
    authenticate_user
)

from app.dependencies import get_current_user
from app.models.user import User



@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
async def register(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await create_user(
            payload,
            db
        )

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    token = await authenticate_user(
        payload.email,
        payload.password,
        db
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.get(
    "/me",
    response_model=UserResponse
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user