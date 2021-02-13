#!/usr/bin/env python3
"""
Module Docstring
"""

import os
import logging
import schedule
import time
from datetime import datetime
from time import strftime
from gpiozero import LED
import random

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

if os.environ.get('MY_ENV') != 'TEST':
    try:
        from db import add_sensor_data
        from db import get_schedules
        from db import update_schedule
    except ImportError:
        logging.error('Could not import db API module')

__author__ = "Timur Yigit"
__version__ = "0.1.0"
__license__ = "MIT"


try:
    import Adafruit_DHT as dht
except BaseException:
    logging.error('Was not able to import Adafruit_DHT')

RELAY1 = LED(21)
RELAY2 = LED(20)
RELAY3 = LED(16)
RELAY4 = LED(12)
RELAY1.ON()
RELAY2.ON()
RELAY3.ON()
RELAY4.ON()

OFF = 0
ON = 1
TEMP_SENSOR_GPIO = 2
# Temperature defines
LIGHT_RELAY = 1
FAN_RELAY = 2
HEATER_RELAY = 3

NIGHT_TEMP = 17
DAY_TEMP = 22
heater_state = OFF
# Used to store temp and humid. values from DMT Sensor
dmt_data = {}

'''
def job():
    add_sensor_data({
        'air_temp': round(random.uniform(1.0, 100.0), 2),
        'humidity': round(random.uniform(1.0, 100.0), 2),
        'moister': round(random.uniform(1.0, 100.0), 2)})
'''


def setRelay(device, state):
    global RELAY1
    global RELAY2
    global RELAY3
    global RELAY4
    global OFF
    global ON

    logging.debug('setRelay {device} and Endtime {state}'.format(
                  device=device, state=state))
    if device == 1:
        relay = RELAY1
    elif device == 2:
        relay = RELAY2
    elif device == 3:
        relay = RELAY3
    elif device == 4:
        relay = RELAY4

    if state == OFF:
        relay.ON()
    elif state == ON:
        relay.OFF()


def tempControlService():
    global dmt_data
    global heater_state

    logging.debug('tempControllService')
    print(dmt_data)
    if dmt_data['temperature'] < NIGHT_TEMP - 1.5:
        if heater_state == OFF:
            logging.debug('Activating heating')
            setRelay(HEATER_RELAY, state=ON)
            heater_state = ON
        else:
            logging.debug('Heater running')
    elif dmt_data['temperature'] > NIGHT_TEMP + 1.5:
        if heater_state == ON:
            logging.debug('Deactivating heating')
            setRelay(HEATER_RELAY, state=OFF)
            heater_state = OFF
        else:
            logging.debug('Heater is off')
    else:
        logging.debug('Temperture OK')


# Get list all sensor GPIO pins stored in DB
def fetchSensorGPIO():

    logging.info("fetchSensorGPIO")
    # Format GPIO data for export
    data = {}
    data['climate_GPIO'] = TEMP_SENSOR_GPIO
    return data


def getGrowData():
    global dmt_data
    logging.debug("getGrowData")
    # TODO fetch Sensor GPIO only needs to be called once
    GPIO = fetchSensorGPIO()
    data = {}
    data['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
    data['temperature'] = fetchRawTemperature(GPIO['climate_GPIO'])
    data['humidity'] = fetchRawHumidity(GPIO['climate_GPIO'])
    '''
    data['moisture_status'] = getGPIOState(GPIO['moisture_GPIO'])
    '''
    dmt_data = data
    return data


def growDataUpdate(data):
    logging.info("Update DB")
    data = getGrowData()
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
            logging.info('Failed to get temperature reading. Try again!')
    except Exception:
        logging.error("sensor error: ", exc_info=True)


# Fetch Raw Humidity
def fetchRawHumidity(gpioPIN):
    try:
        humidity, temperature = dht.read_retry(dht.DHT22, int(gpioPIN))

        if humidity is not None and humidity <= 100:
            data_output = round(humidity, 2)
            logging.info(data_output)
            return data_output
        else:
            logging.info('Failed to get humidity reading. Try again!')
    except Exception:
        logging.error("sensor error: ", exc_info=True)


def scheduleJob():
    logging.debug("scheduleJob")
    events = get_schedules()
    current_time = datetime.now().time()

    for e in events:
        state = OFF
        logging.debug('Processing event with Start time {start} and Endtime {end}'.format(
            start=e.start_schedule, end=e.end_schedule))
        if current_time > e.start_schedule and current_time <= e.end_schedule:
            logging.debug("Setting relay state to ON for: %d", e.device_id)
            state = ON
        else:
            logging.debug("Setting relay state to OFF for: %d", e.device_id)
            state = OFF
        if state != e.last_state:
            setRelay(e.device, state)
            logging.debug("Setting relay %d to %d", e.device_id, state)
            update_schedule(e.id, device_id=e.device_id, last_state=state)


if os.environ.get('MY_ENV') != 'TEST':
    schedule.every(1).minutes.do(growDataUpdate)
    schedule.every(1).seconds.do(scheduleJob)

schedule.every(1).seconds.do(getGrowData)
schedule.every(5).seconds.do(tempControlService)


while True:
    schedule.run_pending()
    time.sleep(1)
