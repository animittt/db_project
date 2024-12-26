
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

@app.get("/students/filter-by-city/", response_model=List[schemas.StudentRead])
def filter_students(city: str, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(
        models.Student.city == city
    ).all()
    return students

@app.get("/students-with-faculty/", response_model=List[dict])
def students_with_faculty(db: Session = Depends(get_db)):
    results = db.query(
        models.Student.name_surname,
        models.Student.city,
        models.Faculty.head_of_dp
    ).join(models.Faculty, models.Student.spec_name == models.Faculty.spec_name).all()

    return [{"name_surname": row[0], "city": row[1], "head_of_dp": row[2]} for row in results]

@app.put("/students/update-city/")
def update_student_city(enrollment_year: int, spec_name: str, new_city: str, db: Session = Depends(get_db)):
    updated_rows = db.query(models.Student).filter(
        models.Student.enrollment_year < enrollment_year,
        models.Student.spec_name == spec_name
    ).update({models.Student.city: new_city})
    db.commit()
    return {"updated_rows": updated_rows}

from sqlalchemy import func

@app.get("/students/count-by-city/")
def count_students_by_city(db: Session = Depends(get_db)):
    results = db.query(
        models.Student.city,
        func.count(models.Student.id).label("student_count")
    ).group_by(models.Student.city).all()

    return [{"city": row[0], "student_count": row[1]} for row in results]

@app.delete("/students/{student_id}/")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted_rows = crud.delete_student(db, student_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"deleted_rows": deleted_rows}

@app.put("/students/{student_id}/")
def update_student(student_id: int, updated_data: dict, db: Session = Depends(get_db)):
    updated_rows = crud.update_student(db, student_id, updated_data)
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"updated_rows": updated_rows}


@app.get("/students/{student_id}/", response_model=schemas.StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student