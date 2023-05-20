from django.shortcuts import render
from django.views.generic import View
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

import joblib
from machinelearning import LinregML

from .models import Sensor, SensorLog, Actuator, ActuatorLog

class SensorTemplateView(APIView):
    sensor_name = ""
    def get(self, request, format=None):
        sensor = Sensor.objects.get(name=self.sensor_name)
        data = {
            "value": sensor.value
        }
        return Response(data)

class ActuatorTemplateView(APIView):
    actuator_name = ""
    sensor1_name  = ""
    sensor2_name  = ""
    sensor3_name  = ""
    training_csv  = ""
    def get(self, request, format=None):
        actuator = Actuator.objects.get(name=self.actuator_name)
        sensor1  = Sensor.objects.get(name=self.sensor1_name)
        sensor2  = Sensor.objects.get(name=self.sensor2_name)
        sensor3  = Sensor.objects.get(name=self.sensor3_name)
        model = LinregML.BaseLinearRegression(settings.ML_ROOT + self.training_csv)
        prediction = model.predict([float(sensor1.value), float(sensor2.value), float(sensor3.value)])
        actuator.state = int(prediction)
        actuator.save()
        data = {
            "state": actuator.state
        }
        return Response(data)

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

# Smart Farm ==========================================================================================================================================
# Susu Hewani dan Telur
class SensorMoistureView(SensorTemplateView):
    sensor_name = "Soil Moisture Sensor"
    
class SensorTemperatureView(SensorTemplateView):
    sensor_name = "Temperature Sensor"

class SensorLightView(SensorTemplateView):
    sensor_name = "Light Level Sensor"
    
class actuator1view(ActuatorTemplateView):
    actuator_name = "actuator1"
    sensor1_name = "Soil Moisture Sensor"
    sensor2_name = "Temperature Sensor"
    sensor3_name = "Light Level Sensor"
    training_csv = "actuator1.csv"