from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SensorDataSerializer
from .models import SensorData
from .tasks import handle_device_event

# Create your views here.
class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        sound_value = request.data.get("loudness_value")
        pressure_pulse = request.data.get("is_sitting")
        handle_device_event.delay(sound_value, pressure_pulse)
        
        return super().create(request, *args, **kwargs)
