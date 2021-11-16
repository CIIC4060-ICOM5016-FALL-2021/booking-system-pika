from flask import Flask, render_template, request, jsonify
import os
from controller.Person import Person
from controller.Room import Room
from controller.Booking import Booking

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
@app.route('/pika-booking/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'POST':
        return Room().create_new_room(request.json)
    elif request.method == 'GET':
        return Room().get_all_rooms()


@app.route('/pika-booking/rooms/all', methods=['GET'])
def get_all_rooms():
    if request.method == 'GET':
        return Room().get_all_rooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/<int:r_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_rooms_by_id(r_id):
    if request.method == 'GET':
        return Room().get_room_by_id(r_id)
    elif request.method == 'PUT':
        return Room().update_room(r_id, request.json)
    elif request.method == 'DELETE':
        return Room().delete_room(r_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/rooms/most_used', methods=['GET'])
def get_most_used_room():
    if request.method == 'GET':
        return Room().get_most_used_room()
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
        return Person().get_person_by_id(p_id)
    elif request.method == 'PUT':
        return Person().update_person(p_id, request.json)
    elif request.method == 'DELETE':
        return Person().delete_person(p_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/pika-booking/persons/role/<int:p_id>', methods=['GET'])
def handle_persons_role_by_id(p_id):
    if request.method == 'GET':
        return Person.get_person_role_by_id(p_id)
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


# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
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


if __name__ == "__main__":
    app.debug = True
    app.run()
