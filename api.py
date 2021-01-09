import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from db import db, get_schedules, get_schedule, update_schedule, enable_schedule, \
    disabe_schedule, add_schedule, delete_schedule, SensorEnum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
import logging
from relay import set_relay, OFF


class ScheduleSchema(Schema):
    id = fields.Int()
    start_schedule = fields.Time()
    end_schedule = fields.Time()
    enable_schedule = fields.Bool()
    manual_schedule = fields.Bool()
    last_state = fields.Int()
    device_id = fields.Int()
    sensor = EnumField(SensorEnum, required=False, dump_by=EnumField.VALUE)
    sensor_min = fields.Float(required=False)
    sensor_max = fields.Float(required=False)


app = Flask(__name__)
app.config['CORS_AUTOMATIC_OPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('GREEN_PI_DB_CONNECTION')
cors = CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/schedules', methods=['GET'])
def schedules():
    schema = ScheduleSchema(many=True)
    schedules = get_schedules(True)
    return jsonify(schema.dump(schedules))


@app.route('/schedules', methods=['POST'])
def schedules_add():
    try:
        data = request.get_json()
    except BaseException:
        logging.error("Error reading the request body")
        return jsonify({"message": "invalid request"})
    add_schedule(
        start_schedule=data.get('start_schedule'),
        end_schedule=data.get('end_schedule'),
        enabled=int(data.get('enable_schedule')),
        device_id=data.get('device_id'),
        sensor=SensorEnum(data.get('sensor')) if data.get('sensor') else None,
        sensor_min=data.get('sensor_min'),
        sensor_max=data.get('sensor_max'),
        manual_schedule=1
    )
    return jsonify({"message": "schedule was added successfully"})


@app.route('/schedules/<int:schedule_id>', methods=['GET'])
def schedule(schedule_id):
    schema = ScheduleSchema()
    schedule = get_schedule(schedule_id)
    return jsonify(schema.dump(schedule))


@app.route('/schedules/<int:schedule_id>', methods=['PUT'])
def schedule_update(schedule_id):
    try:
        data = request.get_json()
    except BaseException:
        logging.error("Error reading the request body")
        return jsonify({"message": "invalid request"})

    schedule = get_schedule(schedule_id)
    if schedule is not None and data.get('enable_schedule') is False and \
            schedule.enable_schedule is True:
        set_relay(schedule.device_id, OFF)
    update_schedule(
        schedule_id,
        start_schedule=data.get('start_schedule'),
        end_schedule=data.get('end_schedule'),
        enabled=int(data.get('enable_schedule')),
        device_id=data.get('device_id'),
        sensor=SensorEnum(data.get('sensor')) if data.get('sensor') else None,
        sensor_min=data.get('sensor_min'),
        sensor_max=data.get('sensor_max'),
    )

    return jsonify({"message": "schedule was updated successfully"})


@app.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def schedule_delete(schedule_id):
    schedule = get_schedule(schedule_id)
    if schedule is not None:
        set_relay(schedule.device_id, OFF)
    delete_schedule(schedule_id)
    return jsonify({"message": "schedule was deleted successfully"})


@app.route('/schedules/<int:schedule_id>/enable', methods=['PUT'])
def schedule_enable(schedule_id):
    enable_schedule(schedule_id)
    return jsonify({"message": "schedule was enabled successfully"})


@app.route('/schedules/<int:schedule_id>/disable', methods=['PUT'])
def schedule_disable(schedule_id):
    schedule = get_schedule(schedule_id)
    if schedule is not None:
        set_relay(schedule.device_id, OFF)
    disabe_schedule(schedule_id)
    return jsonify({"message": "schedule was disabled successfully"})
