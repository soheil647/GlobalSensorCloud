from rest_framework import serializers
from .models import Vehicles


class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = "__all__"
