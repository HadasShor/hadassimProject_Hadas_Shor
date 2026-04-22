import requests
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000/locations"


demo_data = [
    {"id": "2222", "name": "הדס", "lat": [32, 5, 23], "lon": [34, 46, 44]},   # נמל ת"א (מרכז)
    {"id": "3333",  "name": "טליה", "lat": [32, 5, 40], "lon": [34, 46, 50]},    # קרוב לנמל
    {"id": "4444",    "name": "יעלa", "lat": [32, 30, 0], "lon": [34, 50, 0]},   # נתניה (רחוק)
    {"id": "5555",       "name": "אילה", "lat": [31, 46, 0], "lon": [35, 13, 0]},   # ירושלים (רחוק מאוד)
    {"id": "6666",      "name": "שירה", "lat": [32, 48, 0], "lon": [34, 59, 0]},    # חיפה (רחוק מאוד)
    {"id": "7777",       "name": "שרה", "lat": [31, 14, 0], "lon": [34, 47, 0]},     # באר שבע (רחוק מאוד)
    {"id": "8888",     "name": "רבקה", "lat": [32, 10, 0], "lon": [34, 50, 0]},  # הרצליה (רחוק)
    {"id": "9999", "name": "רחל", "lat": [32, 6, 0], "lon": [34, 47, 0]}, # צפון ת"א (קרוב)
    {"id": "1010",      "name": "לאה", "lat": [29, 33, 0], "lon": [34, 57, 0]}      # אילת (הכי רחוק)
]

def send_location(st_id, lat_dms, lon_dms):
    payload = {
        "ID": st_id,
        "Coordinates": {
            "Longitude": {"Degrees": lon_dms[0], "Minutes": lon_dms[1], "Seconds": lon_dms[2]},
            "Latitude": {"Degrees": lat_dms[0], "Minutes": lat_dms[1], "Seconds": lat_dms[2]}
        },
        "Time": datetime.now().isoformat() + "Z"
    }
    try:
        r = requests.post(API_URL, json=payload)
        return r.status_code == 200
    except:
        return False

print("--- מתחיל  ---")

for student in demo_data:
    success = send_location(student["id"], student["lat"], student["lon"])
    status = "הצליח" if success else "נכשל (ודאי שהתלמידה רשומה!)"
    print(f"שולח מיקום עבור {student['name']} ({student['id']}): {status}")
    time.sleep(1)

print("\n--- הסתיים ---")