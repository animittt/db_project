
from sqlalchemy import Column, Integer, String, Numeric, Date
from database import Base

class Faculty(Base):
    __tablename__ = "faculty"
    name = Column(String(100), primary_key=True)
    head_of_dp = Column(String(60), nullable=False)
    number_of_places = Column(Integer, nullable=True)
    spec_name = Column(String(100), nullable=True)

class Learning(Base):
    __tablename__ = "learning"
    spec_name = Column(String(100), primary_key=True)
    amount_of_years = Column(Integer, nullable=True)
    scholarship_amount = Column(Numeric(6, 2), nullable=True)
    group = Column(Integer, nullable=True)

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_surname = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    city = Column(String(40), nullable=False)
    enrollment_year = Column(Integer, nullable=True)
    spec_name = Column(String(100), nullable=True)


