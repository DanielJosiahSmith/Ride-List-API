from django.shortcuts import render
from .models import Ride, Ride_Event

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .validators import validate_new_ride
from .serializers import RideSerializer,RideEventSerializer

class RideViewSet(viewsets.ViewSet):

    def create(self, request):
        valid,msg = validate_new_ride(request.data)

        if valid:
            ride = Ride.objects.create(
                status=request.data['status'],
                id_rider_id=request.data['id_rider'],
                id_driver_id=request.data['id_driver'],
                pickup_latitude=request.data['pickup_latitude'],
                pickup_longitude=request.data['pickup_longitude'],
                dropoff_latitude=request.data['dropoff_latitude'],
                dropoff_longitude=request.data['dropoff_longitude'],
            )

            return Response({'msg':f'{ride.id_ride} - ride created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':msg}, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Ride.objects.all()
        serializer = RideSerializer(queryset,many=True)
        return Response(serializer.data)
        

class RideEventViewSet(viewsets.ViewSet):

    def create(self, request):
        try:
            ride_event = Ride_Event.objects.create(
                id_ride_id = request.data['id_ride'],
                description = request.data['description']
            )
            return Response({'msg':f'{ride_event.id_ride_event} - ride event created'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'400 BAD REQUEST'}, status.HTTP_400_BAD_REQUEST)
         
     
            

    def list(self, request):
        queryset = Ride_Event.objects.all()
        serializer = RideEventSerializer(queryset,many=True)
        return Response(serializer.data)