from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_custom_user(data):
        """verify data exists and valid email"""
        try:
            role = data['role']
            f_name = data['first_name']
            l_name = data['last_name']
            email = data['email']
            phone = data['phone_number']

            try:
                validate_email(email)
            except ValidationError as e:
                return False, 'invalid email'
            

            if role and f_name and l_name and email and phone:
                return True, 'valid'
        except:
             return False, 'Error. required fields: role, first_name, last_name, email, phone_number'
        
