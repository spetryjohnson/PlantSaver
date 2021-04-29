import time
import json
import asyncio

from distutils import util
from django.shortcuts import render 
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.contrib import messages

from plantWatering import IrrigationHelper
from plantWatering.models import Plant

import paho.mqtt.client as mqtt

def index(request):
	context = {
		'plants': IrrigationHelper.getFullStatus()
	}
	template = loader.get_template('plantWatering/index.html')
	return HttpResponse(template.render(context, request))

def waterPlant(request):
	plantId = request.GET.get('plantId', '1')
	seconds = request.GET.get('seconds', '0')
	
	log = IrrigationHelper.waterPlant(plantId, seconds)

	return JsonResponse({ "plantId": log.plant_id })

def stopAllPumps(request):
	IrrigationHelper.stopAllPumps()
	return HttpResponse("All pumps stopped")
	
def pushStatusToMQTT(request):
	plants = IrrigationHelper.getFullStatus()
	
	mqttClient = mqtt.Client("PlantSaver")
	mqttClient.connect("mqtt.pj-home.tech")	
	
	for plantId, plant in plants.items():
		mqttClient.publish("home/plants/plant%i/nextWater" % (plant["id"]), str(plant["nextWater"]), retain=True)
	
	mqttClient.disconnect()	
	
	return HttpResponse("done")