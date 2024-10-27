from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super(LoginSerializer, cls).get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        token["id"] = str(user.id)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {
                "user": {
                    "id": str(self.user.id),
                    "email": self.user.email,
                    "role": self.user.role,
                }
            }
        )
        return data
