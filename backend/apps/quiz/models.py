from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    randomize_questions = models.BooleanField(default=False)
    randomize_choices = models.BooleanField(default=False)
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quizzes'  # 테이블 이름 설정


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = 'questions'  # 테이블 이름 설정


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'choices'  # 테이블 이름 설정


class UserQuizResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.JSONField()

    class Meta:
        db_table = 'user_quiz_responses'  # 테이블 이름 설정
