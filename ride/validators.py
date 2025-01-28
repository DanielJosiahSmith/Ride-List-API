from user.models import CustomUser

def validate_new_ride(data):
        try:
            status = data['status']
            id_rider = data['id_rider']
            id_driver = data['id_driver']
            pickup_latitude = data['pickup_latitude']
            pickup_longitude = data['pickup_longitude']
            dropoff_latitude = data['dropoff_latitude']
            dropoff_longitude = data['dropoff_longitude']


            
            if (CustomUser.objects.filter(user_id=id_rider).exists() == False or 
                CustomUser.objects.filter(user_id=id_driver).exists() == False):
                
                return False, "Invalid Driver or Rider Id"
            
            try:
                #test if valid float
                 float(pickup_latitude)
                 float(pickup_longitude)
                 float(dropoff_latitude)
                 float(dropoff_longitude)
            except:
                 return False, "Invalid latitude/longitutd data"

            return True, "Valid"
                 
                 
        except:
            return False, 'Error. Invalid data'
