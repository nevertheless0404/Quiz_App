from rest_framework import serializers
from .models import Quiz, Question, Choice, UserQuizResponse

# Quiz 시리얼라이저
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'randomize_questions', 'randomize_choices', 'total_questions']

# Question 시리얼라이저
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'quiz_id']

# Choice 시리얼라이저
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'question_id']

# UserQuizResponse 시리얼라이저
class UserQuizResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizResponse
        fields = ['id', 'user_id', 'quiz_id']
