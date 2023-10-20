from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import generics, status

from tof.models import TofData, TofData1, TofData2, VizData, LdrData, VehicleInfo, IncidentData
from tof.serializer import TofDataSerializer, TofData1Serializer, TofData2Serializer, VisualDataSerializer, LdrDataSerializer, VehicleInfoSerializer, IncidentDataSerializer
from .models import Vehicles
from .serializer import VehiclesSerializer


class SyncAPIView(APIView):
    def post(self, request, format=None):
        batch_data = request.data['data']
        sensor_name = request.data['sensor_name']
        vehicle_id = request.data['vehicle_id']
        organization = request.data['organization']

        vehicle = Vehicles.objects.filter(vehicleId=vehicle_id, organization=organization)
        if vehicle.exists():
            vehicle_obj = vehicle[0]
        else:
            vehicle_obj = Vehicles.objects.create(vehicleId=vehicle_id, organization=organization)

        serializer_map = {
            'tofl': TofDataSerializer,
            'tofm': TofData1Serializer,
            'tofr': TofData2Serializer,
            'viz': VisualDataSerializer,
            'ldr': LdrDataSerializer,
            'incident': IncidentDataSerializer,
            'infos': VehicleInfoSerializer,
        }


        serializer_class = serializer_map.get(sensor_name)

        if not serializer_class:
            return Response({'error': 'Invalid sensor name provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Loop through the batch data and save using the serializer
        for data in batch_data:
            data['vehicle'] = vehicle_obj.id  # Add the vehicle foreign key to the data
            if sensor_name == 'infos' or sensor_name == 'incident':
                print(data)
            serializer = serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Saved', status=status.HTTP_201_CREATED)


class VehiclesListView(generics.ListAPIView):
    serializer_class = VehiclesSerializer

    def get_queryset(self):
        organization = self.request.GET.get('vehicleOrganization', "None")
        if organization != "None":
            return Vehicles.objects.filter(organization=organization).order_by('organization')
        else:
            return Vehicles.objects.all().order_by('organization')


class DeviceRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        organization = request.data.get('organization')
        vehicle_id = request.data.get('vehicle_id')

        # Check if the ID is acceptable.
        if Vehicles.objects.filter(vehicleId=vehicle_id, organization=organization).exists():
            return Response({"accept": False})

        # If acceptable, save the ID and organization to the database.
        print(organization, vehicle_id)
        Vehicles.objects.create(organization=organization, vehicleId=vehicle_id)
        return Response({"accept": True})