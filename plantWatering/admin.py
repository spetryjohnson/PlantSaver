from django.contrib import admin

from .models import Plant, Pump, SoilSensor, WateringLog

admin.site.register(Plant)
admin.site.register(Pump)
admin.site.register(SoilSensor)
admin.site.register(WateringLog)

