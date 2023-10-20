from django.contrib import admin

from .models import TofData, TofData1, TofData2, VizData, LdrData, IncidentData, VehicleInfo

# Register your models here.
admin.site.register(TofData)
admin.site.register(TofData1)
admin.site.register(TofData2)
admin.site.register(VizData)
admin.site.register(LdrData)
admin.site.register(IncidentData)
admin.site.register(VehicleInfo)