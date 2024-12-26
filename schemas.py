from pydantic import BaseModel
from typing import Optional

class FacultyBase(BaseModel):
    name: str
    head_of_dp: str
    number_of_places: Optional[int] = None
    spec_name: Optional[str] = None

class FacultyCreate(FacultyBase):
    pass

class FacultyRead(FacultyBase):
    pass

class FacultyUpdate(BaseModel):
    head_of_dp: Optional[str] = None
    number_of_places: Optional[int] = None
    spec_name: Optional[str] = None

class LearningBase(BaseModel):
    spec_name: str
    amount_of_years: int
    scholarship_amount: Optional[float] = None
    group: Optional[int] = None

class LearningCreate(LearningBase):
    pass

class LearningRead(LearningBase):
    pass

class LearningUpdate(BaseModel):
    amount_of_years: Optional[int] = None
    scholarship_amount: Optional[float] = None
    group: Optional[int] = None

from datetime import date

# Student schema for reading
class StudentRead(BaseModel):
    name_surname: str
    date_of_birth: date
    city: str
    enrollment_year: Optional[int]
    spec_name: Optional[str]

    class Config:
        from_attributes = True

# Student schema for creating
class StudentCreate(BaseModel):
    name_surname: str
    date_of_birth: date
    city: str
    enrollment_year: Optional[int]
    spec_name: Optional[str]