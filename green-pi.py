#!/usr/bin/env python3

import os
import logging
import schedule
import time
from datetime import datetime
from time import strftime
import random

from db import db, add_sensor_data, get_schedules, update_schedule, SensorEnum
from flask import Flask
from relay import set_relay, ON, OFF


try:
    import Adafruit_DHT as dht
except BaseException:
    logging.error('Was not able to import Adafruit_DHT')

relay_script_path = os.environ.get("/pyt-8-Way-Relay-Board/k8_box.py")


CLIMATE_GPIO = 2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('GREEN_PI_DB_CONNECTION')
db.init_app(app)


# Fetch Raw Temperature
def fetch_temperature_and_humidity(gpioPIN):
    try:
        humidity, temperature = dht.read_retry(dht.DHT22, int(gpioPIN))
        if temperature is not None:
            temperature = round(temperature, 2)
        if humidity is not None:
            humidity = round(humidity, 2)
        if humidity is None or temperature is None:
            logging.error('Failed to get reading. Try again!')
        return humidity, temperature
    except Exception:
        logging.error("sensor error: ", exc_info=True)
        return None, None


def fetch_sensors():
    humidity, temperature = fetch_temperature_and_humidity(CLIMATE_GPIO)
    return {
        'timestamp': strftime("%Y-%m-%d %H:%M:%S"),
        'temperature': temperature,
        # 'moister': getGPIOState(MOISTURE_GPIO),
        'moister': round(random.uniform(1.0, 100.0), 2),
        'humidity': humidity
    }


def updateSensorData():
    try:
        logging.info("Update DB")
        data = fetch_sensors()
        add_sensor_data({
            'air_temp': data['temperature'],
            'humidity': data['humidity'],
            'moister': data['humidity'],
        })
        return data
    except BaseException:
        logging.error("updateSensorData error: ", exc_info=True)


def get_sensor_state(sensor_value, last_state, sensor_min, sensor_max, inverted=False):
    lower_state = ON if inverted else OFF
    upper_state = OFF if inverted else ON
    if sensor_value < sensor_min and last_state == lower_state:
        return OFF if inverted else ON
    elif sensor_value > sensor_max and last_state == upper_state:
        return ON if inverted else OFF


def get_updated_state(schd):
    current_time = datetime.now().time()
    time_state = ON if current_time >= schd.start_schedule and current_time < schd.end_schedule else OFF
    if schd.sensor is None:
        return time_state
    sensor_data = fetch_sensors()
    humidity = sensor_data.get('humidity')
    temperature = sensor_data.get('temperature')
    logging.debug('Last sensors reading: temperature {temperature}, humidity {humidity}'.format(
        temperature=temperature, humidity=humidity))
    sensor_state = OFF
    if schd.sensor == SensorEnum.SensorTemperature and temperature is not None:
        sensor_state = get_sensor_state(temperature, schd.last_state, schd.sensor_min, schd.sensor_max)
    if schd.sensor == SensorEnum.SensorHumidity and humidity is not None:
        sensor_state = get_sensor_state(humidity, schd.last_state, schd.sensor_min, schd.sensor_max)
    return ON if time_state == ON and sensor_state == ON else OFF


def scheduleJob():
    try:
        logging.debug("scheduleJob")
        events = get_schedules()
        for e in events:
            logging.debug('Processing event with Start time {start} and Endtime {end}, device_id {device_id}, '
                'Sensor {sensor}, min {sensor_min}, max {sensor_max}'.format(
                    start=e.start_schedule, end=e.end_schedule, device_id=e.device_id, 
                    sensor=e.sensor, sensor_min=e.sensor_min, sensor_max=e.sensor_max))
            state = get_updated_state(e)
            logging.debug('State should be {state}'.format(state='ON' if state == ON else 'OFF'))
            if state != e.last_state:
                logging.debug("Setting relay state to %s for: %d", 'ON' if state == ON else 'OFF', e.device_id)
                set_relay(e.device_id, state)
                update_schedule(e.id, device_id=e.device_id, last_state=state)
    except BaseException:
        logging.error("scheduleJob error: ", exc_info=True)


schedule.every(1).minutes.do(updateSensorData)
schedule.every(1).seconds.do(scheduleJob)


@app.cli.command("run-scheduler")
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
