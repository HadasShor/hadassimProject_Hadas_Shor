from database import engine, SessionLocal
import models
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_teacher_access(teacher_identity_number: str, db: Session):
    teacher = db.query(models.Teacher).filter(
        models.Teacher.identity_number == teacher_identity_number
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=403,
            detail="Access allowed for teachers only"
        )

    return teacher

@app.get("/")
def root():
    return {"message": "Hadassim backend is running"}

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"message": "Database connection is working"}



@app.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(
        models.Student.identity_number == student.identity_number
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")

    new_student = models.Student(
        full_name=student.full_name,
        identity_number=student.identity_number,
        class_name=student.class_name
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students")
def get_students(
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)
    return db.query(models.Student).all()

@app.post("/teachers")
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    existing_teacher = db.query(models.Teacher).filter(
        models.Teacher.identity_number == teacher.identity_number
    ).first()

    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher already exists")

    new_teacher = models.Teacher(
        full_name=teacher.full_name,
        identity_number=teacher.identity_number,
        class_name=teacher.class_name
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

@app.get("/teachers")
def get_teachers(
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)
    return db.query(models.Teacher).all()


@app.get("/teachers/by-identity/{identity_number}/students")
def get_students_by_teacher_identity(
    identity_number: str,
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)

    teacher = db.query(models.Teacher).filter(
        models.Teacher.identity_number == identity_number
    ).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    students = db.query(models.Student).filter(
        models.Student.class_name == teacher.class_name
    ).all()

    return students


@app.get("/students/{identity_number}")
def get_student(
    identity_number: str,
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)

    student = db.query(models.Student).filter(
        models.Student.identity_number == identity_number
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.get("/teachers/{identity_number}")
def get_teacher(
    identity_number: str,
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)

    teacher = db.query(models.Teacher).filter(
        models.Teacher.identity_number == identity_number
    ).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher
