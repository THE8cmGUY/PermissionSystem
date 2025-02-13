from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from .models import *




# Create your views here.
class AuthViewSet(viewsets.ViewSet):
    @action (detail=False , methods = ['post'])
    def register(self , request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
           user =  serializer.save()
           return Response(UserRegisterSerializer(user))
        return Response(serializer.errors)

