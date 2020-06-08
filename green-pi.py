#!/usr/bin/env python3
"""
Module Docstring
"""

import schedule
import time
import logging
import click

__author__ = "Timur Yigit"
__version__ = "0.1.0"
__license__ = "MIT"

def job():
    print("I'm working...")

schedule.every(1).minutes.do(job)

while True:
    print("ah faaa")
    schedule.run_pending()
    time.sleep(1)