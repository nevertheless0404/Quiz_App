from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    username: str
    email: str
    is_admin: bool  # 관리자 권한 여부
    
# Quiz Schema
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    total_questions: int
    randomize_questions: Optional[bool] = True
    randomize_choices: Optional[bool] = False

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int
    questions: List["Question"] = []

    class Config:
        orm_mode = True


# Question Schema
class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    quiz_id: int
    choices: List["Choice"] = []

    class Config:
        orm_mode = True


# Choice Schema
class ChoiceBase(BaseModel):
    text: str
    is_correct: Optional[bool] = False

class ChoiceCreate(ChoiceBase):
    pass

class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


# UserQuizResponse Schema
class UserQuizResponseBase(BaseModel):
    user_id: int
    quiz_id: int
    question_id: int
    selected_choice_id: int
    is_correct: bool

class UserQuizResponseCreate(UserQuizResponseBase):
    pass

class UserQuizResponse(UserQuizResponseBase):
    id: int

    class Config:
        orm_mode = True
