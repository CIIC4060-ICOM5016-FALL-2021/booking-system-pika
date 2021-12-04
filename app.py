from flask import Flask, request, jsonify
from flask.json import JSONDecoder
import os
from controller.Person import Person
from controller.Room import Room
from controller.Booking import Booking
from controller.AvailablePerson import AvailablePerson

app = Flask(__name__, instance_relative_config=True)

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
    args = request.args
    if request.method == 'POST':
        return Room().create_new_room(request.json)
    elif request.method == 'GET':
        if args:
            if "room" in args:
                return Room().get_room_by_id(request.json["room"])
            else:
                return jsonify("Parameter Doesn't match with query!"), 200
        else:
            return Room().get_all_rooms()
    elif request.method == 'PUT':
        return Room().update_room(request.json)
    elif request.method == 'DELETE':
        if args:
            if "room" in args:
                return Room().delete_room(args["room"])
            else:
                return jsonify("Parameter Doesn't match with query!"), 200
        else:
            return jsonify("Parameter Doesn't match with query!"), 200
    else:
        return jsonify("Method Not Allowed"), 405


# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
@app.route('/pika-booking/booking', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_bookings():
    if request.method == 'POST':
        return Booking().create_new_booking(request.json)
    elif request.method == 'GET':
        args = request.args
        if args:
            if "b" in args.keys():
                return Booking().get_booking_by_id(args["b"])
            else:
                return jsonify("Sorry, but this query parameter does not exists"), 200
        else:
            return Booking().get_all_booking()

    elif request.method == 'PUT':
        args = request.args
        if args:
            if "b" in args.keys():
                return Booking().update_booking(args["b"], request.json)
            else:
                return jsonify("Sorry, but this query parameter does not exists"), 200
        else:
            return jsonify("Sorry, but this request requires more information"), 200

    elif request.method == 'DELETE':
        args = request.args
        if args:
            if "b" in args.keys():
                return Booking().delete_booking(args["b"])
            else:
                return jsonify("Sorry, but this query parameter does not exists"), 200
        else:
            return jsonify("Sorry, but this request requires more information"), 200
    else:
        return jsonify("Method Not Allowed"), 405


# ========================= #
# ===-| P E R S O N S |-=== #
# ========================= #
@app.route('/pika-booking/persons', methods=['GET', 'POST'])
def handle_persons():
    if request.method == 'POST':
        return Person().create_new_person(request.json)
    elif request.method == 'GET':
        return Person().get_all_persons()
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


@app.route('/pika-booking/room/available', methods=['GET'])
def get_available_rooms_at_timeframe():
    if request.method == 'GET':
        # Find an available room (lab, classroom, study space, etc.) at a time frame
        return Room().get_available_rooms(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# ============================================== #
# ===-| U N A V A I L A B L E  P E R S O N |-=== #
# ============================================== #
@app.route('/pika-booking/rooms/most-booked', methods=['GET'])
def handle_unavailable_person():
    if request.method == 'GET':
        return Room().get_most_booked_rooms()
    else:
        return jsonify("Method Not Allowed"), 405

# TODO FIX THIS
@app.route('/pika-booking/person/all-day-schedule', methods=['GET'])
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
