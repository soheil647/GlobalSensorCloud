from rest_framework import serializers
from .models import TofData, TofData1, TofData2, VizData, LdrData, IncidentData, VehicleInfo


class VehicleInfoSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = VehicleInfo
        fields = "__all__"


class IncidentDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = IncidentData
        fields = "__all__"


class TofDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TofData
        fields = "__all__"


class TofData1Serializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TofData1
        fields = "__all__"


class TofData2Serializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TofData2
        fields = "__all__"


class VisualDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = VizData
        fields = "__all__"


class LdrDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = LdrData
        fields = "__all__"
