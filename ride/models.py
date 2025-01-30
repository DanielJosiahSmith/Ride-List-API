from django.db import models
from user.models import CustomUser

class Ride(models.Model):
    """Ride Model"""
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255)
    id_rider = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True,null=True,related_name='rides')
    id_driver = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True,null=True)
    pickup_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    dropoff_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    pickup_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id_ride)


class Ride_Event(models.Model):
    """Ride Events Model"""
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_ride_event)
