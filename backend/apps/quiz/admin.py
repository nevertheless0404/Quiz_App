# admin.py
from django.contrib import admin
from .models import Quiz, Question, Choice  # 모델 임포트

# 모델을 관리자 페이지에 등록
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)