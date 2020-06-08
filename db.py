import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, Numeric, Sequence
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

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    air_temp = Column(Numeric())
    humidity = Column(Numeric())
    moister = Column(Numeric())
    created_date = Column(DateTime(timezone=True), server_default=func.now())

def add_sensor_data(data):
    with session_scope() as session:
        session.add(SensorData(**data))
