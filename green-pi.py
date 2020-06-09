#!/usr/bin/env python3
"""
Module Docstring
"""

import schedule
import time
from time import strftime
import Adafruit_DHT as dht
import random

from db import add_sensor_data

__author__ = "Timur Yigit"
__version__ = "0.1.0"
__license__ = "MIT"


def job():
    add_sensor_data({
        'air_temp': round(random.uniform(1.0, 100.0), 2),
        'humidity': round(random.uniform(1.0, 100.0), 2),
        'moister': round(random.uniform(1.0, 100.0), 2)})


# Get list all sensor GPIO pins stored in DB
def fetchSensorGPIO():

    # Format GPIO data for export
    data = {}
    data['climate_GPIO'] = 2
    return data


def getGrowData():

    GPIO = fetchSensorGPIO()

    data = {}
    data['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = fetchRawTemperature(GPIO['climate_GPIO'])
    '''
    data['humidity'] = fetchRawHumidity(GPIO['climate_GPIO'])
    data['light_status'] = getGPIOState(GPIO['light_GPIO'])
    data['moisture_status'] = getGPIOState(GPIO['moisture_GPIO'])
    data['fan_status'] = getGPIOState(GPIO['fan_GPIO'])
    data['pump_status'] = getGPIOState(GPIO['pump_GPIO'])
    '''
    print(data)
    return data


def growDataUpdate(data):
    print("Update DB")


# Fetch Raw Temperature
def fetchRawTemperature(gpioPIN):
    try:
        humidity, temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if temperature is not None:
            data_output = round(temperature, 2)
            print(data_output)
            return data_output
        else:
            print('Failed to get reading. Try again!')
    except:
        print("Sensor Error!")


schedule.every(1).minutes.do(getGrowData)

while True:
    print("ah faaa")
    schedule.run_pending()
    time.sleep(1)
