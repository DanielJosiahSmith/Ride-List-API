from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated

from .validators import validate_custom_user

class UserViewSet(viewsets.ModelViewSet):
    """A ViewSet for creating, listing, retrieving, updating, and deleting users."""
     
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    
    def create(self, request):
        """override default create method with validation and token creation"""
        try:
            valid,msg = validate_custom_user(request.data)

            if valid:
                user = CustomUser.objects.create(
                                        role=request.data['role'],
                                        first_name=request.data['first_name'],
                                        last_name=request.data['last_name'],
                                        email=request.data['email'],
                                        phone_number=request.data['phone_number']
                                        )
                token = None
                if request.data['role'].lower() == 'admin':
                    #create token 
                    token = Token.objects.create(user=user).key
                    
                return Response({'role':f'{user.role}','msg':f'{user.user_id} - user created','token':token}, status=status.HTTP_201_CREATED)
            else:
                #if data not valid from validator
                return Response({'message':msg}, status.HTTP_400_BAD_REQUEST)
        except:
            #if user creation fails
            #log exception
            return Response({'message':'400 Bad Request'}, status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]