"""API Integration Tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operational"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_database_health_endpoint(self):
        """Test database health check"""
        response = client.get("/health/db")
        # Status might be healthy or unhealthy depending on DB setup
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestAuthenticationFlow:
    """Test complete authentication flow"""
    
    def test_full_auth_flow(self):
        """Test registration, login, and profile access"""
        # Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "flow_test@example.com",
                "username": "flowtest",
                "full_name": "Flow Test User",
                "password": "FlowTestPassword123"
            }
        )
        assert register_response.status_code == 201
        
        # Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "flow_test@example.com",
                "password": "FlowTestPassword123"
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        token = login_data["access_token"]
        
        # Get profile
        profile_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["email"] == "flow_test@example.com"
