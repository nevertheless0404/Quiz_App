# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# 사용자 가입 시 사용하는 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')  # 필요한 필드만
        extra_kwargs = {'password': {'write_only': True}}  # 비밀번호는 write_only로 설정

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # 비밀번호 해싱 처리
        return user

# JWT 토큰 발급 시 사용하는 시리얼라이저
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 토큰에 사용자 정보 추가
        token['username'] = user.username
        token['email'] = user.email
        return token
