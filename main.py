from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from databases import Database
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./test_management.db"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String)

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    text = Column(String)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    text = Column(String)
    is_correct = Column(Boolean, default=False)

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    score = Column(Float)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True

class TestCreate(BaseModel):
    title: str
    description: str

class TestRead(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    test_id: int
    text: str

class QuestionRead(BaseModel):
    id: int
    test_id: int
    text: str

    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    text: str
    is_correct: bool

class AnswerRead(BaseModel):
    id: int
    question_id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True

class ResultCreate(BaseModel):
    user_id: int
    test_id: int
    score: float

class ResultRead(BaseModel):
    id: int
    user_id: int
    test_id: int
    score: float

    class Config:
        from_attributes = True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password), is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/tests/", response_model=TestRead)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    db_test = Test(title=test.title, description=test.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@app.post("/questions/", response_model=QuestionRead)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(test_id=question.test_id, text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.post("/answers/", response_model=AnswerRead)
def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    db_answer = Answer(question_id=answer.question_id, text=answer.text, is_correct=answer.is_correct)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

@app.post("/results/", response_model=ResultRead)
def create_result(result: ResultCreate, db: Session = Depends(get_db)):
    db_result = Result(user_id=result.user_id, test_id=result.test_id, score=result.score)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
