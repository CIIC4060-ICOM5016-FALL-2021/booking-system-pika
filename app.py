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
@app.route('/pika-booking/rooms', methods=['GET', 'POST', 'PUT'])
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
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/<int:r_id>', methods=['GET', 'DELETE'])
def handle_rooms_by_id(r_id):
    if request.method == 'GET':
        return Room().get_room(r_id)
    elif request.method == 'DELETE':
        return Room().delete_room(r_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/<string:r_name>', methods=['GET'])
def handle_rooms_by_name(r_name):
    if request.method == 'GET':
        return Room().get_room(r_name)
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


# Gets all unavailable rooms by the room id, not the ra_id
@app.route('/pika-booking/rooms/unavailable/<int:room_id>', methods=['GET', 'DELETE'])
def handle_unavailable_room_by_room_id(room_id):
    if request.method == 'GET':
        return AvailableRoom().get_unavailable_room_by_room_id(room_id)
    elif request.method == 'DELETE':
        return AvailableRoom().delete_unavailable_room_by_room_id(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/unavailable/ra-id/<int:ra_id>', methods=['GET', 'DELETE'])
def handle_unavailable_room_by_ra_id(ra_id):
    if request.method == 'GET':
        return AvailableRoom().get_unavailable_by_ra_id(ra_id)
    elif request.method == 'DELETE':
        return AvailableRoom().delete_unavailable_room_by_ra_id(ra_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available/all-day-schedule', methods=['POST'])
def handle_get_room_all_day_schedule_getter_post():
    args = request.json
    if request.method == 'POST':
        if args:
            return AvailableRoom().get_all_day_schedule(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available/all-day-schedule/person-role', methods=['POST'])
def handle_get_room_all_day_schedule_by_person_role():
    args = request.json
    if request.method == 'POST':
        if args:
            return AvailableRoom().get_all_day_schedule_by_role(args)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/available/all-schedule/<int:r_id>', methods=['GET'])
def handle_get_room_all_schedule_getter_post(r_id):
    if request.method == 'GET':
        return AvailableRoom().get_schedule(r_id)
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

@app.route('/pika-booking/persons', methods=['GET', 'POST', 'PUT'])
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
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/but-not', methods=['POST'])
def get_all_persons_but():
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().get_all_persons(args)
        else:
            return jsonify("Args not found: p_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person-by-role/<int:role_id>', methods=['GET'])
def get_all_persons_by_role(role_id):
    if request.method == 'GET':
        return Person().get_all_persons_by_role(role_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>', methods=['GET', 'DELETE'])
def handle_person_getter_post(p_id):
    if request.method == 'GET':
        return Person().get_persons_by_id(p_id)
    elif request.method == 'DELETE':
        return Person().delete_person(p_id)
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
@app.route('/pika-booking/persons/<int:p_id>/most-booked-room', methods=['GET'])
def get_person_most_used_room(p_id):
    if request.method == 'GET':
        return Person().get_most_used_room(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person/<int:p_id>/role-access', methods=['GET'])
def get_role_access(p_id):
    if request.method == 'GET':
        return Person().person_to_get_access_to_room_info(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person/room-roles/<int:r_id>', methods=['GET'])
def get_rooms_by_role(r_id):
    if request.method == 'GET':
        return Person().role_to_get_access_to_room_info(r_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/accounts', methods=['POST'])
def get_account_by_email_and_password():
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().get_account_by_email_and_password(args)
        else:
            return jsonify("Args not found: email or password"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/person/all-schedule/<int:p_id>', methods=['GET'])
def handle_get_all_person_schedule_getter_post(p_id):
    if request.method == 'GET':
        return AvailablePerson().get_schedule(p_id)

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
            return jsonify("Args not found"), 405
    elif request.method == 'PUT':
        if args:
            return AvailablePerson().update_unavailable_schedule(args)
        else:
            return jsonify("Missing Arguments"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/person/unavailable/pa_id/<int:pa_id>', methods=['GET', 'DELETE'])
def handle_unavailable_person_pa_id(pa_id):
    if request.method == 'GET':
        return AvailablePerson().get_unavailable_person_by_id(pa_id)
    elif request.method == 'DELETE':
        return AvailablePerson().delete_unavailable_schedule(pa_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/person/unavailable/person_id/<int:p_id>', methods=['GET'])
def handle_unavailable_person_by_person_id(p_id):
    if request.method == 'GET':
        return AvailablePerson().get_unavailable_person_by_person_id(p_id)
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
            return Booking().delete_booking(args['b_id'])
        else:
            return jsonify("Args not found: b_id"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/<int:b_id>', methods=['GET', 'DELETE'])
def handle_booking_by_id(b_id):
    if request.method == 'GET':
        return Booking().get_booking_by_id(b_id)
    elif request.method == 'DELETE':
        return Booking().delete_booking(b_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/meet/<b_id>', methods=['GET'])
def get_full_booking_by_b_id(b_id):
    if request.method == 'GET':
        return Booking().get_meetings_by_id(b_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/meet/host/<int:host_id>', methods=['GET'])
def get_meeting_by_host_id(host_id):
    if request.method == 'GET':
        return Booking().get_meetings_by_host_id(host_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/host/<int:host_id>', methods=['GET'])
def get_bookings_by_host(host_id):
    if request.method == 'GET':
        return Booking().get_bookings_by_host(host_id)
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


@app.route('/pika-booking/persons/<int:p_id>/shared', methods=['GET'])
def get_shared_person_for_id(p_id):
    # This gets the most booked room in general
    if request.method == 'GET':
        return Person().get_person_that_most_share_with_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/shared-time-booking', methods=['POST']) # json args: int -> b_id (booking id) and date -> date (not timestamp)
def get_free_time_for_meeting_booking():
    # This gets the most booked room in general
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking().get_shared_free_timeslot(request.json)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/meetings', methods=['GET'])
def handle_meeting():
    if request.method == 'GET':
        return Booking().get_all_meetings()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/bookings/shared-time-users', methods=['POST']) # json args: list -> invited_id (list of p_id) and date -> date (not timestamp)
def get_free_time_for_meeting_users():
    # This gets the most booked room in general
    args = request.json
    if request.method == 'POST':
        if args:
            return Booking().get_shared_free_timeslot_users(request.json)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/email', methods=['POST'])
def get_persons_id_by_email():
    args = request.json
    if request.method == 'POST':
        if args:
            return Person().get_person_ids_by_email(request.json)
        else:
            return jsonify("Args not found"), 405
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.debug = True
    app.run()
