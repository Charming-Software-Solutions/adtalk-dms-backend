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
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
        }
        read_only_fields = ("last_login",)

    def create(self, validated_data):
        email = validated_data.get("email")
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        role = validated_data.get("role")
        if not role:
            raise serializers.ValidationError({"role": "This field is required."})

        user = CustomUser.objects.create_user(
            email=email,
            password=validated_data.get("password"),
            role=role,
        )

        user.is_active = validated_data.get("is_active", True)
        user.is_staff = validated_data.get("is_staff", False)

        user.save()
        return user

    def update(self, instance, validated_data):
        # Prevent email from being updated
        if "email" in validated_data:
            validated_data.pop("email")

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
