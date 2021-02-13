from flask import jsonify, request, Blueprint
from db import get_schedules, get_schedule, update_schedule, enable_schedule, \
    disabe_schedule, add_schedule, delete_schedule, SensorEnum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
import logging
from relay import update_relay, OFF


logger = logging.getLogger(__file__)


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


schedules_bp = Blueprint('schedules', 'schedules')


@schedules_bp.route('/schedules', methods=['GET'])
def schedules():
    schema = ScheduleSchema(many=True)
    schedules = get_schedules(True)
    return jsonify(schema.dump(schedules))


@schedules_bp.route('/schedules', methods=['POST'])
def schedules_add():
    try:
        data = request.get_json()
    except BaseException:
        logger.error("Error reading the request body")
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


@schedules_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
def schedule(schedule_id):
    schema = ScheduleSchema()
    schedule = get_schedule(schedule_id)
    return jsonify(schema.dump(schedule))


@schedules_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def schedule_update(schedule_id):
    try:
        data = request.get_json()
    except BaseException:
        logger.error("Error reading the request body")
        return jsonify({"message": "invalid request"})

    schedule = get_schedule(schedule_id)
    if schedule is not None and data.get('enable_schedule') is False and \
            schedule.enable_schedule is True:
        update_relay(schedule.id, schedule.device_id, OFF)
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


@schedules_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def schedule_delete(schedule_id):
    schedule = get_schedule(schedule_id)
    if schedule is not None:
        update_relay(schedule.id, schedule.device_id, OFF)
    delete_schedule(schedule_id)
    return jsonify({"message": "schedule was deleted successfully"})


@schedules_bp.route('/schedules/<int:schedule_id>/enable', methods=['PUT'])
def schedule_enable(schedule_id):
    enable_schedule(schedule_id)
    return jsonify({"message": "schedule was enabled successfully"})


@schedules_bp.route('/schedules/<int:schedule_id>/disable', methods=['PUT'])
def schedule_disable(schedule_id):
    schedule = get_schedule(schedule_id)
    if schedule is not None:
        update_relay(schedule.id, schedule.device_id, OFF)
    disabe_schedule(schedule_id)
    return jsonify({"message": "schedule was disabled successfully"})
