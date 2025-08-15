from django.db import models

# Create your models here.

class SensorData(models.Model):
    loudness_value = models.FloatField()
    is_sitting = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"loudness = {self.loudness_value}, is someone sitting = {self.is_sitting}, timestamp = {self.timestamp}"
    