from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from employee.models import Employee


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super(LoginSerializer, cls).get_token(user)
        token["user"] = str(user.id)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({"user": str(self.user.id)})

        try:
            employee = Employee.objects.get(user=self.user)
            data["employee"] = {
                "id": str(employee.id),
                "name": employee.name,
                "profile_image": (
                    employee.profile_image.url if employee.profile_image else None
                ),
            }
        except Employee.DoesNotExist:
            data["employee"] = None

        return data
