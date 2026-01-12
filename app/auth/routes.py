from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from typing import Optional

from app.db.database import get_db
from app.db.models import User
from app.db.redis_client import RedisClient
from app.auth.security import (
    verify_password, 
    hash_password, 
    create_access_token, 
    decode_token,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.auth.dependencies import require_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()


# Request/Response Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str
    
    class Config:
        from_attributes = True


class VerifyResponse(BaseModel):
    valid: bool
    user: Optional[UserResponse] = None


class MessageResponse(BaseModel):
    message: str
    success: bool


@router.post("/register", response_model=Token)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(request.password)
    new_user = User(
        email=request.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """تسجيل دخول - Login user and return JWT token"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Store session in Redis (optional - won't block if Redis is unavailable)
    try:
        RedisClient.set_session(access_token[:32], user.id)
    except Exception as e:
        # Redis is optional, continue without it
        pass
    
    return Token(access_token=access_token)


@router.get("/verify", response_model=VerifyResponse)
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """التحقق من Token - Verify if JWT token is valid"""
    
    token = credentials.credentials
    
    # Check if token is blacklisted (optional - skip if Redis unavailable)
    try:
        if RedisClient.is_blacklisted(token):
            return VerifyResponse(valid=False)
    except Exception:
        # Redis is optional, continue without it
        pass
    
    # Decode token
    token_data = decode_token(token)
    if token_data is None:
        return VerifyResponse(valid=False)
    
    # Get user from database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        return VerifyResponse(valid=False)
    
    return VerifyResponse(
        valid=True,
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at.isoformat()
        )
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(require_current_user)
):
    """تسجيل خروج - Logout user and invalidate token"""
    
    token = credentials.credentials
    
    # Add token to blacklist (optional - skip if Redis unavailable)
    try:
        RedisClient.add_to_blacklist(token)
        RedisClient.delete_session(token[:32])
    except Exception:
        # Redis is optional, continue without it
        pass
    
    return MessageResponse(
        message="Successfully logged out",
        success=True
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(require_current_user)):
    """Get current authenticated user info"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at.isoformat()
    )
