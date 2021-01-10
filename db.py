import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class SensorEnum(enum.Enum):
    SensorTemperature = 'temperature'
    SensorHumidity = 'humidity'


class Missing(object):
    pass


missing = Missing()

db = SQLAlchemy()


class ScheduleNotFoundException(BaseException):
    pass


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    air_temp = db.Column(db.Integer)
    humidity = db.Column(db.Numeric)
    moister = db.Column(db.Numeric)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())


class ScheduleData(db.Model):
    __tablename__ = 'schedule_data'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    start_schedule = db.Column(db.Time)
    end_schedule = db.Column(db.Time)
    last_state = db.Column(db.Integer)
    manual_schedule = db.Column(db.Integer)
    enable_schedule = db.Column(db.Integer)
    sensor = db.Column(db.Enum(SensorEnum), nullable=True)
    sensor_min = db.Column(db.Numeric, nullable=True)
    sensor_max = db.Column(db.Numeric, nullable=True)


def add_sensor_data(data):
    db.session.add(SensorData(**data))
    db.session.commit()


def add_schedule(start_schedule, end_schedule, enabled, device_id, sensor=None, sensor_min=None, 
                 sensor_max=None, manual_schedule=0):
    db.session.add(ScheduleData(
        start_schedule=start_schedule,
        end_schedule=end_schedule,
        device_id=device_id,
        enable_schedule=enabled,
        manual_schedule=manual_schedule,
        sensor=sensor,
        sensor_min=sensor_min,
        sensor_max=sensor_max,
        last_state=None
    ))
    db.session.commit()


def update_schedule(schedule_id, start_schedule=None, end_schedule=None, enabled=None, device_id=None, last_state=None, 
                    sensor=missing, sensor_min=missing, sensor_max=missing):
    schedule = ScheduleData.query.get(schedule_id)
    if schedule is None:
        raise ScheduleNotFoundException('Schedule not found')
    schedule.start_schedule = start_schedule or schedule.start_schedule
    schedule.end_schedule = end_schedule or schedule.end_schedule
    schedule.enable_schedule = enabled if enabled is not None else schedule.enable_schedule
    schedule.device_id = device_id if device_id is not None else schedule.device_id
    schedule.last_state = last_state if last_state is not None else schedule.last_state
    schedule.sensor = sensor if sensor is not missing else schedule.sensor
    schedule.sensor_min = sensor_min if sensor_min is not missing else schedule.sensor_min
    schedule.sensor_max = sensor_max if sensor_max is not missing else schedule.sensor_max
    db.session.commit()


def enable_schedule(schedule_id):
    schedule = ScheduleData.query.get(schedule_id)
    if schedule is None:
        raise ScheduleNotFoundException('Schedule not found')
    schedule.enable_schedule = 1
    db.session.commit()


def disabe_schedule(schedule_id):
    schedule = ScheduleData.query.get(schedule_id)
    if schedule is None:
        raise ScheduleNotFoundException('Schedule not found')
    schedule.enable_schedule = 0
    db.session.commit()


def delete_schedule(schedule_id):
    schedule = ScheduleData.query.get(schedule_id)
    if schedule is None:
        raise ScheduleNotFoundException('Schedule not found')
    db.session.delete(schedule)
    db.session.commit()


def get_schedule(schedule_id):
    schedule = ScheduleData.query.get(schedule_id)
    if schedule is None:
        raise ScheduleNotFoundException('Schedule not found')
    return schedule


def get_schedules(with_disabled=False):
    schedules = ScheduleData.query
    if not with_disabled:
        schedules = schedules.filter(ScheduleData.enable_schedule == 1)
    schedules = schedules.all()
    return schedules
