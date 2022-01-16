from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from controller import Person, Room, Booking
from controller.Person import create_new_person

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
            return create_new_person(args)
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


@app.route('/pika-booking/persons/<string:name>', methods=['GET'])
def handle_person_name(name):
    if request.method == 'GET':
        return Person.get_person(name)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/role/<int:r_id>', methods=['GET'])
def get_role_access(r_id):
    if request.method == 'GET':
        return Person.get_persons_by_role(r_id)
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
        if args:
            return Person.get_account_info(args)
        else:
            return jsonify("Args not found: email or password"), 405
    else:
        return jsonify("Method Not Allowed"), 405

# =================== #
# ===-| R O O M |-=== #
# =================== #


@app.route('/pika-booking/rooms', methods=['GET', 'POST', 'PUT'])
def handle_roms():
    args = request.json
    if request.method == 'GET':
        if request.args:
            return Room.get_all_rooms(int(request.args['limit']))
        return Room.get_all_rooms()
    elif request.method == 'POST':
        if args:
            return Room.create_new_room(args)
        return jsonify("Args not found"), 405
    elif request.method == 'PUT':
        if args:
            return Room.update_room(args)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/<int:r_id>', methods=['GET', 'DELETE'])
def handle_rooms_by_id(r_id):
    if request.method == 'GET':
        return Room.get_room(r_id)
    elif request.method == 'DELETE':
        return Room.delete_room(r_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/<string:r_name>', methods=['GET'])
def handle_rooms_by_name(r_name):
    if request.method == 'GET':
        return Room.get_room(r_name)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/most-booked', methods=['GET'])
def get_most_booked_room():
    # This gets the most booked room in general (top 10)
    if request.method == 'GET':
        return Room.get_most_booked_rooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available-room', methods=['POST'])
def get_available_rooms():
    # Get available room given a timeframe
    args = request.json
    print(args, "AET")
    if request.method == 'POST':
        if args and args['st_dt'] and args['et_dt']:
            return Room.get_available_rooms(args)
        return jsonify("Args not found"), 405
    else:
        jsonify("Method Not Allowed"), 405

# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #


@app.route('/pika-booking/bookings', methods=['GET', 'POST', 'PUT'])
def handle_bookings():
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking.create_new_booking(args)
        return jsonify("Args not found"), 405
    elif request.method == 'GET':
        if request.args:
            return Booking.get_all_bookings(int(request.args['limit']))
        return Booking.get_all_bookings()
    if request.method == 'PUT':
        if args:
            return Booking.update_room(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/<int:b_id>', methods=['GET', 'DELETE'])
def handle_booking_by(b_id):
    if request.method == 'GET':
        # Get Person by name or id
        return Booking.get_booking_by_id(b_id)
    elif request.method == 'DELETE':
        # Delete Person by id
        return Booking.delete_booking(b_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/shared-time', methods=['POST'])
def get_free_time_for_meeting_users():
    # This gets the most booked room in general
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking.get_shared_free_timeslot(request.json)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405

# ========================================== #
# ===-| U N A V A I L A B L E  R O O M |-=== #
# ========================================== #


if __name__ == "__main__":
    app.debug = True
    app.run()
