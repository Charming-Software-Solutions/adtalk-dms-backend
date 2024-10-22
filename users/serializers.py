from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "is_active",
            "is_staff",
            "role",
            "password",
            "last_login",
        )  # Add last_login here
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("last_login",)  # Ensure last_login is read-only

    def create(self, validated_data):
        # Ensure 'role' is provided in the validated data
        role = validated_data.get("role")
        if not role:
            raise serializers.ValidationError({"role": "This field is required."})

        # Use the create_user method of CustomUserManager
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=role,
        )

        # Set other fields
        user.is_active = validated_data.get("is_active", True)
        user.is_staff = validated_data.get("is_staff", False)

        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password updates
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
