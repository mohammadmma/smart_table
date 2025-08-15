from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SensorDataSerializer
from .models import SensorData

# Create your views here.
class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
