from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.db.models import User, XAccount
from app.auth.admin_dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# Response Models
class UserListResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    is_admin: bool
    is_active: bool
    created_at: str
    x_accounts_count: int
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    admin_users: int
    total_x_accounts: int
    users_created_today: int


class UpdateUserRequest(BaseModel):
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    name: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
    success: bool


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """الحصول على إحصائيات لوحة التحكم - Get dashboard statistics"""
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = db.query(User).filter(User.is_active == False).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()
    total_x_accounts = db.query(XAccount).count()
    
    # Users created today
    today = datetime.utcnow().date()
    users_created_today = db.query(User).filter(
        func.date(User.created_at) == today
    ).count()
    
    return DashboardStats(
        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        admin_users=admin_users,
        total_x_accounts=total_x_accounts,
        users_created_today=users_created_today
    )


@router.get("/users", response_model=List[UserListResponse])
async def get_all_users(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """الحصول على قائمة المستخدمين - Get all users"""
    
    users = db.query(User).offset(skip).limit(limit).all()
    
    result = []
    for user in users:
        result.append(UserListResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            profile_picture=user.profile_picture,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            x_accounts_count=len(user.x_accounts)
        ))
    
    return result


@router.get("/users/{user_id}", response_model=UserListResponse)
async def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """الحصول على معلومات مستخدم محدد - Get user by ID"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserListResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_picture=user.profile_picture,
        is_admin=user.is_admin,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
        x_accounts_count=len(user.x_accounts)
    )


@router.put("/users/{user_id}", response_model=UserListResponse)
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """تحديث معلومات مستخدم - Update user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deactivating themselves
    if user.id == admin_user.id and request.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Update fields
    if request.is_admin is not None:
        user.is_admin = request.is_admin
    if request.is_active is not None:
        user.is_active = request.is_active
    if request.name is not None:
        user.name = request.name
    
    db.commit()
    db.refresh(user)
    
    return UserListResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        profile_picture=user.profile_picture,
        is_admin=user.is_admin,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
        x_accounts_count=len(user.x_accounts)
    )


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """حذف مستخدم - Delete user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return MessageResponse(
        message=f"User {user.email} deleted successfully",
        success=True
    )


@router.get("/x-accounts", response_model=List[dict])
async def get_all_x_accounts(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """الحصول على جميع حسابات X - Get all X accounts"""
    
    accounts = db.query(XAccount).offset(skip).limit(limit).all()
    
    result = []
    for account in accounts:
        result.append({
            "id": account.id,
            "user_id": account.user_id,
            "user_email": account.user.email if account.user else None,
            "username": account.username,
            "status": account.status,
            "created_at": account.created_at.isoformat(),
            "updated_at": account.updated_at.isoformat()
        })
    
    return result
