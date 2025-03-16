from fastapi import FastAPI
from routers import quiz

app = FastAPI()

# 루트 경로 추가 (기본 페이지 처리)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Quiz API"}

# quiz 라우터 포함 (API prefix 추가)
app.include_router(quiz.router, prefix="/api")
