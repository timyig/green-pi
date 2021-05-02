#import subprocess
import logging
from gpiozero import LED
#from db import update_schedule

#logger = logging.getLogger(__file__)

OFF = 0
ON = 1

RELAY1 = LED(21)
RELAY2 = LED(20)
RELAY3 = LED(16)
RELAY4 = LED(12)


def init_relay():
    # Inverted logic On means Off
    RELAY1.on()
    RELAY2.on()
    RELAY3.on()
    RELAY4.on()


def set_relay(device_id, state):
    try:
        device = device_id
        if device == 1:
            relay = RELAY1
        elif device == 2:
            relay = RELAY2
        elif device == 3:
            relay = RELAY3
        elif device == 4:
            relay = RELAY4

        if state == OFF:
            relay.on()
        elif state == ON:
            relay.off()
    except BaseException:
        logger.error('Error setting relay:', exc_info=True)
    logger.debug("Setting relay %d to %d", device_id, state)


def update_relay(schedule_id, device_id, state):
    logger.debug("Setting relay state to %s for: %d", 'ON' if state == ON else 'OFF', device_id)
    set_relay(device_id, state)
    update_schedule(schedule_id, device_id=device_id, last_state=state)
