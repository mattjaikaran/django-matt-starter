"""Pytest configuration and fixtures."""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    """Create a test client."""
    return Client()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="adminpass123",
    )
