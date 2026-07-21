"""Tests for Authentication Service"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest
from app.services.auth import AuthService
from app.utils.security import verify_password
from app.utils.database import SessionLocal

client = TestClient(app)


@pytest.fixture
def db():
    """Database session fixture"""
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db: Session):
    """Create a test user"""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="TestPassword123"
    )
    user = AuthService.register_user(db, user_data)
    return user


class TestUserRegistration:
    """Test user registration"""
    
    def test_register_user_success(self, db: Session):
        """Test successful user registration"""
        user_data = UserCreate(
            email="newuser@example.com",
            username="newuser",
            full_name="New User",
            password="SecurePassword123"
        )
        
        user = AuthService.register_user(db, user_data)
        
        assert user.email == user_data.email
        assert user.username == user_data.username
        assert user.full_name == user_data.full_name
        assert verify_password(user_data.password, user.hashed_password)
    
    def test_register_duplicate_email(self, db: Session, test_user: User):
        """Test registering with duplicate email"""
        user_data = UserCreate(
            email=test_user.email,
            username="otheruser",
            full_name="Other User",
            password="SecurePassword123"
        )
        
        with pytest.raises(Exception):
            AuthService.register_user(db, user_data)
    
    def test_register_duplicate_username(self, db: Session, test_user: User):
        """Test registering with duplicate username"""
        user_data = UserCreate(
            email="other@example.com",
            username=test_user.username,
            full_name="Other User",
            password="SecurePassword123"
        )
        
        with pytest.raises(Exception):
            AuthService.register_user(db, user_data)


class TestUserAuthentication:
    """Test user authentication"""
    
    def test_authenticate_user_success(self, db: Session, test_user: User):
        """Test successful authentication"""
        login_request = LoginRequest(
            email=test_user.email,
            password="TestPassword123"
        )
        
        user = AuthService.authenticate_user(db, login_request)
        
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    def test_authenticate_invalid_email(self, db: Session):
        """Test authentication with invalid email"""
        login_request = LoginRequest(
            email="nonexistent@example.com",
            password="SomePassword123"
        )
        
        with pytest.raises(Exception):
            AuthService.authenticate_user(db, login_request)
    
    def test_authenticate_invalid_password(self, db: Session, test_user: User):
        """Test authentication with invalid password"""
        login_request = LoginRequest(
            email=test_user.email,
            password="WrongPassword123"
        )
        
        with pytest.raises(Exception):
            AuthService.authenticate_user(db, login_request)


class TestChangePassword:
    """Test password change functionality"""
    
    def test_change_password_success(self, db: Session, test_user: User):
        """Test successful password change"""
        new_password = "NewPassword123"
        
        user = AuthService.change_password(
            db,
            test_user,
            "TestPassword123",
            new_password
        )
        
        assert verify_password(new_password, user.hashed_password)
    
    def test_change_password_wrong_current(self, db: Session, test_user: User):
        """Test password change with wrong current password"""
        with pytest.raises(Exception):
            AuthService.change_password(
                db,
                test_user,
                "WrongPassword",
                "NewPassword123"
            )


class TestAuthenticationEndpoints:
    """Test authentication API endpoints"""
    
    def test_register_endpoint(self):
        """Test /register endpoint"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "endpoint_test@example.com",
                "username": "endpointtest",
                "full_name": "Endpoint Test",
                "password": "TestPassword123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "endpoint_test@example.com"
    
    def test_login_endpoint(self):
        """Test /login endpoint"""
        # First register
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login_test@example.com",
                "username": "logintest",
                "full_name": "Login Test",
                "password": "TestPassword123"
            }
        )
        
        # Then login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login_test@example.com",
                "password": "TestPassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
