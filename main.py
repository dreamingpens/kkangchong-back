from fastapi import Depends, FastAPI, HTTPException, Query
from models import Base
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
import crud
from fastapi.middleware.cors import CORSMiddleware  # 이 줄을 추가
from routers.kkangchong_back import llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/club/{subject}", response_model=list[schemas.Club])
def read_club(subject: str, db: Session=Depends(get_db)):
    print(subject)
    club=crud.get_clubs(db, subject)
    
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return club

app.include_router(llm.router)