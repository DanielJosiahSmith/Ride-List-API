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
        "status": "ongoing",
        "id_rider": 2,
        "id_driver": 5,
        "pickup_latitude": 40.7128,
        "pickup_longitude": -74.0060,
        "dropoff_latitude": 40.7306,
        "dropoff_longitude": -73.9352
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

---

