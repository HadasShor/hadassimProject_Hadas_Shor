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
hadassim_db_1

Create a `.env` file and configure:
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/hadassim_db_1
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
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/students` | Add a new student (full name, ID, class). |
| POST | `/teachers` | Add a new teacher (full name, ID, class). |
| GET | `/students` | Retrieve all students (accessible only to verified teachers). |
| GET | `/teachers` | Retrieve all teachers (accessible only to verified teachers). |
| GET | `/students/{identity_number}` | Retrieve a specific student by ID (teacher access required). |
| GET | `/teachers/{identity_number}` | Retrieve a specific teacher by ID (teacher access required). |
| GET | `/teachers/my-class/students` | Retrieve all students belonging to the authenticated teacher's class. |

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
![error](screenshots/error.png)




###  Assumptions & Design Decisions
### Access Control

User authentication is simplified and based on verifying the provided ID against the Teachers table for each request.

### Data Integrity

Teachers can retrieve all records and can also filter students by their own class.

## Phase B: Real-Time Location Tracking System

In this phase, the system was expanded to include real-time geographical tracking of participants using an interactive map interface and GPS data processing.

### Core Features (Phase B)

#### Real-Time Map Interface
- Integrated **Leaflet.js** to provide an interactive map of Israel.
- Dynamic markers that represent the last known location of each student and teacher.
- Automatic UI updates: The map refreshes every 60 seconds to ensure data accuracy.

#### Advanced GPS Data Processing
- **DMS to Decimal Conversion**: The system accepts coordinates in Degrees, Minutes, and Seconds (DMS) format—simulating real GPS hardware—and converts them to Decimal Degrees for mapping.
- **Location History**: The backend stores multiple location pings while the frontend intelligently fetches only the `latest` position for each user.


---

### New Technologies & Tools

#### Mapping & GIS
- **Leaflet.js**: An open-source JavaScript library for mobile-friendly interactive maps.
- **OpenStreetMap**: Used as the base map layer provider.

#### Backend Logic
- **Geospatial Math**: Implementation of spherical geometry for distance tracking.
- **Simulated Data Stream**: A Python simulation script to demonstrate live movement and map population.

---

### API Endpoints (Updated)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/locations` | Receive GPS data (DMS format) from tracking devices. |
| GET | `/locations/latest` | Retrieve the most recent location for all active participants. |

---

### How to Use the Tracking System

1. **Start the Backend**: Ensure your FastAPI server is running (`uvicorn main:app --reload`).
2. **Populate Data**: Use the `simulator.py` script or Swagger UI to send location JSONs to the `/locations` endpoint.
3. **Open the Map**: Refresh `index.html`. You will see blue markers appearing across the map.

---

### System Preview 

#### Live Tracking Map
![Live Map](screenshots/mapA.png)


![Live Map](screenshots/mapB.png)

---

### Design Decisions & Assumptions

- **Latest Location Logic**: To maintain performance, the map only renders the most recent coordinate for each ID, preventing clutter from historical data.
- **DMS Format**: The decision to use Degrees/Minutes/Seconds in the API was made to simulate professional GPS device integration.



## Phase C: Teacher’s Safety & Alert System (Bonus)

This final phase introduces a safety intelligence layer, enabling teachers to monitor their class and receive automatic alerts when students move beyond a defined safe distance.

---

### Core Features (Phase C)

#### Smart Proximity Alerts
- **Dynamic Distance Calculation**: Uses the Haversine formula to calculate real-time aerial distance between a teacher and their students.
- **Safety Perimeter**: A "Too Far" alert is triggered when a student exceeds a 3 km radius from their teacher.
- **Visual Warnings**: When a teacher enters their ID, the map highlights out-of-range students using highlighted warning markers with descriptive popups.

#### Class-Based Monitoring
- **Automatic Filtering**: The system identifies the teacher’s class and monitors only the relevant students instead of all participants.

---

### API Endpoints (Bonus Update)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/teachers/{id}/alerts` | Returns students located more than 3 km away from the specified teacher |

---

### How to Use the Alert System

1. **Teacher Identification**  
   In the "Teacher Control Center" section on the map, enter the teacher's ID (e.g., `1111`).

2. **Activate Monitoring**  
   Click **"Update Locations & Alerts"**.

3. **Monitor Results**  
   - **Blue Markers**: Students within the 3 km safe zone  
   - **highlighted warning markers**: Students outside the safe zone  
     Click on a red marker to see the exact distance from the teacher.

---

### Safety System Preview (Phase C)

#### Proximity Alert Example  

![Live Map1](screenshots/c1.png)


![Live Map2](screenshots/c2.png)

---

### Design Decisions & Assumptions

- **Teacher-Centric Logic**: The teacher’s last known location serves as the anchor point for all distance calculations. If no location is available, alerts cannot be generated.
- **3 km Threshold**:The 3 km threshold follows the assignment requirement.
- **Performance Optimization**: Distance calculations are handled on the backend to ensure a smooth and responsive map interface.
