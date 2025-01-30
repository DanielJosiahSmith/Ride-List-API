# Ride API

## Getting Started

1. Create a directory for the project - $mkdir RideAPI
2. Cd into the directory - $cd RideAPI
3. Clone repository - $git clone https://github.com/DanielJosiahSmith/Ride-List-API.git
4. Create a virtual environment - $python -m venv venv
5. Activate virtual environment - $venv/scripts/activate
6. Install requirements.txt - $pip install -r requirement.txt
7. Run migrations - $python manage.py migrate
8. Start local server - $python manage.py runserver
9. Create a user(admin) using postman, cURL - ex. 
POST http://127.0.0.1:8000/users/
payload  {
    "role": "admin",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "phone_number": "1234567890"
}
10. Save token to use for all other requests. - ex.
response {
    "role": "admin",
    "msg": "1 - user created",
    "token": "abcd1234token"
}

# Authentication

Include in HTTP headers:<br>
"Authorization" : "Token [your-token-here]"



# Ride API Usage

## User

### Endpoints

#### List all users (Authenticated only)
```http
GET /api/users/
```

#### Create a new user (Public)
```http
POST /api/users/
```
**Request Body:**
```json
{
    "role": "admin",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "phone_number": "1234567890"
}
```
**Response:**
```json
{
    "role": "admin",
    "msg": "1 - user created",
    "token": "abcd1234token"
}
```

#### Retrieve a user (Authenticated only)
```http
GET /api/users/{id}/
```

#### Update a user (Authenticated only)
```http
PUT /api/users/{id}/
```

#### Delete a user (Authenticated only)
```http
DELETE /api/users/{id}/
```



## Ride

### Endpoints

#### List all rides
```http
GET /api/rides/
```
**Response:**
```json
[
     {
            "id_ride": 1,
            "status": "en-route",
            "id_driver": {
                "user_id": 2,
                "role": "admin",
                "first_name": "fred",
                "last_name": "flintstone",
                "email": "flintstone@gmail.com",
                "phone_number": "555-5555"
            },
            "id_rider": {
                "user_id": 1,
                "role": "admin",
                "first_name": "dan",
                "last_name": "smith",
                "email": "d@gmail.com",
                "phone_number": "555-5555"
            },
            "pickup_latitude": "37.755651",
            "pickup_longitude": "-122.447557",
            "dropoff_latitude": "37.619572",
            "dropoff_longitude": "-122.381601",
            "pickup_time": null,
            "ride_event_set": [
                {
                    "id_ride_event": 1,
                    "description": "Status changed to pickup",
                    "created_at": "2025-01-28T08:43:02.686500Z",
                    "id_ride": 1
                },
                {
                    "id_ride_event": 2,
                    "description": "Status changed to pickup",
                    "created_at": "2025-01-28T08:43:41.879567Z",
                    "id_ride": 1
                },
                {
                    "id_ride_event": 1921,
                    "description": "Status changed to dropoff",
                    "created_at": "2025-01-28T09:47:01.904091Z",
                    "id_ride": 1
                },
                {
                    "id_ride_event": 3531,
                    "description": "Status changed to dropoff",
                    "created_at": "2025-01-28T09:47:01.940091Z",
                    "id_ride": 1
                },
                {
                    "id_ride_event": 4158,
                    "description": "Status changed to pickup",
                    "created_at": "2025-01-28T09:47:01.954091Z",
                    "id_ride": 1
                }
            ],
            "todays_ride_events": []
    }
]
```

#### Create a new ride
```http
POST /api/rides/
```
**Request Body:**
```json
{
    "status": "ongoing",
    "id_rider": 2,
    "id_driver": 5,
    "pickup_latitude": 40.7128,
    "pickup_longitude": -74.0060,
    "dropoff_latitude": 40.7306,
    "dropoff_longitude": -73.9352
}
```
**Response:**
```json
{
    "msg": "1 - ride created"
}
```

#### Retrieve a ride
```http
GET /api/rides/{id}/
```

#### Update a ride
```http
PUT /api/rides/{id}/
```

#### Delete a ride
```http
DELETE /api/rides/{id}/
```

#### Get rides by distance to pickup location
```http
GET /api/rides/distance_to_pickup/?latitude=40.7128&longitude=-74.0060&offset=0&limit=10
```

---

## Ride Event API

### Endpoints

#### List all ride events
```http
GET /api/ride-events/
```

#### Create a new ride event
```http
POST /api/ride-events/
```
**Request Body:**
```json
{
    "id_ride": 1,
    "description": "Ride started"
}
```
**Response:**
```json
{
    "msg": "1 - ride event created"
}
```

#### Retrieve a ride event
```http
GET /api/ride-events/{id}/
```

#### Update a ride event
```http
PUT /api/ride-events/{id}/
```

#### Delete a ride event
```http
DELETE /api/ride-events/{id}/
```

## Bonus SQL
 ~~~~sql
With ride_durations As(
    SELECT
        r.id_driver_id,
        strftime('%Y-%m', pe.created_at) AS month,
        pe.created_at AS pickup_time,
        de.created_at AS dropoff_time,
        (julianday(de.created_at) - julianday(pe.created_at)) * 24 AS duration_hours
    FROM ride_Ride r
    JOIN ride_Ride_Event pe ON r.id_ride = pe.id_ride_id AND pe.description = 'Status changed to pickup'
    JOIN ride_Ride_Event de ON r.id_ride = de.id_ride_id AND de.description = 'Status changed to dropoff'
    WHERE de.created_at > pe.created_at
)SELECT 
    strftime('%Y-%m', rd.pickup_time) AS Month,
    u.first_name || ' ' || u.last_name AS Driver,
    COUNT(*) AS 'Count of Trips > 1 hr'
FROM ride_durations rd
JOIN user_CustomUser u ON rd.id_driver_id = u.user_id
WHERE rd.duration_hours > 1
GROUP BY Month, Driver
ORDER BY Month, Driver;
 ~~~~
---

