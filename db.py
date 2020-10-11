import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, Numeric, Time
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(os.environ.get('GREEN_PI_DB_CONNECTION'))

Base = declarative_base()
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()


class ScheduleNotFoundException(BaseException):
    pass


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    air_temp = Column(Integer)
    humidity = Column(Numeric())
    moister = Column(Numeric())
    created_date = Column(DateTime(timezone=True), server_default=func.now())


class ScheduleData(Base):
    __tablename__ = 'schedule_data'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    start_schedule = Column(Time)
    end_schedule = Column(Time)
    last_state = Column(Integer)
    manual_schedule = Column(Integer)
    enable_schedule = Column(Integer)


def add_sensor_data(data):
    with session_scope() as session:
        session.add(SensorData(**data))


def add_schedule(start_schedule, end_schedule, enabled, device_id, manual_schedule=0):
    with session_scope() as session:
        session.add(ScheduleData(
            start_schedule=start_schedule,
            end_schedule=end_schedule,
            device_id=device_id,
            enable_schedule=enabled,
            manual_schedule=manual_schedule,
            last_state=None
        ))


def update_schedule(schedule_id, start_schedule=None, end_schedule=None, enabled=True, device_id=None, last_state=None):
    with session_scope() as session:
        schedule = session.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        schedule.start_schedule = start_schedule or schedule.start_schedule
        schedule.end_schedule = end_schedule or schedule.end_schedule
        schedule.enable_schedule = enabled if enabled is not None else schedule.enable_schedule
        schedule.device_id = device_id if device_id is not None else schedule.device_id
        schedule.last_state = last_state if last_state is not None else schedule.last_state
        session.commit()


def enable_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        schedule.enable_schedule = 1
        session.commit()


def disabe_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        schedule.enable_schedule = 0
        session.commit()


def delete_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        session.delete(schedule)
        session.commit()


def get_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        session.expunge_all()
        return schedule


def get_schedules(with_disabled=False):
    with session_scope() as session:
        schedules = session.query(ScheduleData)
        if not with_disabled:
            schedules = schedules.filter(ScheduleData.enable_schedule == 1)
        schedules = schedules.all()
        session.expunge_all()
        return schedules
