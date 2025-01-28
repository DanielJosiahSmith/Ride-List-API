from .models import Ride,Ride_Event
from rest_framework import serializers


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride_Event
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id_ride','status','id_rider','id_driver','pickup_latitude',
                  'pickup_longitude','dropoff_latitude','dropoff_longitude',
                  'pickup_time']

