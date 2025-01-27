from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from employee.models import Employee
from users.models import CustomUser

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super(LoginSerializer, cls).get_token(user)
        token["role"] = user.role
        token["id"] = str(user.id)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {
                "user": {
                    "id": str(self.user.id),
                    "role": self.user.role,
                }
            }
        )

        try:
            employee = Employee.objects.get(user=self.user)
            data["employee"] = {
                "id": str(employee.id),
                "name": f"{employee.first_name} {employee.last_name}",
                "profile_image": (
                    employee.profile_image.url if employee.profile_image else None
                ),
            }
        except Employee.DoesNotExist:
            data["employee"] = None

        return data


class ChangeEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password")
        read_only_fields = ("id", "password")

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError(
                {"password": "Current password is not correct"}
            )

        if CustomUser.objects.exclude(id=user.id).filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "This email is already in use"})

        return attrs

    def update(self, instance, validated_data):
        if instance != self.context["request"].user:
            raise serializers.ValidationError("You can only update your own email")

        instance.email = validated_data["email"]
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("new_password", "confirm_password", "current_password")

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is not correct.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
