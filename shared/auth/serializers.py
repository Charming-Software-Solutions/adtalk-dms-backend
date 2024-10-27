from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super(LoginSerializer, cls).get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({"user": str(self.user.id)})
        return data
