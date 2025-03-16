from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, validates
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255)) 

class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    total_questions = Column(Integer, nullable=False, default=10)
    randomize_questions = Column(Boolean, default=True)
    randomize_choices = Column(Boolean, default=False)

    questions = relationship("Question", back_populates="quiz")

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))

    quiz = relationship("Quiz", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")

    @validates("choices")
    def validate_correct_choice(self, key, choice):
        correct_choices = [c for c in self.choices if c.is_correct]
        if len(correct_choices) > 1:
            raise ValueError("Each question must have exactly one correct choice.")
        if len(self.choices) < 3:
            raise ValueError("Each question must have at least 3 choices.")
        return choice

class Choice(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship("Question", back_populates="choices")


class UserQuizResponse(Base):
    __tablename__ = 'user_quiz_responses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    selected_choice_id = Column(Integer, ForeignKey('choices.id'))
    is_correct = Column(Boolean)

    quiz = relationship("Quiz")
    question = relationship("Question")
    selected_choice = relationship("Choice")
