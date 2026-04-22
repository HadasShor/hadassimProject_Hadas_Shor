from sqlalchemy import Column, Integer, String,Float, DateTime, ForeignKey
from database import Base

from sqlalchemy.sql import func


class StudentLocation(Base):
    __tablename__ = "student_locations"

    id = Column(Integer, primary_key=True, index=True)
    # שורה שצריך לשנות: במקום ForeignKey("students.identity_number")
    # פשוט הגדירי את זה כעמודה רגילה:
    student_id = Column(String) 
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime(timezone=True))

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    identity_number = Column(String, unique=True, nullable=False)
    class_name = Column(String, nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    identity_number = Column(String, unique=True, nullable=False)
    class_name = Column(String, nullable=False)