from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view()),

#Smart Farm
    path('sfarm/moisture', views.SensorMoistureView.as_view()),
    path('sfarm/temp', views.SensorTemperatureView.as_view()),
    path('sfarm/light', views.SensorLightView.as_view()),
    path('actuator/actuator1', views.actuator1view.as_view()),
]