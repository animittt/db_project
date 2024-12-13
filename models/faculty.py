
from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Faculty(Base):
    __tablename__ = "faculty"
    name = Column(String(100), primary_key=True)
    head_of_dp = Column(String(60), nullable=False)
    number_of_places = Column(Integer, nullable=True)
    spec_name = Column(String(100), nullable=True)
