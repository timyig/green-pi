from flask import Flask, jsonify, request
from db import get_schedules, update_schedule, enable_schedule, disabe_schedule, add_schedule, delete_schedule
from marshmallow import Schema, fields
import logging

class ScheduleSchema(Schema):
    id = fields.Int()
    start_schedule = fields.Time()
    end_schedule = fields.Time()
    enable_schedule = fields.Bool()
    manual_schedule = fields.Bool()
    device_id = fields.Int()

app = Flask(__name__)

@app.route('/schedules', methods=['GET'])
def schedules():
    schema = ScheduleSchema(many=True)
    schedules = get_schedules(True)
    return jsonify(schema.dump(schedules))

@app.route('/schedules', methods=['POST'])
def schedules_add():
    try:
        data = request.get_json()
    except:
        logging.error("Error reading the request body")
        return jsonify({"message": "invalid request"})
    add_schedule(
        start_schedule=data.get('start_schedule'),
        end_schedule=data.get('end_schedule'),
        enabled=1,
        device_id=data.get('device_id'),
        manual_schedule=1
        )
    return jsonify({"message": "schedule was added successfully"})

@app.route('/schedules/<int:schedule_id>', methods=['PUT'])
def schedule_update(schedule_id):
    try:
        data = request.get_json()
    except:
        logging.error("Error reading the request body")
        return jsonify({"message": "invalid request"})
        
    update_schedule(
        schedule_id,
        start_schedule=data.get('start_schedule'),
        end_schedule=data.get('end_schedule'),
        device_id=data.get('device_id')
        )

    return jsonify({"message": "schedule was updated successfully"})

@app.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def schedule_delete(schedule_id):
    delete_schedule(schedule_id)
    return jsonify({"message": "schedule was deleted successfully"})

@app.route('/schedules/<int:schedule_id>/enable', methods=['PUT'])
def schedule_enable(schedule_id):
    enable_schedule(schedule_id)
    return jsonify({"message": "schedule was enabled successfully"})

@app.route('/schedules/<int:schedule_id>/disable', methods=['PUT'])
def schedule_disable(schedule_id):
    disabe_schedule(schedule_id)
    return jsonify({"message": "schedule was disabled successfully"})
