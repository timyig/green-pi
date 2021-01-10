import os
import logging

from db import update_schedule

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


OFF = 0
ON = 1


def set_relay(device_id, state):
    os.system('python pyt-8-Way-Relay-Board/k8_box.py set-relay -r {relay} -s {state}'.format(
        relay=device_id, state=state))
    logging.debug("Setting relay %d to %d", device_id, state)


def update_relay(schedule_id, device_id, state):
    logging.debug("Setting relay state to %s for: %d", 'ON' if state == ON else 'OFF', device_id)
    set_relay(device_id, state)
    update_schedule(schedule_id, device_id=device_id, last_state=state)
