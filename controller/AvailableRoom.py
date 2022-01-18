from flask import jsonify

from models.AvailableRoom import AvailableRoomDAO
from models.Person import PersonDAO
from models.Room import RoomDAO


#############################
# CREATE UNAVAILABLE ROOM
# TIMEFRAME
#############################
def create_unavailable_room_dt(json: dict):
    room_id = json['room_id']
    start_time = json['start_time']
    end_time = json['end_time']
    unavailability_person = json['person_id']

    # Checks if the room exists
    method1 = RoomDAO()
    method2 = PersonDAO()

    if not method2.check_if_person_exists(unavailability_person):
        return jsonify("Person doesn't exist"), 404

    if not method1.check_if_room_exists(room_id):
        return jsonify("Room does not exist"), 404

    person = method2.get_person_by_id(unavailability_person)[2]
    room = method1.get_room_by_id(room_id)

    if not (method2.access[person] == room[3]):
        return jsonify("This person is not a staff. "
                       "Only staff members can modify the availability of rooms"), 404

    # add entry and return back
    method3 = AvailableRoomDAO()
    ra_id = method3.create_unavailable_room_time(room_id, start_time, end_time)
    return jsonify({'ra_id': ra_id}), 200


#############################
# UPDATE UNAVAILABLE ROOM
# BY UNAVAILABLE ID
#############################
def update_unavailability_room(json: dict):
    ra_id = json["ra_id"]
    p_id = json['person_id']
    room_id = json['room_id']
    st_dt = json["start_time"]
    et_dt = json["end_time"]

    # Checks if the room exists
    method1 = RoomDAO()
    method2 = PersonDAO()

    if not method2.check_if_person_exists(p_id):
        return jsonify("Person doesn't exist"), 404

    if not method1.check_if_room_exists(room_id):
        return jsonify("Room does not exist"), 404

    person = method2.get_person_by_id(p_id)[2]
    room = method1.get_room_by_id(room_id)

    if not (method2.access[person] == room[3]):
        return jsonify("This person is not a staff. "
                       "Only staff members can modify the availability of rooms"), 404

    method3 = AvailableRoomDAO()
    method3.update_unavailability_room(ra_id, p_id, room_id, st_dt, et_dt)
    return jsonify(True), 200


#############################
# CHECK IF ROOM HAS CONFLICT
# WITH UNAVAILABLE TIMEFRAME
#############################
def verify_unavailable_room_at_timeframe(json: dict):
    room_id = json["room_id"]
    st_dt = json["start_time"]
    et_dt = json["end_time"]

    method1 = RoomDAO()

    if not method1.check_if_room_exists(room_id):
        return jsonify("Room does not exist"), 404

    method2 = AvailableRoomDAO()
    if method2.verify_available_room_at_timeframe(room_id, st_dt, et_dt):
        return jsonify("Room has conflict"), 404

    return jsonify(True), 200


#############################
# CHECK IF ROOM HAS CONFLICT
# WITH UNAVAILABLE TIMEFRAME
#############################
# deletes the timeframe of a room who cannot be accessed given that it matches its id and the exact timeframe given
def delete_unavailable_room(json: dict):
    room_id = json["room_id"]
    st_dt = json["start_time"]
    et_dt = json["end_time"]

    method1 = RoomDAO()
    method2 = AvailableRoomDAO()
    if not method1.check_if_room_exists(room_id):
        return jsonify("Room does not exist"), 404

    method2.delete_unavailable_room_schedule(room_id, st_dt, et_dt)
    return jsonify("Unavailable Room Timeframe Deleted Successfully"), 200


#############################
# CHECK IF ROOM HAS CONFLICT
# WITH UNAVAILABLE TIMEFRAME
#############################
# Returns the timeframe for a room (all day)
def get_all_day_schedule(json: dict):
    room_id = json['room_id']
    date = json['date']

    method = AvailableRoomDAO()
    method2 = RoomDAO()

    if method2.check_if_room_exists(room_id):
        data = method.get_all_day_schedule(room_id, date)
        result: list = []
        for st_dt, et_dt, schedule, name in data:
            result.append({
                'name': name,
                'start_time': st_dt,
                'end_time': et_dt,
                'schedule_id': schedule,
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/bookings/unavailable-schedule/'
                       + str(schedule) if name == 'unavailable'
                else 'https://booking-system-pika.herokuapp.com/pika-booking/bookings/' + str(schedule)
            })
            return jsonify(result), 200
    else:
        return jsonify("Room doesn't exist"), 404


# returns the entire available rooms query
def get_all_unavailable_rooms():
    method = AvailableRoomDAO()
    available_rooms_list = method.get_all_unavailable_room()
    result = []
    for ra_id, st_dt, et_dt, room_id in available_rooms_list:
        result.append({
            'ra_id': ra_id,
            'room_id': room_id,
            'room_url': 'https://booking-system-pika.herokuapp.com/pika-booking/rooms/' + str(room_id),
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/rooms/unavailable-schedule/' + str(ra_id)
        })
    return jsonify(result), 200


def verify_available_room_at_timeframe(args):
    return None


def get_schedule(r_id):
    return None


def get_all_schedule(args):
    return None


def get_unavailable_by_ra_id(ra_id):
    return None


def get_unavailable_room_by_id(room_id):
    return None


def update_room_availability(args):
    return None