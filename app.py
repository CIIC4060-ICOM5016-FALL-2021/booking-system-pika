from flask import Flask, request, jsonify
import os

from flask_cors import CORS

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


# ################################################

# =================== #
# ===-| R O O M |-=== #
# =================== #

# Room Basic CRUD
# This crud maanges all 5 main basic requests for room
# Create a new room (json)
# Delete an existing room given a room id
# Update an existing room also by a given id
# Get either all rooms or by a specified query parameter
# /pika-booking/rooms?department='ININ'
@app.route('/pika-booking/rooms', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_rooms():
    args = request.json
    if request.method == 'POST':
        return Room().create_new_room(args)
    elif request.method == 'GET':
        if args:
            if "r_id" in args:
                return Room().get_room_by_id(args["r_id"])
            else:
                return jsonify("Parameter Doesn't match with query!"), 200
        else:
            return Room().get_all_rooms()
    elif request.method == 'PUT':
        return Room().update_room(args)
    elif request.method == 'DELETE':
        if args:
            if "r_id" in args:
                return Room().delete_room(args["r_id"])
            else:
                return jsonify("Args not found: r_id"), 405
        else:
            return jsonify("Args not found: r_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# Finds all available rooms at a given timeframe
@app.route('/pika-booking/rooms/available-room', methods=['GET'])
def find_available_rooms():
    args = request.json
    if request.method == 'GET':
        return Room().get_available_rooms(args)
    else:
        return jsonify("Method Not Allowed"), 405


# ========================================== #
# ===-| U N A V A I L A B L E  R O O M |-=== #
# ========================================== #
@app.route('/pika-booking/rooms/available', methods=['GET', 'POST', 'DELETE', 'PUT'])
def get_available_rooms_at_timeframe():
    return


# ========================= #
# ===-| P E R S O N S |-=== #
# ========================= #

@app.route('/pika-booking/persons', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_persons():
    args = request.json
    if request.method == 'POST':
        return Person().create_new_person(args)

    elif request.method == 'GET':
        if args:
            if "p_id" in args:
                return Person().get_persons_by_id(args["p_id"])
            else:
                return jsonify("Parameter Doesn't match with query!"), 200
        else:
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


# Retrieves top 10 most booked persons
@app.route('/pika-booking/persons/most-booked', methods=['GET'])
def get_most_booked_persons():
    if request.method == 'GET':
        return Person().get_most_booked_persons()
    else:
        return jsonify("Method Not Allowed"), 405


# # Retrieves most booked room by a person
@app.route('/pika-booking/persons/person/most-booked-room', methods=['GET'])
def get_person_most_used_room():
    args = request.json
    if request.method == 'GET':
        if args and args["p_id"] is not None:
            return Person().get_most_used_room(args["p_id"])
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person/role-access/<int:p_id>', methods=['GET'])
def get_role_access(p_id):
    if request.method == 'GET':
        return Person().role_to_get_access_to_room_info(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


# ============================================== #
# ===-| U N A V A I L A B L E  P E R S O N |-=== #
# ============================================== #

@app.route('/pika-booking/persons/available', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_unavailable_person():
    args = request.json
    if request.method == 'GET':
        if args:
            return
        else:
            return AvailablePerson().get_all_unavailable_persons()
    elif request.method == 'POST':
        if args:
            return AvailablePerson().create_unavailable_time_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'DELETE':
        if args:
            if "pa_id" in args:
                return AvailablePerson().delete_unavailable_schedule(args["pa_id"])
            else:
                return jsonify("Missing Arguments"), 405
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


@app.route('/pika-booking/persons/available/timeframe', methods=['DELETE', 'GET'])
def handle_unavailable_person_at_timeframe():
    args = request.json
    if request.method == 'DELETE':
        if args and "p_id" in args and "st_dt" in args and "et_dt" in args:
            return AvailablePerson().delete_unavailable_person_schedule_at_certain_time(args)
        else:
            return jsonify("Missing Arguments"), 405
    elif request.method == 'GET':
        if args and "p_id" in args and "date" in args:
            return AvailablePerson().get_all_day_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
@app.route('/pika-booking/booking', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_bookings():
    args = request.json
    if request.method == 'POST':
        return Booking().create_new_booking(request.json)
    elif request.method == 'GET':
        if args:
            if "b_id" in args:
                return Booking().get_booking_by_id(args["b_id"])
            else:
                return jsonify("Sorry, but this query parameter does not exists"), 200
        else:
            return Booking().get_all_booking()

    elif request.method == 'PUT':
        if args:
            return Booking().update_booking(args)
        else:
            return jsonify("Missing Arguments"), 405

    elif request.method == 'DELETE':
        print(args)
        if args:
            if "b_id" in args.keys():
                return Booking().delete_booking(args["b_id"])
            else:
                return jsonify("Args not found: b_id"), 405
        else:
            return jsonify("Args not found: b_id"), 405
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
@app.route('/pika-booking/persons/shared-user', methods=['GET'])
def get_shared_person_for_id():
    # This gets the most booked room in general
    if request.method == 'GET':
        return Person().get_person_that_most_share_with_person(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/shared-time', methods=['GET'])
def get_free_time_for_meeting_users():
    # This gets the most booked room in general
    if request.method == 'GET':
        return Booking().get_shared_free_timeslot(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

if __name__ == "__main__":
    app.debug = True
    app.run()
