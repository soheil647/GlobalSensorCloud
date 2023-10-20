from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/sync/', views.SyncAPIView.as_view(), name='sync-data'),
    path('api/index/vehicles/', views.VehiclesListView.as_view(), name='vehicles-list'),
    path('api/registerVehicle/', views.DeviceRegistrationView.as_view(), name='register-vehicle'),
]