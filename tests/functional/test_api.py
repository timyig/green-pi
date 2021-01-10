from datetime import time
from http import HTTPStatus
from db import ScheduleData, SensorEnum


def test_add_schedule(client, db):
    before_count = ScheduleData.query.count()
    rv = client.post('/schedules', json={
        'start_schedule': '08:00:00',
        'end_schedule': '18:00:00',
        'enable_schedule': True,
        'device_id': 1,
        'sensor': 'temperature',
        'sensor_min': 16.5,
        'sensor_max': 18
    })
    assert HTTPStatus.OK.value == rv.status_code
    assert 'schedule was added successfully' == rv.json.get('message')
    after_count = ScheduleData.query.count()
    assert after_count == before_count + 1


def test_schedules(client, db):
    rv = client.get('/schedules')
    assert HTTPStatus.OK.value == rv.status_code
    schedule = next(iter(rv.json or []), None)
    assert schedule.get('start_schedule') is not None
    assert schedule.get('end_schedule') is not None
    assert schedule.get('device_id') is not None


def test_get_schedule(client, db):
    db_schedule = ScheduleData.query.first()
    rv = client.get('/schedules/{id}'.format(id=db_schedule.id))
    assert HTTPStatus.OK.value == rv.status_code
    schedule = rv.json or {}
    assert schedule.get('id') == db_schedule.id
    assert schedule.get('start_schedule') is not None
    assert schedule.get('end_schedule') is not None
    assert schedule.get('device_id') is not None


def test_delete_schedule(client, db):
    db_schedule = ScheduleData.query.first()
    rv = client.delete('/schedules/{id}'.format(id=db_schedule.id))
    assert HTTPStatus.OK.value == rv.status_code


def test_update_schedule(client, db):
    db_schedule = ScheduleData.query.first()
    rv = client.put('/schedules/{id}'.format(id=db_schedule.id), json={
        'start_schedule': '01:01:01',
        'end_schedule': '18:18:18',
        'enable_schedule': False,
        'device_id': 2,
        'sensor': 'humidity',
        'sensor_min': 17.5,
        'sensor_max': 18.5
    })
    assert HTTPStatus.OK.value == rv.status_code
    db_schedule = ScheduleData.query.first()
    assert db_schedule.start_schedule == time(1, 1, 1)
    assert db_schedule.end_schedule == time(18, 18, 18)
    assert db_schedule.enable_schedule == 0
    assert db_schedule.device_id == 2
    assert db_schedule.sensor == SensorEnum.SensorHumidity
    assert db_schedule.sensor_min == 17.5
    assert db_schedule.sensor_max == 18.5


def test_enable_schedule(client, db):
    db_schedule = ScheduleData.query.first()
    rv = client.put('/schedules/{id}/enable'.format(id=db_schedule.id))
    assert HTTPStatus.OK.value == rv.status_code


def test_disable_schedule(client, db):
    db_schedule = ScheduleData.query.first()
    rv = client.put('/schedules/{id}/disable'.format(id=db_schedule.id))
    assert HTTPStatus.OK.value == rv.status_code
