from django.core.management.base import BaseCommand, CommandError
from user.models import CustomUser
from ride.models import Ride, Ride_Event

import random
from faker import Faker
from random import randrange

from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "generate test data"


    def handle(self, *args, **options):
            
            roles = ['admin','driver','rider']
            statuses = ['en-route','pick_up','dropoff']
            descriptions = ['Status changed to pickup','Status changed to dropoff']
            370000000-380000000
            1220000000-1230000000
            fake = Faker()

            users = []
            for i in range(1000):
                user = CustomUser(
                    role=random.choice(roles),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone_number=fake.phone_number(),
                    )
                users.append(user)
            
            CustomUser.objects.bulk_create(users,ignore_conflicts=True)

            rides = []
            for i in range(2000):
                ride = Ride(
                     status=random.choice(statuses),
                     id_rider_id=randrange(1,1000),
                     id_driver_id=randrange(1,1000),
                     pickup_latitude=randrange(370000000,380000000)/10000000,
                     pickup_longitude=randrange(1220000000,1230000000)/10000000,
                     dropoff_latitude=randrange(370000000,380000000)/10000000,
                     dropoff_longitude=randrange(1220000000,1230000000)/10000000,
                     pickup_time=now() - timedelta(minutes=randrange(1,200))
                )

                rides.append(ride)

            Ride.objects.bulk_create(rides,ignore_conflicts=True)

            ride_events = []
            for i in range(5000):
                ride_event = Ride_Event(
                    id_ride_id = randrange(1,2000),
                    description = random.choice(descriptions)
                )
            
                ride_events.append(ride_event)
            

            Ride_Event.objects.bulk_create(ride_events,ignore_conflicts=True)
                
                
            
            
            self.stdout.write(
                self.style.SUCCESS('Test Data Generated!')
            )
