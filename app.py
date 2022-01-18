from flask import Flask, request, jsonify
import os

from flask_cors import CORS

from controller.AvailableRoom import AvailableRoom
from controller import Person
from controller.Room import Room
from controller.Booking import Booking
from controller import AvailablePerson

app = Flask(__name__, instance_relative_config=True)

CORS(app, origins=["*"])  # allow it from all places

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


# Home Page, greeting
@app.route('/')
@app.route('/index')
@app.route('/home')
def main():
    return "Hey! Welcome to Pika Booking, a cute lil booking App! ❤"


# ======================= #
# ===-| P E R S O N |-=== #
# ======================= #

@app.route('/pika-booking/persons', methods=['GET', 'POST', 'PUT'])
def handle_persons():
    args = request.json
    # Create new Person
    if request.method == 'POST':
        if args:
            return Person.create_new_person(args)
        return jsonify("Args not found"), 405
    elif request.method == 'GET':
        # Get all Persons
        if request.args:
            return Person.get_all_persons(int(request.args['limit']))
        return Person.get_all_persons()
    if request.method == 'PUT':
        # Update Person
        if args:
            return Person.update_person(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>', methods=['GET', 'DELETE'])
def handle_person_by(p_id):
    if request.method == 'GET':
        # Get Person by name or id
        return Person.get_person(p_id)
    elif request.method == 'DELETE':
        # Delete Person by id
        return Person.delete_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/persons/role/<int:role_id>', methods=['GET'])
def get_all_persons_by_role(role_id):
    if request.method == 'GET':
        return Person.get_persons_by_role(role_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>/shared', methods=['GET'])
def get_person_who_shares_booking_with(p_id):
    # This gets the most booked room in general
    if request.method == 'GET':
        return Person.get_person_that_most_share_with_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>/all-hosts', methods=['GET'])
def get_hosts_that_invited_person(p_id):
    if request.method == 'GET':
        return Person.get_hosts_that_invited_this_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>/most-used-room', methods=['GET'])
def get_most_used_room_by_person(p_id):
    if request.method == 'GET':
        return Person.get_most_used_room_by_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/top-bookers', methods=['GET'])
def get_top_10_bookers():
    if request.method == 'GET':
        return Person.get_person_who_booked_most()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/accounts', methods=['POST'])
def get_account_by_email_and_password():
    args = request.json
    if request.method == 'POST':
        if args and 'p_email' in args and 'p_password' in args:
            return Person.get_account_info(args)
        else:
            return jsonify("Args not found: email or password"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/persons/<int:p_id>/all-schedule', methods=['GET'])
def get_person_schedule(p_id):
    if request.method == 'GET':
        return AvailablePerson.get_schedule(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


# ============================================== #
# ===-| U N A V A I L A B L E  P E R S O N |-=== #
# ============================================== #

@app.route('/pika-booking/persons/unavailable', methods=['GET', 'POST', 'PUT'])
def handle_unavailable_person():
    args = request.json
    if request.method == 'GET':
        return AvailablePerson.get_all_unavailable_persons()
    elif request.method == 'POST':
        if args:
            return AvailablePerson.create_unavailable_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'PUT':
        if args:
            return AvailablePerson.update_unavailable_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/unavailable-schedule/<int:pa_id>', methods=['GET'])
def get_unavailable_person_schedule(pa_id):
    if request.method == 'GET':
        return AvailablePerson.get_unavailable_person_by_id(pa_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/persons/<int:p_id>/unavailable', methods=['GET'])
def get_unavailable_person_schedule_by_person(p_id):
    if request.method == 'GET':
        return AvailablePerson.get_unavailable_person_by_person_id(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/all-day-schedule', methods=['POST'])
def handle_all_day_schedule():
    args = request.json
    if request.method == 'POST':
        if args and 'date' in args and 'person_id' in args:
            return AvailablePerson.get_all_day_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.debug = True
    app.run()
