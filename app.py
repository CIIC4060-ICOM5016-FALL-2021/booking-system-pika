from flask import Flask, request, jsonify
import os

from flask_cors import CORS

from controller.Person import Person
from controller.Room import Room
from controller.Booking import Booking
from controller.AvailablePerson import AvailablePerson

app = Flask(__name__, instance_relative_config=True)

CORS(app, origins=["*"])  # allow it from todos los lugares

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

# @app.route('/pika-booking/rooms/available-room/timeframe', methods=['GET'])


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
        if args:
            if "p_id" in args:
                return Person().delete_person(args["p_id"])
            else:
                return jsonify("Args not found: p_id"), 405
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


@app.route('/pika-booking/persons/person/role-access', methods=['GET'])
def get_role_access():
    args = request.json
    if request.method == 'GET':
        if args and args["p_id"] is not None:
            return Person().role_to_get_access_to_room_info(args["p_id"])
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


# ============================================== #
# ===-| U N A V A I L A B L E  P E R S O N |-=== #
# ============================================== #

@app.route('/pika-booking/room/available', methods=['GET', 'POST', 'DELETE'])
def get_available_rooms_at_timeframe():
    if request.method == 'GET':
        # Find an available room (lab, classroom, study space, etc.) at a time frame
        return Room().get_available_rooms(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

# @app.route('/pika-booking/persons/person/all-day-schedule', methods=['GET'])
# def get_all_day_schedule_person():
#     args = request.json
#     if request.method == 'GET':
#         if args:
#             return Person().get_all_day_schedule_of_person(args)
#         else:
#             return jsonify("Missing Arguments")
#     else:
#         return jsonify("Method Not Allowed"), 405

# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
@app.route('/pika-booking/booking', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_bookings():
    args =request.json
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
        if args:
            if "b_id" in args:
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


# TODO FIX THIS
@app.route('/pika-booking/persons/all-day-schedule', methods=['GET'])
def get_all_day_schedule():
    if request.method == 'GET':
        return AvailablePerson().get_all_schedule(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# @app.route('/pika-booking/room/busiest-hours', methods=['GET'])
# def get_busiest_hours():
# This returns a query of the timeframes with most hours booked


if __name__ == "__main__":
    app.debug = True
    app.run()
