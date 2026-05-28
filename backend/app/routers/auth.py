"""Auth routers - authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.utils.jwt import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from app.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Login endpoint"""
    user = await db.scalar(
        select(User).where(User.username == username)
    )
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(token: str = None, db: AsyncSession = Depends(get_db)):
    """Get current user info"""
    if not token:
        raise HTTPException(401, "Not authenticated")
    # Token validation logic here
    return {"user": "current_user"}
