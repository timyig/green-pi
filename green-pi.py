#!/usr/bin/env python3
"""
Module Docstring
"""

import schedule
import time
import logging
import click

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

schedule.every(1).minutes.do(job)

while True:
    print("ah faaa")
    schedule.run_pending()
    time.sleep(1)