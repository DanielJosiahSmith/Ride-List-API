from django.shortcuts import render
from .models import Ride, Ride_Event

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .validators import validate_new_ride
from .serializers import RideSerializer,RideEventSerializer
from .funcs import results_by_distance

class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all().order_by('id_ride')
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status','id_driver__email']
    ordering_fields = ['pickup_time']

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
    
    @action(detail=False, methods=['get'])
    def distance_to_pickup(self, request):
        longitude = self.request.query_params.get('longitude')
        latitude= self.request.query_params.get('latitude')
        offset = int(self.request.query_params.get('offset', 0))  # Default offset is 0
        limit = int(self.request.query_params.get('limit', 10))  # Default limit is 10
        
        qs = results_by_distance(latitude,longitude,offset,limit)
        serializer = RideSerializer(qs,many=True)

        return Response(serializer.data)

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = Ride_Event.objects.all()
    serializer_class = RideEventSerializer
    

    def create(self, request):
        try:
            ride_event = Ride_Event.objects.create(
                id_ride_id = request.data['id_ride'],
                description = request.data['description']
            )
            return Response({'msg':f'{ride_event.id_ride_event} - ride event created'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'400 BAD REQUEST'}, status.HTTP_400_BAD_REQUEST)
         
    