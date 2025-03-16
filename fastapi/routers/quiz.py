from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
import random
import time
import redis
from models import Quiz, Question, Choice, UserQuizResponse, User
from database import get_db
from dependencies import get_current_user  # JWT 인증을 위한 의존성
import json

router = APIRouter()

# Redis 클라이언트
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# 관리자 권한 체크를 위한 의존성
def check_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    return user

@router.post("/quizzes/")
async def create_quiz(
    title: str, 
    description: str, 
    question_ids: list,  # 퀴즈에 포함될 문제 목록
    current_user: User = Depends(check_admin),  # 관리자만 퀴즈 생성 가능
    db: AsyncSession = Depends(get_db)
):
    quiz = Quiz(title=title, description=description)
    db.add(quiz)
    await db.commit()
    
    for question_id in question_ids:
        question = await db.execute(select(Question).filter(Question.id == question_id))
        question = question.scalar_one_or_none()
        if question:
            quiz.questions.append(question)
    
    await db.commit()
    return {"message": "Quiz created successfully"}

@router.get("/quizzes/")
async def get_quizzes(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    result = await db.execute(select(Quiz).offset(offset).limit(page_size))
    quizzes = result.scalars().all()

    # 사용자가 응시한 퀴즈 목록 가져오기
    user_attempts = await db.execute(
        select(UserQuizResponse.quiz_id)
        .filter(UserQuizResponse.user_id == user_id)
        .distinct()
    )
    attempted_quizzes = {attempt.quiz_id for attempt in user_attempts.scalars().all()}

    total_count = await db.execute(select(Quiz).count())
    total_pages = (total_count.scalar_one() + page_size - 1) // page_size

    return {
        "quizzes": [
            {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "attempted": quiz.id in attempted_quizzes,
            }
            for quiz in quizzes
        ],
        "page": page,
        "total_pages": total_pages,
    }


@router.get("/quiz/{quiz_id}/questions/")
async def get_quiz_questions(
    quiz_id: int, 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1), 
    user_id: int = Query(...),  # 사용자 ID 추가
    db: AsyncSession = Depends(get_db),
):
    quiz_query = await db.execute(select(Quiz).filter(Quiz.id == quiz_id))
    quiz = quiz_query.scalar_one_or_none()
    if not quiz:
        return {"error": "Quiz not found"}

    # Redis를 사용하여 문제 순서를 세션별로 유지
    redis_key = f"user:{user_id}:quiz:{quiz_id}:state"
    stored_state = redis_client.get(redis_key)

    if stored_state:
        # Redis에 저장된 순서를 사용
        questions_order = json.loads(stored_state)
    else:
        # Redis에 저장된 순서가 없으면 DB에서 문제들을 가져와 랜덤화
        questions_query = await db.execute(select(Question).filter(Question.quiz_id == quiz_id).offset((page-1) * page_size).limit(page_size))
        questions = questions_query.scalars().all()
        questions_order = [q.id for q in questions]
        # 랜덤화된 문제 순서를 Redis에 저장 (1시간 동안 캐시)
        redis_client.set(redis_key, json.dumps(questions_order), ex=3600)

    # 문제와 선택지 가져오기
    result = []
    for question_id in questions_order:
        question_query = await db.execute(select(Question).filter(Question.id == question_id))
        question = question_query.scalar_one_or_none()
        if not question:
            continue
        
        choices_query = await db.execute(select(Choice).filter(Choice.question_id == question.id))
        choices = choices_query.scalars().all()

        # 선택지 랜덤화
        if quiz.randomize_choices:
            random.shuffle(choices)

        result.append(
            {
                "id": question.id,
                "text": question.text,
                "choices": [{"id": c.id, "text": c.text} for c in choices],
            }
        )

    # 페이징 처리
    total_questions = await db.execute(select(Question).filter(Question.quiz_id == quiz_id).count())
    total_pages = (total_questions.scalar_one() + page_size - 1) // page_size

    return {
        "questions": result,
        "page": page,
        "total_pages": total_pages,
    }


@router.post("/quizzes/")
async def create_quiz(
    title: str, 
    description: str, 
    question_ids: list,  # 퀴즈에 포함될 문제 목록
    current_user: User = Depends(check_admin),  # 관리자만 퀴즈 생성 가능
    db: AsyncSession = Depends(get_db)
):
    quiz = Quiz(title=title, description=description)
    db.add(quiz)
    await db.commit()
    
    for question_id in question_ids:
        question = await db.execute(select(Question).filter(Question.id == question_id))
        question = question.scalar_one_or_none()
        if question:
            quiz.questions.append(question)
    
    await db.commit()
    return {"message": "Quiz created successfully"}


@router.post("/submit_quiz/")
async def submit_quiz(
    quiz_id: int, 
    answers: dict, 
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    redis_key = f"user:{user_id}:quiz:{quiz_id}:state"
    stored_state = redis_client.get(redis_key)

    if stored_state:
        questions_order = json.loads(stored_state)
    else:
        questions_query = await db.execute(select(Question).filter(Question.quiz_id == quiz_id))
        questions = questions_query.scalars().all()
        questions_order = [q.id for q in questions]
        redis_client.set(redis_key, json.dumps(questions_order), ex=3600)

    correct_count = 0
    for question_id in questions_order:
        user_answer = int(answers.get(str(question_id), -1))
        correct_choice_query = await db.execute(
            select(Choice).filter(Choice.question_id == question_id, Choice.is_correct == True)
        )
        correct_choice = correct_choice_query.scalar_one_or_none()
        if correct_choice and user_answer == correct_choice.id:
            correct_count += 1

        response = UserQuizResponse(
            user_id=user_id,
            quiz_id=quiz_id,
            question_id=question_id,
            selected_choice_id=user_answer,
            is_correct=(user_answer == correct_choice.id)
        )
        db.add(response)

    await db.commit()
    score = (correct_count / len(questions_order)) * 100
    redis_client.set(f"user:{user_id}:quiz:{quiz_id}:attempt:{int(time.time())}", score, ex=3600)

    return {"score": score}
