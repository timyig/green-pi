#!/usr/bin/env python3
"""
Module Docstring
"""

import os
import logging
import schedule
import time
from time import strftime
import Adafruit_DHT as dht
import random

from db import add_sensor_data

__author__ = "Timur Yigit"
__version__ = "0.1.0"
__license__ = "MIT"

logging.basicConfig(level=logging.DEBUG)
relay_script_path = os.environ.get("/pyt-8-Way-Relay-Board/k8_box.py")

'''
def job():
    add_sensor_data({
        'air_temp': round(random.uniform(1.0, 100.0), 2),
        'humidity': round(random.uniform(1.0, 100.0), 2),
        'moister': round(random.uniform(1.0, 100.0), 2)})
'''

# Get list all sensor GPIO pins stored in DB
def fetchSensorGPIO():

    logging.info("fetchSensorGPIO")
    # Format GPIO data for export
    data = {}
    data['climate_GPIO'] = 2
    return data


def getGrowData():

    GPIO = fetchSensorGPIO()

    data = {}
    data['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = fetchRawTemperature(GPIO['climate_GPIO'])
    data['humidity'] = fetchRawHumidity(GPIO['climate_GPIO'])
    '''
    data['moisture_status'] = getGPIOState(GPIO['moisture_GPIO'])
    '''
    logging.info(data)
    return data


def growDataUpdate(data):
    logging.info("Update DB")
    add_sensor_data({
        'air_temp': data['temperature'],
        'humidity': data['humidity'],
        'moister': round(random.uniform(1.0, 100.0), 2)})


# Fetch Raw Temperature
def fetchRawTemperature(gpioPIN):
    try:
        humidity, temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if temperature is not None:
            data_output = round(temperature, 2)
            logging.info(data_output)
            return data_output
        else:
            logging.info('Failed to get reading. Try again!')
    except Exception:
        logging.error("sensor error: ", exc_info=True)

# Fetch Raw Humidity
def fetchRawHumidity(gpioPIN):
    try:
        humidity,temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if humidity is not None and humidity <= 100:
            data_output = round(humidity, 2)
            logging.info(data_output)
            return data_output
        else:
            logging.info('Failed to get reading. Try again!')
    except Exception:
        logging.error("sensor error: ", exc_info=True)

'''
def setLight():
    GPIO = fetchSensorGPIO()
    logging.info(GPIO)
    logging.info(GPIO['climate_GPIO'])
    os.system("python " + "/pyt-8-Way-Relay-Board/k8_box.py" + " set-relay -r " + str(2) + " -s 1")
'''

schedule.every(1).minutes.do(getGrowData)
#schedule.every(10).seconds.do(setLight)


while True:
    schedule.run_pending()
    time.sleep(1)
