"""Authentication Service"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from datetime import datetime
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""

    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_create.email) | (User.username == user_create.username)
        ).first()
        
        if existing_user:
            logger.warning(f"User registration failed: email or username already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create new user
        user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hash_password(user_create.password),
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User registered successfully: {user.email}")
        return user

    @staticmethod
    def authenticate_user(db: Session, login_request: LoginRequest) -> User:
        """Authenticate user and return user object"""
        # Find user by email
        user = db.query(User).filter(User.email == login_request.email).first()
        
        if not user:
            logger.warning(f"Login attempt with non-existent email: {login_request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is locked due to failed attempts
        if user.locked_until and user.locked_until > datetime.utcnow():
            logger.warning(f"Login attempt on locked account: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is locked. Please try again later."
            )
        
        # Verify password
        if not verify_password(login_request.password, user.hashed_password):
            # Increment failed login attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                from datetime import timedelta
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
                logger.warning(f"Account locked due to failed login attempts: {user.email}")
            
            db.commit()
            logger.warning(f"Login failed for user: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt on inactive account: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled"
            )
        
        # Reset failed login attempts
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info(f"User authenticated successfully: {user.email}")
        return user

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """Get current user from token"""
        payload = decode_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user

    @staticmethod
    def change_password(db: Session, user: User, old_password: str, new_password: str) -> User:
        """Change user password"""
        if not verify_password(old_password, user.hashed_password):
            logger.warning(f"Password change failed for user: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        logger.info(f"Password changed successfully for user: {user.email}")
        return user
