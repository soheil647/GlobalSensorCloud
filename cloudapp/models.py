from django.db import models


# Create your models here.
class Vehicles(models.Model):
    vehicleId = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)

    def __str__(self):
        return "Vehicle Id: " + self.vehicleId
