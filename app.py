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
@app.route('/pika-booking/rooms', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_rooms():
    args = request.args
    if request.method == 'POST':
        return Room().create_new_room(request.json)
    elif request.method == 'GET':
        if args:
            args_dict = {}
            if "room" in args:
                args_dict["r_id"] = args["room"]
            if "building" in args:
                args_dict["r_building"] = args["building"]
            if "department" in args:
                args_dict["r_dept"] = args["department"]
            if "lab" in args:
                args_dict["r_type"] = 1
            if "classroom" in args:
                args_dict["r_type"] = 2
            if "conference" in args:
                args_dict["r_type"] = 3
            if "office" in args:
                args_dict["r_type"] = 4
            if "study" in args:
                args_dict["r_type"] = 4
            if args_dict == {}:
                return jsonify("Parameter Doesn't match with query!"), 200
            return Room().get_rooms(args_dict)
        else:
            return Room().get_all_rooms()
    elif request.method == 'PUT':
        if args:
            args_dict = {}
            if "room" in args:
                return Room().update_room(args["room"], request.json)
            else:
                return jsonify("Parameter Doesn't match with query!"), 200
        else:
            return jsonify("Parameter Doesn't match with query!"), 200
    elif request.method == 'DELETE':
        if args:
            args_dict = {}
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
@app.route('/pika-booking/booking', methods=['GET', 'POST'])
def handle_bookings():
    if request.method == 'POST':
        return Booking().create_new_booking(request.json)
    elif request.method == 'GET':
        return Booking().get_all_booking()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/booking/<int:b_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_bookings_by_id(b_id):
    if request.method == 'GET':
        return Booking().get_booking_by_id(b_id)
    elif request.method == 'PUT':
        return Booking().update_booking(b_id, request.json)
    elif request.method == 'DELETE':
        return Booking().delete_booking(b_id)
    else:
        return jsonify("Method Not Allowed"), 405



# Other

@app.route('/pika-booking/rooms/most-booked', methods=['GET'])
def get_most_used_room():
    if request.method == 'GET':
        return Room().get_most_booked_rooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>/rooms', methods=['GET'])
def get_room_by_person_id(p_id):
    pass


@app.route('/pika-booking/rooms/unavailable_rooms/<int:r_id>', methods=['GET'])
def get_unavailable_time_rooms():
    if request.method == 'GET':
        return Room().get_available_room_in_timeslot()


@app.route('/pika-booking/rooms/verify-time-frame', methods=['GET'])
def get_verify_time_frame():
    pass


# ======================= #
# ===-| P E R S O N |-=== #
# ======================= #
@app.route('/pika-booking/persons/', methods=['GET', 'POST'])
@app.route('/pika-booking/persons', methods=['GET', 'POST'])
def handle_persons():
    if request.method == 'POST':
        return Person().create_new_person(request.json)
    elif request.method == 'GET':
        return Person().get_all_persons()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_persons_by_id(p_id):
    if request.method == 'GET':
        return Person().get_persons_by_id(p_id)
    elif request.method == 'PUT':
        return Person().update_person(p_id, request.json)
    elif request.method == 'DELETE':
        return Person().delete_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/role/<int:p_id>', methods=['GET'])
def handle_persons_role_by_id(p_id):
    if request.method == 'GET':
        return Person().get_person_role_by_id(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/schedule/', methods=['GET'])
def handle_persons_schedule_by_id():
    if request.method == 'GET':
        return Person().get_all_day_schedule_of_person(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/pika-booking/persons/mostbookedperson', methods=['GET'])
def handle_most_booked_persons():
    if request.method == 'GET':
        return Person().get_most_booked_persons()
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/pika-booking/persons/busiesthours', methods=['GET'])
def handle_busiest_hours_persons():
    if request.method == 'GET':
        return Person().get_busiest_hours()
    else:
        return jsonify("Method Not Allowed"), 405

# unavailable person
@app.route('/pika-booking/unavailablepersons', methods=['GET', 'POST'])
def handle_unavailable_persons():
    if request.method == 'POST':
        return AvailablePerson().create_unavailable_time_schedule(request.json)
    elif request.method == 'GET':
        return AvailablePerson().get_all_unavailable_persons()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/unavailablepersons/<int:pa_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_unavaliable_persons_by_id(pa_id):
    if request.method == 'GET':
        return AvailablePerson().get_unavailable_person_by_id(pa_id)
    elif request.method == 'PUT':
        return AvailablePerson().update_unavailable_schedule(pa_id, request.json)
    elif request.method == 'DELETE':
        return AvailablePerson().delete_unavailable_schedule(pa_id)
    else:
        return jsonify("Method Not Allowed"), 405


# ================================= #
# ===-| A V A I A B I L I T Y |-=== #
# ================================= #
@app.route('/pika-booking/persons/unavailable-time-users', methods=['GET'])
def handle_available_time_of_users():
    if request.method == 'GET':
        return Person().get_all_available_time_persons()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/unavailable-time-users/<int:p_id>', methods=['GET'])
def handle_available_time_of_users_by_id(p_id):
    if request.method == 'GET':
        return Person().get_all_available_time_persons(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/<int:p_id>/unavailable-time-slot/', methods=['POST'])
def handle_person_available(p_id):
    if request.method == 'POST':
        return Person().add_unavailable_time_schedule(p_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.debug = True
    app.run()
