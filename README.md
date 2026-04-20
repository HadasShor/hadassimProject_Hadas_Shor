# hadassimProject_Hadas_Shor

## School Trip Management System – Hadassim Program

A system for managing registration and data retrieval for a school trip to Jerusalem.  
This project was developed as part of the Phase A home assignment in the Hadassim program and demonstrates a full-stack application including backend, database, and user interface.



## Core Features (Phase A)

### User Registration

A dedicated interface for registering both students and teachers.  
Each user provides:
- Full Name  
- ID Number  
- Class  

### Teacher-Only Data Access

The system restricts data retrieval exclusively to users identified as teachers, using verification against the database.

### Smart Filtering

Teachers can:
- View all trip participants  
- Filter students based on their own class  

### Basic Data Management

The system supports:
- Create operations  
- Read operations  

> Update and Delete operations are not implemented, according to assignment requirements.


## Technologies

### Backend
- Python  
- FastAPI – for building efficient and clear REST APIs  

### Database
- PostgreSQL  
- Managed using pgAdmin  

### ORM
- SQLAlchemy – mapping Python objects to database tables  

### Frontend
- HTML



## Installation & Setup

### 1. Database Configuration

Create a PostgreSQL database named: 
hadassim_db

Create a `.env` file and configure:
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5433/hadassim_db


### 2. Install Dependencies

```bash
pip install -r requirements.txt

3. Run the Server
uvicorn main:app --reload

The server will be available at:

http://127.0.0.1:8000
4. Run the Frontend

Open index.html in your browser
or run:

python -m http.server 5500
API Endpoints
Method	Endpoint	Description
POST	/students	Add a student
POST	/teachers	Add a teacher
GET	/students	Retrieve students (teachers only)

Access to GET endpoints is restricted and requires teacher ID verification.
System Preview

Add screenshots of:

Registration forms for students and teachers
Teacher dashboard displaying query results
Assumptions & Design Decisions
Access Control

User authentication is simplified and based on verifying the provided ID against the Teachers table for each request.

Data Integrity

Each teacher can only access students belonging to their own class.

Simplicity

The system is designed to be clear and focused, demonstrating proper backend–database integration and API design.

Summary

This project demonstrates a basic full-stack system including:

API development using FastAPI
Relational database integration with PostgreSQL
Data modeling using SQLAlchemy
Separation between backend and frontend

The system highlights core principles such as data management, access control, and API-based communication.

