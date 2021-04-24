import time
from datetime import timedelta
import asyncio
from asgiref.sync import sync_to_async
from django.conf import settings

# for RPi control
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

# for moisture sensors
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_seesaw.seesaw import Seesaw
from .models import Plant, Pump, SoilSensor, WateringLog

# for I2C bus
import board
import busio
from board import SCL, SDA
i2c_bus = busio.I2C(board.SCL, board.SDA)

# BCM pin numbers corresponding to the GPIO pins that fire the pumps on the HAT
ZONE_PINS = [13, 16, 19, 20, 26, 21]   

def getFullStatus():

	# read all pumps
	GPIO.setmode(GPIO.BCM)
	pumpStatus = {}
	for pump in Pump.objects.all():
		zonePin = ZONE_PINS[pump.zoneNumberOnHAT - 1]
		GPIO.setup(zonePin, GPIO.OUT)
		pumpStatus[pump.id] = GPIO.input(zonePin)
		
	# read all sensors
	sensorReadings = {}
	for sensor in SoilSensor.objects.all():
		currentMoisture = "N/A"
		
		try:
			soilSensor = Seesaw(i2c_bus, addr = int(sensor.i2cAddr, 16))	# convert "0x36" to int
			currentMoisture = soilSensor.moisture_read()
		except ValueError:
			currentMoisture = "** error **"
	
		sensorReadings[sensor.id] = currentMoisture
		
	# tie it all together in a plant-focused dict
	data = {}

	for plant in Plant.objects.all():
		pump = plant.pump
		sensor = plant.sensor
		
		latestLogs = WateringLog.objects.all() \
			.filter(plant_id = plant.id) \
			.values("logDateTime", "durationSeconds") \
			.order_by("-logDateTime")[:1]
	
		row = {
			"id": plant.id,
			"name": str(plant),
			"imageUrl": "",
			"waterSeconds": 10,
			"moisture":  "",
			"pump": "",
			"zone": "",
			"isRunning": False,
			"latestLog": None,
			"lastWatered": None,
			"nextWater": None
		}

		if (pump is not None):
			row["pump"] = str(pump)
			row["zone"] = pump.zoneNumberOnHAT
			row["isRunning"] = pumpStatus[pump.id]
			
		if (sensor is not None):
			row["moisture"] = sensorReadings[sensor.id]
			
		if (plant.image):
			row["imageUrl"] = plant.image.url
		
		if (len(latestLogs) > 0):
			latestLog = latestLogs[0]
			row["latestLog"] = latestLog
			row["lastWatered"] = latestLog["logDateTime"]
			row["nextWater"] = latestLog["logDateTime"] + timedelta(days = plant.waterFrequencyDays)
			
		data[plant.id] = row
	
	GPIO.cleanup()
	
	return data

def startPump(pump):
	GPIO.setmode(GPIO.BCM)
	zonePin = ZONE_PINS[pump.zoneNumberOnHAT - 1]
	GPIO.setup(zonePin, GPIO.OUT)
	GPIO.output(zonePin, GPIO.HIGH)

def stopPump(pump):
	GPIO.setmode(GPIO.BCM)
	zonePin = ZONE_PINS[pump.zoneNumberOnHAT - 1]
	GPIO.setup(zonePin, GPIO.OUT)
	GPIO.output(zonePin, GPIO.LOW)
	
def waterPlant(plantId, durationSeconds):
	plant = getPlant(plantId)
	
	if (plant.pump is None):
		return None
		
	log = WateringLog(
		plant_id=plant.id, 
		pump_id=plant.pump_id,
		sensor_id=plant.sensor_id,
		durationSeconds=durationSeconds,
		moistureLevel=None,
		triggeredBy="website")

	log.save()

	startPump(plant.pump)
	time.sleep(int(durationSeconds))
	stopPump(plant.pump)
	
	GPIO.cleanup()
	
	return log
	
def stopAllPumps():
	GPIO.setmode(GPIO.BCM)

	for zonePin in ZONE_PINS:
		GPIO.setup(zonePin, GPIO.OUT)
		GPIO.output(zonePin, GPIO.LOW)
		
	GPIO.cleanup()

def getPlant(id):
	return Plant.objects.get(pk=id)

