from flask import Flask, request, jsonify
import os

from flask_cors import CORS

from controller.AvailableRoom import AvailableRoom
from controller.Person import Person
from controller.Room import Room
from controller.Booking import Booking
from controller.AvailablePerson import AvailablePerson

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


# =================== #
# ===-| R O O M |-=== #
# =================== #

# Room Basic CRUD
# This crud maanges all 5 main basic requests for room
# Create a new room (json)
# Delete an existing room given a room id
# Update an existing room also by a given id
@app.route('/pika-booking/rooms', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_rooms():
    args = request.json
    if request.method == 'POST':
        return Room().create_new_room(args)
    elif request.method == 'GET':
        return Room().get_all_rooms()
    elif request.method == 'PUT':
        if args:
            return Room().update_room(args)
        else:
            return jsonify("Args not found"), 405
    elif request.method == 'DELETE':
        if args and "r_id" in args:
            return Room().delete_room(args["r_id"])
        else:
            return jsonify("Args not found: r_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/id', methods=['POST'])
def handle_room_getter_post():
    args = request.json
    if request.method == 'POST':
        if args and "r_id" in args:
            return Room().get_room_by_id(args["r_id"])
        else:
            return jsonify("Args not found: r_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# Finds all available rooms at a given timeframe
@app.route('/pika-booking/rooms/available-room', methods=['POST'])
def find_available_rooms():
    args = request.json
    if request.method == 'POST':
        if args:
            return Room().get_available_rooms(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ========================================== #
# ===-| U N A V A I L A B L E  R O O M |-=== #
# ========================================== #
@app.route('/pika-booking/rooms/available', methods=['GET', 'POST', 'DELETE', 'PUT'])
def get_available_rooms_at_timeframe():
    args = request.json
    if request.method == 'GET':
        return AvailableRoom().get_all_unavailable_rooms()
    elif request.method == 'POST':
        if args:
            return AvailableRoom().create_unavailable_room_dt(args)
        else:
            return jsonify("Args not found"), 405
    elif request.method == 'DELETE':
        if args:
            return AvailableRoom().delete_unavailable_room(args)
        else:
            return jsonify("Args not found"), 405
    elif request.method == 'PUT':
        if args:
            return AvailableRoom().update_room_availability(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available/all-day-schedule', methods=['POST'])
def handle_get_all_schedule_getter_post():
    args = request.json
    if request.method == 'POST':
        if args:
            return AvailableRoom().get_all_schedule(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available/schedule', methods=['POST'])
def handle_verify_available_room_getter_post():
    args = request.json
    if request.method == 'POST':
        if args:
            return AvailableRoom().verify_available_room_at_timeframe(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/person/unavailable/id', methods=['POST'])
def handle_room__unavailable_getter_post():
    args = request.json
    if request.method == 'POST':
        if args and "r_id" in args:
            return Room().get_room_by_id(args["r_id"])
        else:
            return jsonify("Args not found: r_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ========================== #
# ===-| A C C O U N T |-=== #
# ========================= #

# NOTE: this is not part of the schema. this is just as a replacement of auth to handle accounts
@app.route('/booking/account', methods=['POST'])
def handle_account():
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().get_account_by_email_and_password(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405

# ========================= #
# ===-| P E R S O N S |-=== #
# ========================= #

@app.route('/pika-booking/persons', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_persons():
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().create_new_person(args)
        return jsonify("Args not found"), 405
    elif request.method == 'GET':
        return Person().get_all_persons()
    if request.method == 'PUT':
        if args:
            return Person().update_person(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'DELETE':
        if args and "p_id" in args:
            return Person().delete_person(args["p_id"])
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/id', methods=['POST'])
def handle_person_getter_post():
    args = request.json
    if request.method == 'POST':
        if args and "p_id" in args:
            return Person().get_persons_by_id(args["p_id"])
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# Retrieves top 10 most booked persons
@app.route('/pika-booking/persons/most-booked', methods=['GET'])
def get_most_booked_persons():
    if request.method == 'GET':
        return Person().get_most_booked_persons()
    else:
        return jsonify("Method Not Allowed"), 405


# Retrieves most booked room by a person
@app.route('/pika-booking/persons/person/most-booked-room', methods=['POST'])
def get_person_most_used_room():
    args = request.json
    if request.method == 'POST':
        if args and "p_id" in args:
            return Person().get_most_used_room(args["p_id"])
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person/role-access', methods=['POST'])
def get_role_access(p_id):
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().role_to_get_access_to_room_info(args)
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ============================================== #
# ===-| U N A V A I L A B L E  P E R S O N |-=== #
# ============================================== #

@app.route('/pika-booking/persons/available', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_unavailable_person():
    args = request.json
    if request.method == 'GET':
        return AvailablePerson().get_all_unavailable_persons()
    elif request.method == 'POST':
        if args:
            return AvailablePerson().create_unavailable_time_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'DELETE':
        if args and "pa_id" in args:
            return AvailablePerson().delete_unavailable_schedule(args["pa_id"])
        else:
            return jsonify("Args not found  "), 405
    elif request.method == 'PUT':
        if args:
            return AvailablePerson().update_unavailable_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/available/person', methods=['DELETE'])
def handle_unavailable_person_by_p_id():
    args = request.json
    if request.method == 'DELETE':
        if args and "p_id" in args:
            return AvailablePerson().delete_all_unavailable_person_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/available/timeframe', methods=['DELETE', 'POST'])
def handle_unavailable_person_at_timeframe():
    args = request.json
    if request.method == 'DELETE':
        if args and "p_id" in args and "st_dt" in args and "et_dt" in args:
            return AvailablePerson().delete_unavailable_person_schedule_at_certain_time(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'POST':
        if args and "p_id" in args and "date" in args:
            return AvailablePerson().get_all_day_schedule(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
@app.route('/pika-booking/booking', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_bookings():
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking().create_new_booking(request.json)
        else:
            return jsonify("Args not found"), 405
    elif request.method == 'GET':
        return Booking().get_all_booking()
    elif request.method == 'PUT':
        if args:
            return Booking().update_booking(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'DELETE':
        if args and "b_id" in args:
            return Booking().delete_booking(args["b_id"])
        else:
            return jsonify("Args not found: b_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/id', methods=['POST'])
def handle_person_id_getter_post():
    args = request.json
    if request.method == 'POST':
        if args and "b_id" in args:
            return Booking().get_booking_by_id(args["b_id"])
        else:
            return jsonify("Args not found: b_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/busiesthour', methods=['GET'])
def get_busiest_hours():
    if request.method == 'GET':
        return Booking().get_busiest_hours()
    else:
        return jsonify("Method Not Allowed"), 405


# =============================== #
# ===-| S T A T I S T I C S |-=== #
# =============================== #
@app.route('/pika-booking/rooms/most-booked', methods=['GET'])
def get_most_booked_room():
    # This gets the most booked room in general
    if request.method == 'GET':
        return Room().get_most_booked_rooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/shared', methods=['GET'])
def get_shared_person_for_id():
    # This gets the most booked room in general
    if request.method == 'GET':
        return Person().get_person_that_most_share_with_person(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/shared-time', methods=['POST'])
def get_free_time_for_meeting_users():
    # This gets the most booked room in general
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking().get_shared_free_timeslot(request.json)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.debug = True
    app.run()
