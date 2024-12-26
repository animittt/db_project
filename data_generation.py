from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Initialize Faker
faker = Faker()

# Number of records to generate
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
            spec_name=faker.unique.word()  # Ensure spec_name is unique
        )
        faculties.append(faculty)
        db.add(faculty)
    db.commit()
    print(f"{len(faculties)} faculties added.")
    return faculties  # Return the created faculties for use in other tables

def populate_learning(db: Session, faculties):
    learnings = []
    for faculty in faculties:
        # Use spec_name from the Faculty table to ensure the connection
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
        faculty = faker.random.choice(faculties)  # Randomly select a faculty
        student = models.Student(
            name_surname=faker.name(),
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=25),
            city=faker.city(),
            enrollment_year=faker.random_int(min=2015, max=2024),
            spec_name=faculty.spec_name  # Use spec_name from the Faculty table
        )
        students.append(student)
        db.add(student)
    db.commit()
    print(f"{len(students)} students added.")

def main():
    db = SessionLocal()
    try:
        print("Populating faculty table...")
        faculties = populate_faculty(db)  # Capture faculties for linking
        print("Populating learning table...")
        populate_learning(db, faculties)  # Pass faculties to the learning function
        print("Populating student table...")
        populate_students(db, faculties)  # Pass faculties to the students function
        print("Database population completed.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
