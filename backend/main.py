from database import engine, SessionLocal
import models
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import schemas
import math
models.Base.metadata.create_all(bind=engine)#כל היצירה של הטבלאות והכול מתבצע פה (במידה ולא קיימות עדיין יוצר אותם)


app = FastAPI()#יצירת האוביקט של האפליקציה כל הפונקציות של APP נרשמות על האוביקט הזה

#CORS 
#כדי שהפרונט יוכל לדבר עם הבאק  כי מתי שהם באים מבקשות שלא תואמות בדיוק יכול להיות חסימה ולכן עשיתי הרשאה לכל הבקשות שיגיעו מהפרונט 
#בגלל שזה אבטחה ממש לא מגבילה אז הוספתי בדיקה של תז של מורה בהמשך 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#כל קריאה לפונקציה נוצרת עבודת יחידה בפני עצמה מול הבסיס נתונים נועד בשביל הסדר והארגון 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:#כל עוד הפונקציה סיימה לא משנה אם הצליחה או נכשלה תעבור לפה לסגור אותה
        db.close()

# מקבל תז מורה וחיבור פעיל לבסיס נתונים 
def verify_teacher_access(teacher_identity_number: str, db: Session):
    teacher = db.query(models.Teacher).filter(
        models.Teacher.identity_number == teacher_identity_number
    ).first()#מחפש מתוך הטבלה של המורות את התז הראשונה שתואמת

    if not teacher:
        raise HTTPException(
            status_code=403,#שגיאת אין הרשאה לבצע
            detail="Access allowed for teachers only"
        )

    return teacher
#פונקציות בדיקה שהכול עובד 
@app.get("/")
def root():
    return {"message": "Hadassim backend is running"}
#בדיקה שהבסיס נתונים מצליח להתחבר
@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"message": "Database connection is working"}


#הוספת תלמידה חדשה 
@app.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(
        models.Student.identity_number == student.identity_number
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")
#אם לא קיימת כזאת יוצר אוביקט חדש של תלמידה 
    new_student = models.Student(
        full_name=student.full_name,
        identity_number=student.identity_number,
        class_name=student.class_name
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student#השרת מחזיר את האוביקט החדש של התלמידה שנוצר

#שליפת כל התלמידות של המורה
@app.get("/students")
def get_students(
    teacher_identity_number: str = Query(...),#קבלת תז של מורה מURL של הבקשה
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
#שליפת מורה
@app.get("/teachers")
def get_teachers(
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher_access(teacher_identity_number, db)
    return db.query(models.Teacher).all()


#מקבל תז של מורה בנתיב שנרצה את התלמידות שלה
@app.get("/teachers/my-class/students")
def get_my_class_students(
    teacher_identity_number: str = Query(...),
    db: Session = Depends(get_db)
):
    teacher = verify_teacher_access(teacher_identity_number, db)

    students = db.query(models.Student).filter(
        models.Student.class_name == teacher.class_name
    ).all()

    return students

#מקבל תז של תלמידה בURL
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
#שולף מורה ספציפית
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

#מקבלים גייסון של מעלות דקות ושניות וממירים את זה לדצימאלי
def dms_to_decimal(degrees, minutes, seconds):
    return float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)

@app.post("/locations")
def receive_location(loc: schemas.LocationIn, db: Session = Depends(get_db)):#נמיר את הגייסון שקיבלנו לדצימאלי
    lat = dms_to_decimal(
        loc.Coordinates.Latitude.Degrees,
        loc.Coordinates.Latitude.Minutes,
        loc.Coordinates.Latitude.Seconds
    )
    lon = dms_to_decimal(
        loc.Coordinates.Longitude.Degrees,
        loc.Coordinates.Longitude.Minutes,
        loc.Coordinates.Longitude.Seconds
    )

    
    # קודם נבדוק אם זו תלמידה
    user = db.query(models.Student).filter(models.Student.identity_number == loc.ID).first()
    
    # אם לא נמצאה תלמידה נבדוק אם זו מורה
    if not user:
        user = db.query(models.Teacher).filter(models.Teacher.identity_number == loc.ID).first()
    
    # רק אם לא נמצא אף אחד בשתי הטבלאות שגיאה
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {loc.ID} not found in Students or Teachers."
        )
#ניצור אוביקט חדש של מיקום
    new_location = models.StudentLocation(
        student_id=loc.ID,
        latitude=lat,
        longitude=lon,
        timestamp=loc.Time
    )
    
    db.add(new_location)#מכניס לבסיס נתונים
    db.commit()
    db.refresh(new_location)
    
    return new_location#מחזיר תשובה  ללקוח בפורמט גייסון

@app.get("/locations/latest")
def get_latest_locations(db: Session = Depends(get_db)):
    from sqlalchemy import func#מאפשר להתשמש בפונק SQLבצוך פייתון 
    
    #  מציאת זמן העדכון המקסימלי לכל תלמידה הכול נוצר בשאילתא זמנית
    subquery = db.query(
        models.StudentLocation.student_id,
        func.max(models.StudentLocation.timestamp).label('max_ts')
    ).group_by(models.StudentLocation.student_id).subquery()

    #  שליפת השורות המלאות שתואמות לזמנים שמצאנו בשאילתא לפני כמו JOIN בSQL
    latest_locs = db.query(models.StudentLocation).join(
        subquery, 
        (models.StudentLocation.student_id == subquery.c.student_id) & 
        (models.StudentLocation.timestamp == subquery.c.max_ts)
    ).all()
    
    return latest_locs


#חישוב מרחק אוירי על כדור הארץ נוסחת הויאנס
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 #רדיוס כדור הארץ
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@app.get("/teachers/{teacher_id}/alerts")
def get_teacher_alerts(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.identity_number == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    #  מציאת המיקום האחרון של המורה
    teacher_loc = db.query(models.StudentLocation).filter(
        models.StudentLocation.student_id == teacher_id
    ).order_by(models.StudentLocation.timestamp.desc()).first()

    if not teacher_loc:
        return {"alerts": [], "message": "No location found for teacher"}

    # מציאת כל התלמידות שרשומות באותה כיתה של המורה
    students = db.query(models.Student).filter(models.Student.class_name == teacher.class_name).all()
    
    alerts = []#ניצור רשימה של כל התלמידות שחורגות 
    for student in students:
        # מציאת המיקום האחרון של התלמידה
        s_loc = db.query(models.StudentLocation).filter(
            models.StudentLocation.student_id == student.identity_number
        ).order_by(models.StudentLocation.timestamp.desc()).first()

        if s_loc:
            dist = calculate_distance(teacher_loc.latitude, teacher_loc.longitude, s_loc.latitude, s_loc.longitude)
            
            # אם מרחק התלמידה גדול מ3
            if dist > 3:
                alerts.append({
                    "student_id": student.identity_number,
                    "student_name": student.full_name,
                    "distance": round(dist, 2),
                    "lat": s_loc.latitude,
                    "lon": s_loc.longitude
                })

    return {"alerts": alerts}#מחזיר את רשימת ההתראות כמילון