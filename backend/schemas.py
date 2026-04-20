from pydantic import BaseModel


class StudentCreate(BaseModel):
    full_name: str
    identity_number: str
    class_name: str


class TeacherCreate(BaseModel):
    full_name: str
    identity_number: str
    class_name: str