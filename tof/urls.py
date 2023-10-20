from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # Matches any html file
    # re_path(r'^(?!api).*\.*', views.pages, name='pages'),
    re_path(r'^.*\.html$', views.pages, name='pages'),

    # Frontend APIS
    path('api/sensordata/', views.SensorData.as_view(), name='sensor-data'),
    path('api/incidentsensordata/', views.IncidentSensorData.as_view(), name='incident-sensor-data'),
    path('api/incidents/', views.IncidentsList.as_view(), name='incident-data'),
    path('api/download_video/', views.download_video, name='download-video'),
    path('api/vehicle_info/', views.LastVehicleInfoView.as_view(), name='vehicle_info')
]