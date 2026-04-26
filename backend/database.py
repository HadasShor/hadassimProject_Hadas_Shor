import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")# לוקח את הURL של כתובת החיבור לבסיס נתונים

engine = create_engine(DATABASE_URL)#חיבור לבסיס נתונים 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#תבנית ליצירת אוביקט מול הבסיס נתונים 
Base = declarative_base()#כל השימוש בORM מול הבסיס נתונים זה דרך זה
