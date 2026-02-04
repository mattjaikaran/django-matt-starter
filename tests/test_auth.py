"""Tests for authentication endpoints."""

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_protected_endpoint_unauthenticated(self, client):
        """Test protected endpoint when not authenticated."""
        response = client.get("/api/protected")
        assert response.status_code == 401

    def test_me_unauthenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_register(self, client):
        """Test user registration."""
        response = client.post(
            "/api/auth/register",
            data={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "securepass123",
            },
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
