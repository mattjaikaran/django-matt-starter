"""Authentication controller."""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django_matt.auth import create_token_pair, jwt_required, refresh_tokens
from django_matt.core import APIController
from django_matt.core.errors import APIError, ValidationAPIError

from ..schemas import (
    ChangePasswordSchema,
    LoginSchema,
    RefreshTokenSchema,
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
)

User = get_user_model()


class AuthController(APIController):
    """Authentication controller."""

    tags = ["Auth"]

    @staticmethod
    async def register(request, body: dict) -> dict:
        """Register a new user."""
        data = UserCreateSchema(**body)
        # Check if email exists
        if await User.objects.filter(email=data.email).aexists():
            raise ValidationAPIError("Email already registered")

        # Check if username exists
        if await User.objects.filter(username=data.username).aexists():
            raise ValidationAPIError("Username already taken")

        # Create user
        user = await User.objects.acreate(
            email=data.email,
            username=data.username,
            password=make_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
        )

        return UserSchema.model_validate(user).model_dump(mode="json")

    @staticmethod
    async def login(request, body: dict) -> dict:
        """Login and get tokens."""
        data = LoginSchema(**body)
        try:
            user = await User.objects.aget(email=data.email)
        except User.DoesNotExist:
            raise APIError(status_code=401, message="Invalid credentials")

        if not check_password(data.password, user.password):
            raise APIError(status_code=401, message="Invalid credentials")

        if not user.is_active:
            raise APIError(status_code=401, message="Account is disabled")

        tokens = create_token_pair(user)
        return {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def refresh(request, body: dict) -> dict:
        """Refresh access token."""
        data = RefreshTokenSchema(**body)
        try:
            tokens = refresh_tokens(data.refresh_token)
            return {
                "access_token": tokens.access_token,
                "refresh_token": tokens.refresh_token,
                "token_type": "bearer",
            }
        except Exception as e:
            raise APIError(status_code=401, message=str(e))

    @staticmethod
    @jwt_required
    async def me(request) -> dict:
        """Get current user profile."""
        return UserSchema.model_validate(request.user).model_dump(mode="json")

    @staticmethod
    @jwt_required
    async def update_me(request, body: dict) -> dict:
        """Update current user profile."""
        data = UserUpdateSchema(**body)
        user = request.user
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        await user.asave()
        return UserSchema.model_validate(user).model_dump(mode="json")

    @staticmethod
    @jwt_required
    async def change_password(request, body: dict) -> dict:
        """Change password."""
        data = ChangePasswordSchema(**body)
        user = request.user

        if not check_password(data.current_password, user.password):
            raise ValidationAPIError("Current password is incorrect")

        user.password = make_password(data.new_password)
        await user.asave()

        return {"message": "Password changed successfully"}
