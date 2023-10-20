from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializerWithToken

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@csrf_exempt
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            username = data['username'].lower(),
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except: 
        message = {"Details": "The user with current username already exists."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_profile(request):
    data = request.data
    profile = request.user.profile
    profile.username = data['username']
    profile.name = data['name']
    profile.email = data['email']
    profile.birth_date = data['birth_date']
    profile.phone_number = data['phone_number']
    profile.save()
    return Response("Your profile has been updated successfully.")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    data = request.data
    user = request.user

    old_password = data['old_password']
    new_password = data['new_password']
    if not check_password(old_password, user.password):
        message = {"Details": "Your old password is wrong."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    user.password = new_password
    message = {"Details": "Your password has changed successfully."}
    return Response(message, status=status.HTTP_202_ACCEPTED)
    