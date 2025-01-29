from django.db import connection
from django.core.serializers import serialize
from .models import Ride

def results_by_distance(target_lat, target_lng, offset=0, limit=10):
    radius_km = 1000  # Radius in kilometers

    # Query with Bounding Box and Haversine Formula
    query = f"""
    SELECT * ,
        (
            6371 * acos(
                cos(radians(%s)) * cos(radians(pickup_latitude)) *
                cos(radians(pickup_longitude) - radians(%s)) +
                sin(radians(%s)) * sin(radians(pickup_latitude))
            )
        ) AS distance
    FROM ride_Ride
    WHERE pickup_latitude BETWEEN %s - (%s / 111) AND %s + (%s / 111)
    AND pickup_longitude BETWEEN %s - (%s / (111 * cos(radians(%s)))) AND %s + (%s / (111 * cos(radians(%s))))
    ORDER BY distance
    LIMIT %s OFFSET %s;
    """

    params = [
        target_lat, target_lng, target_lat,  # For Haversine
        target_lat, radius_km, target_lat, radius_km,  # Latitude bounds
        target_lng, radius_km, target_lat, target_lng, radius_km, target_lat,  # Longitude bounds
        limit, offset  # Pagination
    ]

    # Return raw query results
    return Ride.objects.raw(query, params)
