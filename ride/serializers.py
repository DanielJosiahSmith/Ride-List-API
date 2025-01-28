from .models import Ride,Ride_Event
from rest_framework import serializers


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride_Event
        fields = '__all__'