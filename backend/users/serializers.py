# users/serializers.py

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Read-only representation of a user (for /me and other endpoints).
    """
    institution_name = serializers.CharField(
        source="institution.name", read_only=True
    )
    class_group_name = serializers.CharField(
        source="class_group.name", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "institution",
            "institution_name",
            "class_group",
            "class_group_name",
            "wallet_address",
            "mobile_number",
            "profile_image",
            "gender",
            "date_of_birth",
            "bio",
        ]
        read_only_fields = [
            "id",
            "role",          # if you want only admins to change role
            "wallet_address" # or allow later with a separate endpoint
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration serializer. Creates a new user with password.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "role",
            "institution",
            "class_group",
            "mobile_number",
        ]
        extra_kwargs = {
            "role": {"required": False},
            "institution": {"required": False},
            "class_group": {"required": False},
            "email": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2", None)

        # default role to student if not provided
        if "role" not in validated_data or not validated_data["role"]:
            validated_data["role"] = "student"

        user = User.objects.create_user(
            **validated_data,
            password=password,
        )
        return user
