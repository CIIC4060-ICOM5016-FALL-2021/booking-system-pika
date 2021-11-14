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
    return render_template('index.html')


# ################################################

# =================== #
# ===-| R O O M |-=== #
# =================== #
@app.route('/pika-booking/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'POST':
        return Room().create_room(request.json)
    elif request.method == 'GET':
        return Room().get_all_rooms()
    else:
        return jsonify("Method Not Allowed"), 405


# ======================= #
# ===-| P E R S O N |-=== #
# ======================= #
@app.route('/pika-booking/users', methods=['GET', 'POST'])
def handle_users(username):
    if request.method == 'POST':
        return Person().create_new_person(request.json)
    else:
        return Person().get_all_persons()


# ========================= #
# ===-| B O O K I N G |-=== #
# ========================= #
@app.route('/pika-bookings/booking/<int:b_id>', methods=['GET'])
def handle_bookings_by_id(b_id):
    if request.method == 'GET':
        return Booking().get_booking_by_id(b_id)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == "__main__":
    app.run(debug=True)
