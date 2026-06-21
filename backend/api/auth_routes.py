from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.database import get_db
from core.security import create_access_token
from core.deps import get_current_user
from models.user import User
from services.auth_service import (
    get_user_by_email,
    create_user,
    authenticate_user
)

from schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        payload.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = create_user(
        db,
        payload.name,
        payload.email,
        payload.password
    )

    return {
        "message": "User registered",
        "user_id": user.id
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        payload.email,
        payload.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }