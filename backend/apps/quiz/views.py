from rest_framework import viewsets, permissions
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# 관리자만 접근 가능한 Quiz ViewSet
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def add_questions(self, request, pk=None):
        quiz = self.get_object()
        questions_data = request.data.get('questions', [])
        
        for question_data in questions_data:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data['text'],
            )
            for choice_data in question_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )
        return Response({"message": "Questions added successfully"})
    
    
# 문제 ViewSet
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

# 선택지 ViewSet
class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]
