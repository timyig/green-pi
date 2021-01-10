import pytest
from relay import ON, OFF
from green_pi import get_sensor_state


@pytest.mark.parametrize("sensor_value,last_state,sensor_min,sensor_max,inverted,output_state", [
    (15, OFF, 16, 18, False, ON),
    (20, OFF, 16, 18, False, OFF),
    (17, OFF, 16, 18, False, OFF),
    (16, OFF, 16, 18, False, ON),
    (18, OFF, 16, 18, False, OFF),
    (15, ON, 16, 18, False, ON),
    (20, ON, 16, 18, False, OFF),
    (17, ON, 16, 18, False, ON),
    (16, ON, 16, 18, False, ON),
    (18, ON, 16, 18, False, OFF),
    (15, OFF, 16, 18, True, OFF),
    (20, OFF, 16, 18, True, ON),
    (17, OFF, 16, 18, True, OFF),
    (16, OFF, 16, 18, True, OFF),
    (18, OFF, 16, 18, True, ON),
    (15, ON, 16, 18, True, OFF),
    (20, ON, 16, 18, True, ON),
    (17, ON, 16, 18, True, ON),
    (16, ON, 16, 18, True, OFF),
    (18, ON, 16, 18, True, ON),
])
def test_get_sensor_state(sensor_value, last_state, sensor_min, sensor_max, inverted, output_state):
    assert output_state == get_sensor_state(sensor_value, last_state, sensor_min, sensor_max, inverted=inverted)
