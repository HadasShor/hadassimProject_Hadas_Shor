from pydantic import BaseModel
from datetime import datetime


class StudentCreate(BaseModel):
    full_name: str
    identity_number: str
    class_name: str


class TeacherCreate(BaseModel):
    full_name: str
    identity_number: str
    class_name: str




class CoordinateDetail(BaseModel):
    Degrees: int
    Minutes: int
    Seconds: float

class Coordinates(BaseModel):
    Longitude: CoordinateDetail
    Latitude: CoordinateDetail

class LocationIn(BaseModel):
    ID: str
    Coordinates: Coordinates
    Time: datetime

class LocationOut(BaseModel):
    student_id: str
    latitude: float
    longitude: float
    timestamp: datetime

    class Config:
        from_attributes = True