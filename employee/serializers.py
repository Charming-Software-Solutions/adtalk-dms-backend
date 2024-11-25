import json

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers

from employee.models import Employee
from shared.utils.email import send_resend_email
from users.serializers import CustomUserSerializer

User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"

    def validate(self, attrs):
        # Ensure the `email` is not included in user data during update
        if self.instance and "user" in attrs:
            user_data = attrs.get("user", {})
            user_data.pop("email", None)
        return attrs

    def to_internal_value(self, data):
        if hasattr(data, "dict"):
            data = data.dict()

        if "user" in data and isinstance(data["user"], str):
            try:
                user_data = json.loads(data["user"])
                # Remove email if this is an update operation
                if self.instance:
                    user_data.pop("email", None)
                data["user"] = user_data
            except json.JSONDecodeError:
                raise serializers.ValidationError({"user": "Invalid JSON data"})
        return super().to_internal_value(data)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        original_password = user_data.get("password", get_random_string(length=8))
        user_data["password"] = original_password
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)

        send_resend_email(
            subject="Your Account Credentials",
            recipient=user.email,
            html=f"""
            <p>Hello,</p>
            <p>Your account has been created. Here are your login credentials:</p>
            <p>Email: <strong>{user.email}</strong></p>
            <p>Temporary Password: <strong>{original_password}</strong></p>
            <p>Please change your password upon first login.</p>
            """,
        )
        return employee

    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_data.pop("email", None)

            # Update only non-email user fields
            for attr, value in user_data.items():
                if attr != "email":
                    setattr(instance.user, attr, value)
            instance.user.save()

        # Update employee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class UpdateEmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ("id", "user")

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        if instance.user != request_user:
            raise serializers.ValidationError("You can only update your own profile")

        if "profile_image" in validated_data:
            instance.profile_image = validated_data["profile_image"]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
