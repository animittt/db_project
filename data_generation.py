from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
import models


faker = Faker()
NUM_FACULTIES = 5
NUM_LEARNINGS = 10
NUM_STUDENTS = 100
def populate_faculty(db: Session):
    faculties = []
    for _ in range(NUM_FACULTIES):
        faculty = models.Faculty(
            name=faker.unique.company(),
            head_of_dp=faker.name(),
            number_of_places=faker.random_int(min=20, max=100),
            spec_name=faker.unique.word()
        )
        faculties.append(faculty)
        db.add(faculty)
    db.commit()
    print(f"{len(faculties)} faculties added.")
    return faculties

def populate_learning(db: Session, faculties):
    learnings = []
    for faculty in faculties:
        learning = models.Learning(
            spec_name=faculty.spec_name,
            amount_of_years=faker.random_int(min=1, max=5),
            scholarship_amount=faker.random_int(min=5000, max=20000) / 100,
            group=faker.random_int(min=1, max=20)
        )
        learnings.append(learning)
        db.add(learning)
    db.commit()
    print(f"{len(learnings)} learnings added.")

def populate_students(db: Session, faculties):
    students = []
    for _ in range(NUM_STUDENTS):
        faculty = faker.random.choice(faculties)
        student = models.Student(
            name_surname=faker.name(),
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=25),
            city=faker.city(),
            enrollment_year=faker.random_int(min=2015, max=2024),
            spec_name=faculty.spec_name
        )
        students.append(student)
        db.add(student)
    db.commit()
    print(f"{len(students)} students added.")

def main():
    db = SessionLocal()
    try:
        print("Populating faculty table")
        faculties = populate_faculty(db)
        print("Populating learning table")
        populate_learning(db, faculties)
        print("Populating student table")
        populate_students(db, faculties)
        print("Database population completed")
    finally:
        db.close()

if __name__ == "__main__":
    main()
