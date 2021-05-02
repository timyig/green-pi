#!/usr/bin/env python3

# import os
import logging
import schedule
import time
import datetime
from time import strftime
import random

# TODO Add rolling average https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# from db import add_sensor_data, get_schedules, SensorEnum
from relay import update_relay, init_relay, ON, OFF
# from app import create_app


# logger = logging.getLogger(__file__)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger("green-pi")


try:
    import Adafruit_DHT as dht
    logger.info('Adafruit DHT imported')
except (ImportError, ModuleNotFoundError):
    logger.error('Was not able to import Adafruit_DHT')

CLIMATE_GPIO = 2
NO_SENSOR_DATA = 404
LIGHT_ON_EVENT = datetime.time(20, 32, 0)
logger.debug('Heating starts at : ', LIGHT_ON_EVENT.hour)
LIGHT_OFF_EVENT = datetime.time(10, 0, 0)

sensor_data = {
    "temperature": NO_SENSOR_DATA,
    "humidity": NO_SENSOR_DATA
}


# Fetch Raw Temperature
def fetch_temperature_and_humidity(gpioPIN):
    try:
        humidity, temperature = dht.read_retry(dht.DHT22, int(gpioPIN))
        if temperature is not None:
            temperature = round(temperature, 2)
        if humidity is not None:
            humidity = round(humidity, 2)
        if humidity is None or temperature is None:
            logger.error('Failed to get reading. Try again!')
        return humidity, temperature
    except Exception:
        logger.error("sensor error: ", exc_info=True)
        return None, None


def fetch_sensors():
    humidity, temperature = fetch_temperature_and_humidity(CLIMATE_GPIO)
    return {
        'timestamp': strftime("%Y-%m-%d %H:%M:%S"),
        'temperature': temperature,
        'humidity': humidity,
        # No sensor implemented yet
        'moister': round(random.uniform(50.0, 70.0), 2)
    }


def update_sensor_data():
    try:
        logger.debug("Update DB")
        data = fetch_sensors()
        if data['temperature'] is not None:
            sensor_data["temperature"] = data['temperature']
        if data['humidity'] is not None:
            sensor_data["humidity"] = data['humidity']

        '''
        add_sensor_data({
            'air_temp': data['temperature'],
            'humidity': data['humidity'],
            'moister': data['humidity'],
        })
        '''
        logger.debug('Last sensors reading: temperature {temperature}, humidity {humidity}'
                     .format(temperature=sensor_data["temperature"],
                             humidity=sensor_data["humidity"]))
    except BaseException:
        logger.error("updateSensorData error: ", exc_info=True)


def set_light_state():
    logger.debug('Setting Light State')
    current_time = datetime.datetime.now().time()
    time_state = ON

    if current_time > LIGHT_OFF_EVENT and current_time < LIGHT_ON_EVENT:
        time_state = OFF

    logger.debug('time_state is {time_state}'.format(time_state=time_state))


def get_sensor_state(sensor_value, last_state, sensor_min, sensor_max, inverted=False):
    lower_state = ON if inverted else OFF
    upper_state = OFF if inverted else ON
    if sensor_value <= sensor_min and last_state == lower_state:
        return OFF if inverted else ON
    elif sensor_value >= sensor_max and last_state == upper_state:
        return ON if inverted else OFF
    else:
        return last_state


'''
def get_updated_state(schd):
    current_time = datetime.now().time()
    time_state = ON if current_time >= schd.start_schedule and current_time < schd.end_schedule else OFF
    if schd.sensor is None:
        return time_state
    sensor_data = fetch_sensors()
    humidity = sensor_data.get('humidity')
    temperature = sensor_data.get('temperature')
    logger.debug('Last sensors reading: temperature {temperature}, humidity {humidity}'.format(
        temperature=temperature, humidity=humidity))
    sensor_state = OFF
    if schd.sensor == SensorEnum.SensorTemperature and temperature is not None:
        sensor_state = get_sensor_state(temperature, schd.last_state, schd.sensor_min, schd.sensor_max)
    if schd.sensor == SensorEnum.SensorHumidity and humidity is not None:
        sensor_state = get_sensor_state(humidity, schd.last_state, schd.sensor_min, schd.sensor_max)
    return ON if time_state == ON and sensor_state == ON else OFF
'''


'''
def updated_relay_state(schd):
    current_time = datetime.now().time()
    time_state = ON if current_time >= schd.start_schedule and current_time < schd.end_schedule else OFF
    if schd.sensor is None:
        return time_state
    sensor_data = fetch_sensors()
    humidity = sensor_data.get('humidity')
    temperature = sensor_data.get('temperature')
    logger.debug('Last sensors reading: temperature {temperature}, humidity {humidity}'.format(
        temperature=temperature, humidity=humidity))
    sensor_state = OFF
    if schd.sensor == SensorEnum.SensorTemperature and temperature is not None:
        sensor_state = get_sensor_state(temperature, schd.last_state, schd.sensor_min, schd.sensor_max)
    if schd.sensor == SensorEnum.SensorHumidity and humidity is not None:
        sensor_state = get_sensor_state(humidity, schd.last_state, schd.sensor_min, schd.sensor_max)
    return ON if time_state == ON and sensor_state == ON else OFF
'''


'''
def schedule_job():
    try:
        logger.debug("scheduleJob")
        events = get_schedules()
        for e in events:
            logger.debug('Processing event with Start time {start} and Endtime {end}, device_id {device_id}, '
                'Sensor {sensor}, min {sensor_min}, max {sensor_max}'.format(
                    start=e.start_schedule, end=e.end_schedule, device_id=e.device_id,
                    sensor=e.sensor, sensor_min=e.sensor_min, sensor_max=e.sensor_max))
            state = get_updated_state(e)
            logger.debug('State should be {state}'.format(state='ON' if state == ON else 'OFF'))
            if state != e.last_state:
                update_relay(e.id, e.device_id, state)
    except BaseException:
        logger.error("scheduleJob error: ", exc_info=True)
'''


'''
def schedule_job():
    try:
        logger.debug("scheduleJob")
        events = get_schedules()
        for e in events:
            logger.debug('Processing event with Start time {start} and Endtime {end}, device_id {device_id}, '
                'Sensor {sensor}, min {sensor_min}, max {sensor_max}'.format(
                    start=e.start_schedule, end=e.end_schedule, device_id=e.device_id,
                    sensor=e.sensor, sensor_min=e.sensor_min, sensor_max=e.sensor_max))
            state = get_updated_state(e)
            logger.debug('State should be {state}'.format(state='ON' if state == ON else 'OFF'))
            if state != e.last_state:
                update_relay(e.id, e.device_id, state)
    except BaseException:
        logger.error("scheduleJob error: ", exc_info=True)
'''


def run_scheduler():
    init_relay()
    logger.debug("Initaized relays")
    while True:
        schedule.run_pending()
        time.sleep(1)


logger.info("Starting green_pi service")
# schedule.every(1).minutes.do(update_sensor_data)
schedule.every(30).seconds.do(update_sensor_data)
schedule.every(10).seconds.do(set_light_state)
# schedule.every(1).seconds.do(schedule_job)

run_scheduler()
