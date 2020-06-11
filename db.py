import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, Numeric, Sequence, Boolean, Time
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
    except:
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
    enable_schedule = Column(Boolean)

def add_sensor_data(data):
    with session_scope() as session:
        session.add(SensorData(**data))


def add_schedule(start_schedule, end_schedule, enabled, device_id):
    with session_scope() as session:
        session.add(ScheduleData(
            start_schedule=start_schedule,
            end_schedule=end_schedule,
            device_id=device_id,
            enable_schedule=enabled,
            last_state=None
        ))

def get_schedule(schedule_id, session=None):
    if session is not None:
        session = session_scope()
    with session:
        schedule = sesssion.query(ScheduleData).get(schedule_id)
        if schedule is None:
            raise ScheduleNotFoundException('Schedule not found')
        return schedule

def update_schedule(schedule_id, start_schedule=None end_schedule=None, enabled=True, device_id=None, last_state=None):
    with session_scope() as session:
        schedule = get_schedule(schedule_id)
        schedule.start_schedule = start_schedule or schedule.start_schedule
        schedule.end_schedule = end_schedule or schedule.end_schedule
        schedule.enable_schedule = enabled if enabled is not None else schedule.enable_schedule
        schedule.device_id = device_id if device_id is not None else schedule.device_id
        Schedule.last_state = last_state or Schedule.last_state
        session.commit()

def enable_schedule(schedule_id):
    with session_scope() as session:
        schedule = get_schedule(schedule_id, session)
        Schedule.enable_schedule = True
        session.commit()

def disabe_schedule(schedule_id):
    with session_scope() as session:
        schedule = get_schedule(schedule_id, session)
        Schedule.enable_schedule = True
        session.commit()
    
def get_schedules():
    with session_scope() as session:
        return session.query(ScheduleData).filter(ScheduleData.enable_schedule==True).all()
