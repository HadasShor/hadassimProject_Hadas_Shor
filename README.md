# hadassimProject_Hadas_Shor

## School Trip Management System – Hadassim Program

A system for managing registration and data retrieval for a school trip to Jerusalem.  

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
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/hadassim_db
### 2. Create Virtual Environment
python -m venv venv
Activate it:
venv\Scripts\activate
### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run the Server
cd backend
uvicorn main:app --reload

The server will be available at:

http://127.0.0.1:8000
### 5. Test the Backend
Open in browser:
http://127.0.0.1:8000/docs
You can test all API endpoints from there.
### 6. Run the Frontend

Open index.html in your browser
or run:

python -m http.server 5500
### 7. Important Notes
The backend must be running before using the frontend
The frontend communicates with the backend via HTTP requests
CORS is enabled to allow communication between frontend and backend
Make sure PostgreSQL is running before starting the server

###  API Endpoints
Method	Endpoint	Description
POST	/students	Add a student
POST	/teachers	Add a teacher
GET	/students	Retrieve students (teachers only)

Access to GET endpoints is restricted and requires teacher ID verification.
 ### System Preview
 
### Student Registration Form
![Student Form](screenshots/student_reg.png)
### Teacher Registration Form
![Teacher Form](screenshots/teach_reg.png)
### Teacher View
![Teacher View](screenshots/teach_p.png)
![Student View](screenshots/stud_p.png)
![Class View](screenshots/class.png)
![All Students](screenshots/all.png)




###  Assumptions & Design Decisions
### Access Control

User authentication is simplified and based on verifying the provided ID against the Teachers table for each request.

### Data Integrity

Each teacher can only access students belonging to their own class.

### Simplicity

The system is designed to be clear and focused, demonstrating proper backend–database integration and API design.
