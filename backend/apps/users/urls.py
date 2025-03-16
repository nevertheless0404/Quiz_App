# apps/users/urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 회원가입
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 (JWT 토큰 발급)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 리프레시
]
