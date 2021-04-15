# https://www.guguweb.com/2019/11/21/django-asynchronous-tasks-without-celery'
# ABANDONED for the moment; getting uwsgi running was more complex than expected
import logging
import time

# for RPi control
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

try:
    from uwsgidecorators import spool
except:
    def spool(func):
        def func_wrapper(**arguments):
            return func(arguments)
        return func_wrapper
 
import django
django.setup()
 
#from .models import Model1
 
logger = logging.getLogger(__name__)
 
@spool
def turnZoneOnAndSleep(arguments):
    zone = arguments['zone']
	seconds = arguments['seconds']
	testMode = arguments['testMode']
	
	GPIO.setmode(GPIO.BCM)
	zonePins = [13, 15, 19, 20, 26, 21]   #BCM pin numbers
	zonePin = zonePins[int(zone) - 1]
	
	GPIO.setup(zonePin, GPIO.OUT)

	if (not testMode): 
		GPIO.output(zonePin, GPIO.HIGH)
		
	time.sleep(int(seconds))
	GPIO.output(zonePin, GPIO.LOW)
