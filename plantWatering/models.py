from django.db import models

class Pump(models.Model):
	PUMP_TYPES = [
		('12V', '12V')
	]

	id = models.IntegerField(primary_key=True)
	description = models.CharField(max_length=50, null=True, blank=True)
	type = models.CharField(max_length=10, choices=PUMP_TYPES)
	zoneNumberOnHAT = models.IntegerField()
	
	def __str__(self):
		return 'Pump #' + str(self.id)
	
class SoilSensor(models.Model):
	SENSOR_TYPES = [
		('ANALOG', 'Analog'),
		('I2C', 'I2C')
	]

	id = models.IntegerField(primary_key=True)
	description = models.CharField(max_length=50, null=True, blank=True)
	type = models.CharField(max_length=10, choices=SENSOR_TYPES)
	i2cAddr = models.CharField(max_length=5, null=True, blank=True)
	analogInputNumber = models.IntegerField(null=True, blank=True)
	
	def __str__(self):
		return 'Sensor #' + str(self.id)
	
class Plant(models.Model):
	id = models.IntegerField(primary_key=True)
	description = models.CharField(max_length=50, null=True, blank=True)
	pump = models.ForeignKey(Pump, on_delete=models.SET_NULL, null=True, blank=True)
	sensor = models.ForeignKey(SoilSensor, on_delete=models.SET_NULL, null=True, blank=True)
	
	def __str__(self):
		return 'Plant #' + str(self.id)

class WateringLog(models.Model):
	logDateTime = models.DateTimeField(auto_now=False, auto_now_add=True)
	plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=False, blank=False)
	pump = models.ForeignKey(Pump, on_delete=models.CASCADE, null=False, blank=False)
	sensor = models.ForeignKey(SoilSensor, on_delete=models.CASCADE, null=True, blank=True)
	durationSeconds = models.IntegerField(null=False, blank=False)
	moistureLevel = models.IntegerField(null=True, blank=True)
	triggeredBy = models.CharField(max_length=50, null=False, blank=False, default="System")
	
	def __str__(self):
		return 'Log #' + str(self.id) + ' (' + self.logDateTime.strftime("%Y%m%d:%H%M%S") + ')'
	