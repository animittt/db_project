
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models, crud, schemas
from database import SessionLocal, engine, Base
import schemas
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API! Use the available endpoints like /faculties/, /students/, etc."}

@app.get("/faculties/", response_model=List[schemas.FacultyRead])
def get_faculties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_faculties(db, skip=skip, limit=limit)

@app.get("/students/", response_model=List[schemas.StudentRead])
def get_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.post("/students/", response_model=schemas.StudentRead)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/{student_id}/", response_model=schemas.StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student