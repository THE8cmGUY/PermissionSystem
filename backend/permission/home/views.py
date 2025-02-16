from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token




# Create your views here.
class AuthViewSet(viewsets.ViewSet):
    @action (detail=False , methods = ['post'])
    def register(self , request):
        serializer = RegistrationSerializer(data = request.data)
    
        if serializer.is_valid():
           user =  serializer.save()
           
           return Response(UserRegisterSerializer(user).data)
           
        return Response(serializer.errors)
    @action (detail=False , methods = ['post'])
    def login(self , request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            username  = request.data.get['username']
            password = request.data.get['password']
            user = authenticate(request , username = username , password = password)
            if user :
                token , _ = Token.objects.create(user = user)
                data  = UserRegisterSerializer(user).data
                data['token'] = token.key
                return Response(data)
            else:
                return Response({"message":"Wrong credential entered"})


            return Response(UserRegisterSerializer(user).data)
        return Response(serializer.errors)
        



