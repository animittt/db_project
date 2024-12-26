from sqlalchemy.orm import Session
import models, schemas

def create_faculty(db: Session, faculty: schemas.FacultyCreate):
    db_faculty = models.Faculty(
        name=faculty.name,
        head_of_dp=faculty.head_of_dp,
        number_of_places=faculty.number_of_places,
        spec_name=faculty.spec_name
    )
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def get_faculty(db: Session, name: str):
    return db.query(models.Faculty).filter(models.Faculty.name == name).first()

def get_faculties(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Faculty).offset(skip).limit(limit).all()

def update_faculty(db: Session, name: str, faculty: schemas.FacultyUpdate):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.name == name).first()
    if db_faculty is None:
        return None
    for key, value in faculty.dict(exclude_unset=True).items():
        setattr(db_faculty, key, value)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

def delete_faculty(db: Session, name: str):
    db_faculty = db.query(models.Faculty).filter(models.Faculty.name == name).first()
    if db_faculty:
        db.delete(db_faculty)
        db.commit()
    return db_faculty


def create_learning(db: Session, learning: schemas.LearningCreate):
    db_learning = models.Learning(
        spec_name=learning.spec_name,
        amount_of_years=learning.amount_of_years,
        scholarship_amount=learning.scholarship_amount,
        group=learning.group
    )
    db.add(db_learning)
    db.commit()
    db.refresh(db_learning)
    return db_learning

def get_learning(db: Session, spec_name: str):
    return db.query(models.Learning).filter(models.Learning.spec_name == spec_name).first()

def get_learnings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Learning).offset(skip).limit(limit).all()

def update_learning(db: Session, spec_name: str, learning: schemas.LearningUpdate):
    db_learning = db.query(models.Learning).filter(models.Learning.spec_name == spec_name).first()
    if db_learning is None:
        return None
    for key, value in learning.dict(exclude_unset=True).items():
        setattr(db_learning, key, value)
    db.commit()
    db.refresh(db_learning)
    return db_learning

def delete_learning(db: Session, spec_name: str):
    db_learning = db.query(models.Learning).filter(models.Learning.spec_name == spec_name).first()
    if db_learning:
        db.delete(db_learning)
        db.commit()
    return db_learning

from typing import List, Optional


# Get all students with pagination
def get_students(db: Session, skip: int = 0, limit: int = 10) -> List[models.Student]:
    return db.query(models.Student).offset(skip).limit(limit).all()


# Get a student by ID
def get_student_by_id(db: Session, student_id: int) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


# Create a new student
def create_student(db: Session, student_data: schemas.StudentCreate) -> models.Student:
    db_student = models.Student(**student_data.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# Update a student's information
def update_student(db: Session, student_id: int, updated_data: dict) -> int:
    result = db.query(models.Student).filter(models.Student.id == student_id).update(updated_data)
    db.commit()
    return result


# Delete a student
def delete_student(db: Session, student_id: int) -> int:
    result = db.query(models.Student).filter(models.Student.id == student_id).delete()
    db.commit()
    return result

