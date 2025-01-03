
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models, crud, schemas
from database import SessionLocal, engine, Base
import schemas
from sqlalchemy import func
from sqlalchemy.sql import cast
from sqlalchemy.types import String

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
    return {"message": "Welcome to the dekanat API! Use the available endpoints like /faculties/, /students/, etc."}

@app.get("/faculties/", response_model=List[schemas.FacultyRead])
def get_faculties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_faculties(db, skip=skip, limit=limit)

@app.get("/students/", response_model=List[schemas.StudentRead])
def get_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.post("/students/", response_model=schemas.StudentRead)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.post("/faculties/", response_model=schemas.FacultyRead) 
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db, faculty)

@app.get("/faculties/{name}/", response_model=schemas.FacultyRead)
def get_faculty(name: str, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, name)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty

@app.get("/students/filter-by-city/", response_model=List[schemas.StudentRead])
def filter_students(city: str, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(
        models.Student.city == city
    ).all()
    students = sorted(students, key=lambda x: x.name_surname)
    return students

@app.get("/students-with-faculty/", response_model=List[dict])
def students_with_faculty(db: Session = Depends(get_db)):
    results = db.query(
        models.Student.name_surname,
        models.Student.city,
        models.Faculty.head_of_dp
    ).join(models.Faculty, models.Student.spec_name == models.Faculty.spec_name).all()
    results = sorted(results, key=lambda x: x[0])
    return [{"name_surname": row[0], "city": row[1], "head_of_dp": row[2]} for row in results]

@app.put("/students/update-city/")
def update_student_city(enrollment_year: int, spec_name: str, new_city: str, db: Session = Depends(get_db)):
    updated_rows = db.query(models.Student).filter(
        models.Student.enrollment_year < enrollment_year,
        models.Student.spec_name == spec_name
    ).update({models.Student.city: new_city})
    db.commit()
    return {"updated_rows": updated_rows}

@app.get("/students/count-by-city/")
def count_students_by_city(db: Session = Depends(get_db)):
    results = db.query(
        models.Student.city,
        func.count(models.Student.id).label("student_count")
    ).group_by(models.Student.city).all()
    return [{"city": row[0], "student_count": row[1]} for row in results]

@app.get("/students/search-by-name/")
def search_students_by_name(name: str, db: Session = Depends(get_db)):
    students = crud.search_students_by_name(db, name)
    if students is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return students

@app.get("/students/search-with-metadata/")
def search_students(query: str, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(
        cast(models.Student.meta_info, String).ilike(f"%{query}%")
    ).all()
    if students is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return students

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