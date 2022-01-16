from flask import jsonify

from models.AvailableRoom import AvailableRoomDAO
from models.Room import RoomDAO


def get_all_rooms(limit_thingy=25):
    method = RoomDAO()
    count = method.count_rooms()
    if count != 0:
        data = method.get_all_rooms(limit_thingy)
        rooms = {}
        result: dict = {'count': count, 'rooms': {}}
        for index, row in enumerate(data):
            rooms[index] = {
                'r_id': row[0],
                'room_name': row[1],
                'room_type': method.rooms[row[2]],
                'url': 'https://booking-system-pika.herokuapp.com/rooms/' + str(row[0])
            }
        result['rooms'] = rooms
        return jsonify(result), 200
    else:
        return jsonify("There are no Rooms around"), 404


def create_new_room(json: dict):
    r_building = json['r_building']
    r_dept = json['r_dept']
    r_name = json['r_name']
    r_type = json['r_type']
    method = RoomDAO()
    r_id = method.create_new_room(r_name, r_building, r_dept, r_type)
    return jsonify({"r_id": r_id})


def update_room(json: dict):
    r_id = json['r_id']
    r_building = json['r_building']
    r_dept = json['r_dept']
    r_name = json['r_name']
    r_type = json['r_type']
    method = RoomDAO()
    existing_room = method.check_if_room_exists(r_id)
    if existing_room:
        result = method.update_room(r_id, r_name, r_building, r_dept, r_type)
        return jsonify(result), 200
    else:
        return jsonify("Room Not Found"), 404


def delete_room(r_id: int):
    method = RoomDAO()
    result = method.delete_room(r_id)
    if result:
        method2 = AvailableRoomDAO()
        method2.delete_unavailable_room(r_id)
        return jsonify("Room Deleted Successfully"), 200
    else:
        return jsonify("Room Not Found"), 404


def get_room(room):
    method = RoomDAO()
    if type(room) == int:
        if method.check_if_room_exists(room):
            data = method.get_room_by_id(room)
            return jsonify({
                'r_name': data[0],
                'r_building': data[1],
                'r_dept': data[2],
                'r_type': method.rooms[data[3]]
            })
        else:
            return jsonify("Room Not Found"), 404
    elif type(room) == str:
        data = method.get_room_by_name(room)
        if not data:
            return jsonify("Room does not exist"), 404
        else:
            return jsonify({
                'r_id': data[0],
                'r_building': data[1],
                'r_dept': data[2],
                'r_type': method.rooms[data[3]]
            })


def get_most_booked_rooms():
    method = RoomDAO()
    booked_rooms = method.get_most_booked_rooms()
    if not booked_rooms:
        return jsonify("There's either no Bookings or no Rooms created"), 404
    else:
        result: dict = {}
        for index, row in enumerate(booked_rooms):
            result[index] = {
                "r_id": row[0],
                "room_name": row[1],
                "timed_booked": row[2],
                "url": 'https://booking-system-pika.herokuapp.com/rooms/' + str(row[0])
            }
        return jsonify(result), 200


# Retrieves all available rooms
def get_available_rooms(json):
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    method = RoomDAO()
    data = method.find_available_rooms(st_dt, et_dt)
    if not data:
        return jsonify("Room Not Found"), 404
    else:
        result = {}
        for index, row in enumerate(data):
            result[index] = {
                'r_id': row[0],
                'room_name': row[1],
                'room_type': row[2],
                'url': 'https://booking-system-pika.herokuapp.com/rooms/' + str(row[0])
            }
        return jsonify(result), 200
