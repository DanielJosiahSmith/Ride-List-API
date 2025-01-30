from django.shortcuts import render
from django.db.models import Prefetch
from .models import Ride, Ride_Event

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .validators import validate_new_ride
from .serializers import RideSerializer,RideEventSerializer
from .funcs import results_by_distance

from datetime import timedelta
from django.utils.timezone import now


class RideViewSet(viewsets.ModelViewSet):
    """A ViewSet for creating, listing, retrieving, updating, and deleting rides."""

    serializer_class = RideSerializer
   
    #Add filtering for status, and driver_email
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status','id_driver__email']
    
    def get_queryset(self):
        #sorting based on pickup_time
        order_by = 'id_ride'
        order_pickup = self.request.query_params.get('order_pickup')
        if order_pickup == 'recent':
            order_by = '-pickup_time'
        elif order_pickup == 'last':
            order_by = 'pickup_time'
        

         #select_related to get users
        #prefetch for ride_events per ride
        #another prefetch for ride_events within the past 24 hours
        queryset = Ride.objects.select_related(
                            'id_driver','id_rider'
                            ).prefetch_related(
                                'ride_event_set'
                            ).prefetch_related(
                                Prefetch('ride_event_set', queryset=Ride_Event.objects.filter(created_at__gte=now()-timedelta(hours=24)),to_attr='todays_ride_events'),
                            ).all().order_by(order_by)

        return queryset

    def create(self, request):
        try:
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
        except:
            return Response({'message':'400 Bad Request'}, status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def distance_to_pickup(self, request):
        """define a custom url method to get rides based on distance from a given location"""
        try:
            longitude = self.request.query_params.get('longitude')
            latitude = self.request.query_params.get('latitude')
            offset = int(self.request.query_params.get('offset', 0))  # Default offset is 0
            limit = int(self.request.query_params.get('limit', 10))  # Default limit is 10
            
            qs = results_by_distance(latitude,longitude,offset,limit)
            serializer = RideSerializer(qs,many=True)

            return Response(serializer.data)
        except:
            return Response({'message':'400 Bad Request'}, status.HTTP_400_BAD_REQUEST)

class RideEventViewSet(viewsets.ModelViewSet):
    """A ViewSet for creating, listing, retrieving, updating, and deleting ride events."""

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
            return Response({'message':'400 Bad Request'}, status.HTTP_400_BAD_REQUEST)
         
    