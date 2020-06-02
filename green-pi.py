#!/usr/bin/env python3
"""
Module Docstring
"""

import serial
import time
import logging
import click

__author__ = "Timur Yigit"
__version__ = "0.1.0"
__license__ = "MIT"

""" Data Frame """
""" BYTE 0  - BYTE 1        - BYTE 2 - BYTE 3 """
""" Command - Board address - Data   - Check sum XOR BYTE 1 BYTE 2 BYTE 3 """
print("Hellooooooo")