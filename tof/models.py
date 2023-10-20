from django.db import models
from cloudapp.models import Vehicles


class TofData(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='tofl')
    value1 = models.IntegerField(null=True)
    value2 = models.IntegerField(null=True)
    value3 = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk} - Value1: {self.value1}, Value2: {self.value2}, Value3: {self.value3}'


class TofData1(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='tofm')
    value1 = models.IntegerField(null=True)
    value2 = models.IntegerField(null=True)
    value3 = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk} - Value1: {self.value1}, Value2: {self.value2}, Value3: {self.value3}'


class TofData2(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='tofr')
    value1 = models.IntegerField(null=True)
    value2 = models.IntegerField(null=True)
    value3 = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk} - Value1: {self.value1}, Value2: {self.value2}, Value3: {self.value3}'


class VizData(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='viz')
    value1 = models.IntegerField(null=True)
    value2 = models.CharField(null=True, max_length=50)
    value3 = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk} - Value1: {self.value1}, Value2: {self.value2}, Value3: {self.value3}'


class LdrData(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='ldr')
    value1 = models.IntegerField(null=True)
    value2 = models.IntegerField(null=True)
    value3 = models.IntegerField(null=True)
    value4 = models.IntegerField(null=True)
    value5 = models.IntegerField(null=True)
    value6 = models.IntegerField(null=True)
    value7 = models.IntegerField(null=True)
    value8 = models.IntegerField(null=True)
    value9 = models.IntegerField(null=True)
    value10 = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk}'


class IncidentData(models.Model):
    timestamp = models.DateTimeField()
    description = models.CharField(max_length=20, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='incident')

    LdrValue = models.ForeignKey(LdrData, null=True, blank=True, on_delete=models.CASCADE, related_name='ldr')
    TofmValue = models.ForeignKey(TofData, null=True, blank=True, on_delete=models.CASCADE, related_name='tofm')
    ToflValue = models.ForeignKey(TofData1, null=True, blank=True, on_delete=models.CASCADE, related_name='tofl')
    TofrValue = models.ForeignKey(TofData2, null=True, blank=True, on_delete=models.CASCADE, related_name='tofr')
    VizValue = models.ForeignKey(VizData, null=True, blank=True, on_delete=models.CASCADE, related_name='viz')

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    breakAction = models.BooleanField()
    override = models.BooleanField()
    speed = models.FloatField(default=0.0)
    zones = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.timestamp} - Vehicle: {self.vehicle.pk}'


class VehicleInfo(models.Model):
    timestamp = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='Info')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    mode = models.CharField(max_length=255, default='override')
    speed = models.FloatField(default=0.0)
    zones = models.CharField(max_length=255)


class Device(models.Model):
    DEVICE_TYPES = (
        ('LIDAR', 'Lidar'),
        ('TOF', 'Tof Camera'),
        ('VISUAL', 'Visual Camera'),
        ('OTHERS', 'Others'),
        ('LEGACY', 'Legacy'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    status = models.CharField(max_length=10)
    last_seen = models.DateTimeField()

    def __str__(self):
        return self.name


