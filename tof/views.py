import json
import os
from datetime import timedelta, datetime, time

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.template import loader
from django.urls import reverse
from django import template
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import TofData, TofData1, TofData2, VizData, LdrData, IncidentData, VehicleInfo
from .serializer import TofDataSerializer, TofData1Serializer, TofData2Serializer, VisualDataSerializer, \
    LdrDataSerializer, IncidentDataSerializer, VehicleInfoSerializer

import concurrent.futures
import requests


# Create your views here.
@login_required(login_url="users/login/")
def index(request):
    context = {'segment': 'dashboard'}
    # html_template = loader.get_template('home/dashboard.html')
    html_template = loader.get_template('pages/dashboard.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="users/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('pages/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class IncidentsList(generics.ListAPIView):
    serializer_class = IncidentDataSerializer

    def get_queryset(self):
        mode = self.request.query_params.get('mode')
        incident_id = self.request.query_params.get('incident_id')
        vehicle_id = self.request.query_params.get('vehicleId')
        organization = self.request.query_params.get('organization')

        if incident_id:
            return IncidentData.objects.filter(pk=incident_id)

        elif mode:
            if mode == 'daily':
                delta = timedelta(days=1)
                count = 10
            elif mode == 'weekly':
                delta = timedelta(weeks=1)
                count = 10
            elif mode == 'monthly':
                delta = timedelta(weeks=4)  # roughly a month
                count = 10
            else:
                return IncidentData.objects.none()  # Return an empty queryset if invalid mode

            # Assuming you just want to filter incidents and not count them for this example
            current_date = timezone.now().date()
            end_date = datetime.combine(current_date + delta, time(0, 0, 0, 0))
            start_date = end_date - delta * count

            return IncidentData.objects.filter(timestamp__range=(start_date, end_date), vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
        else:

            print(vehicle_id, organization)
            return IncidentData.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization)


class IncidentSensorData(generics.ListAPIView):

    def get_queryset(self):
        sensor_name = self.request.query_params.get('name')
        vehicle_id = self.request.query_params.get('vehicleId')
        organization = self.request.query_params.get('organization')
        timestamp_str = self.request.query_params.get('timestamp')

        # Convert the timestamp string into a datetime object
        timestamp_dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        # Create two datetime objects representing the two-minute bounds
        start_time = timestamp_dt - timedelta(minutes=5)
        end_time = timestamp_dt + timedelta(minutes=5)

        if sensor_name == 'tof':
            queryset = TofData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time, vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
            sorted_data = sorted(queryset, key=lambda x: abs((x.timestamp - timestamp_dt).total_seconds()))
            return sorted_data[:5]
            # return TofData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-id')[:5]
        elif sensor_name == 'tof1':
            queryset = TofData1.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time, vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
            sorted_data = sorted(queryset, key=lambda x: abs((x.timestamp - timestamp_dt).total_seconds()))
            return sorted_data[:5]
            # return TofData1.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-id')[:5]
        elif sensor_name == 'tof2':
            queryset = TofData2.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time, vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
            sorted_data = sorted(queryset, key=lambda x: abs((x.timestamp - timestamp_dt).total_seconds()))
            return sorted_data[:5]
            # return TofData2.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-id')[:5]
        elif sensor_name == 'visual':
            queryset = VizData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time, vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
            sorted_data = sorted(queryset, key=lambda x: abs((x.timestamp - timestamp_dt).total_seconds()))
            return sorted_data[:5]
            # return VizData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-id')[:5]
        elif 'ldr' in sensor_name:
            queryset = LdrData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time, vehicle__vehicleId=vehicle_id, vehicle__organization=organization)
            sorted_data = sorted(queryset, key=lambda x: abs((x.timestamp - timestamp_dt).total_seconds()))
            return sorted_data[:5]
            # return LdrData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time).order_by('-id')[:5]
        else:
            return None

    def get_serializer_class(self):
        sensor_name = self.request.query_params.get('name')

        if sensor_name == 'tof':
            return TofDataSerializer
        elif sensor_name == 'tof1':
            return TofData1Serializer
        elif sensor_name == 'tof2':
            return TofData2Serializer
        elif sensor_name == 'visual':
            return VisualDataSerializer
        elif 'ldr' in sensor_name:
            return LdrDataSerializer
        else:
            return None


class SensorData(generics.ListAPIView):

    def get_queryset(self):
        sensor_name = self.request.query_params.get('name')
        vehicle_id = self.request.query_params.get('vehicleId')
        organization = self.request.query_params.get('organization')

        if sensor_name == 'tof':
            return TofData.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).order_by('-timestamp')[:100]
        elif sensor_name == 'tof1':
            return TofData1.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).order_by('-timestamp')[:100]
        elif sensor_name == 'tof2':
            return TofData2.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).order_by('-timestamp')[:100]
        elif sensor_name == 'visual':
            return VizData.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).order_by('-timestamp')[:100]
        elif 'ldr' in sensor_name:
            return LdrData.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).order_by('-timestamp')[:100]
        else:
            return None

    def get_serializer_class(self):
        sensor_name = self.request.query_params.get('name')

        if sensor_name == 'tof':
            return TofDataSerializer
        elif sensor_name == 'tof1':
            return TofData1Serializer
        elif sensor_name == 'tof2':
            return TofData2Serializer
        elif sensor_name == 'visual':
            return VisualDataSerializer
        elif 'ldr' in sensor_name:
            return LdrDataSerializer
        else:
            return None


def find_closest_video(timestamp, video_dir='~/MyDir/buffer/'):
    min_diff = None
    closest_video = None

    for filename in os.listdir(video_dir):
        if filename.endswith(".avi"):  # Assuming all videos are mp4 files, modify as needed
            full_path = os.path.join(video_dir, filename)

            # Get file creation time
            creation_time = datetime.fromtimestamp(os.path.getctime(full_path))

            # Calculate time difference
            diff = abs((creation_time - timestamp).total_seconds())

            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_video = full_path

    return closest_video


def download_video(request):
    incident_id = request.GET.get('incident_id')

    if not incident_id:
        raise Http404("Incident ID not provided")

    # Assuming the video file name is based on the incident_id.
    timestamp = IncidentData.objects.filter(pk=incident_id)[0].timestamp
    # Adjust this path as needed based on how you store and name your videos.
    # video_path = os.path.join('../MyDir/buffer/video', f"{incident_id}.mp4")
    video_path = find_closest_video(timestamp)

    if not os.path.exists(video_path):
        raise Http404("Video not found")

    response = FileResponse(open(video_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="incident_{incident_id}.avi"'

    return response


class LastVehicleInfoView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            vehicle_id = self.request.query_params.get('vehicleId')
            organization = self.request.query_params.get('organization')

            latest_vehicle = VehicleInfo.objects.filter(vehicle__vehicleId=vehicle_id, vehicle__organization=organization).latest('id')  # Assuming 'id' is the auto-incremented field
            serializer = VehicleInfoSerializer(latest_vehicle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VehicleInfo.DoesNotExist:
            return Response({"detail": "No VehicleInfo data found."}, status=status.HTTP_404_NOT_FOUND)
