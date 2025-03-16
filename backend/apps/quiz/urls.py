from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, ChoiceViewSet

# DRF Router를 사용하여 뷰셋을 자동으로 URL에 연결
router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')

urlpatterns = [
    path('api/', include(router.urls)),  # /api/ 에 모든 뷰셋 URL을 연결
]
