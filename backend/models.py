from sqlalchemy import Column, Integer, String,Float, DateTime
from database import Base

from sqlalchemy.sql import func
#הגדרות איך הנתונים נשמרים בבסיס הנתונים 
#כל המחלקות פה יורשות מBASE שהוא מתורגם לSQL ןנשמר בבסיס נתןונים
class StudentLocation(Base):
    __tablename__ = "student_locations"

    id = Column(Integer, primary_key=True, index=True)#הוספתי מזהה פנימי של השורה כאינדקס בשביל הנוחות
    student_id = Column(String)#תכלס זה כל משתמש בטבלה גם מורה וגם תלמידה 
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


