# Generated by Django 5.1.7 on 2025-03-15 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="choice",
            table="choices",
        ),
        migrations.AlterModelTable(
            name="question",
            table="questions",
        ),
        migrations.AlterModelTable(
            name="quiz",
            table="quizzes",
        ),
        migrations.AlterModelTable(
            name="userquizresponse",
            table="user_quiz_responses",
        ),
    ]
