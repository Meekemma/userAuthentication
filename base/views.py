from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistationSerializer,changePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes,parser_classes,renderer_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
# Create your views here.
@api_view(['POST'])
def registration_view(request):
    serializer = RegistationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Custom serializer for obtaining JWT token with additional claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_verified'] = user.is_verified
        

        return token
    
# validate method is overridden to add extra responses to the data returned by the parent class's validate method.
    def validate(self, attrs):
        # Normalize the email to lowercase before validation
        attrs['email'] = attrs['email'].lower()
        # call validates the provided attributes using the parent class's validate method and returns the validated data.
        data = super().validate(attrs)

        # Add extra responses
        # Adds the user id to the response
        data.update({'user_id': self.user.id})
        full_name = f"{self.user.first_name} {self.user.last_name}"
        data.update({'full_name': full_name})
        data.update({'email': self.user.email})
        data.update({'is_verified': self.user.is_verified})

        return data

       
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer 



#change password view
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePasswordView(request):
    """
    API endpoint to change the password of the authenticated user.
    """
    if request.method == 'PUT':
        serializer=changePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to changed password", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
