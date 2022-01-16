from flask import jsonify

from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO

from models.AvailablePerson import AvailablePersonDAO
from models.AvailableRoom import AvailableRoomDAO


def build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id):
    if type(b_id) == list:
        result = []
        for booking_id in b_id:
            result.append({
                'b_id': booking_id,
                'st_dt': st_dt,
                'et_dt': et_dt,
                'invited_id': invited_id,
                'host_id': host_id,
                'room_id': room_id
            })
        return result

    elif type(b_id) == int:
        return {
            'b_id': b_id,
            'st_dt': st_dt,
            'et_dt': et_dt,
            'invited_id': invited_id,
            'host_id': host_id,
            'room_id': room_id
        }


def create_new_booking(json: dict):
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    invited_id = json['invited_id']
    host_id = json['host_id']
    room_id = json['room_id']

    # Checking if the room exists
    method = RoomDAO()
    if method.check_if_room_exists(room_id):
        # Checking if the room is available
        method2 = AvailableRoomDAO()
        if method2.verify_available_room_at_timeframe(room_id, st_dt, et_dt):

            # Check if both the host and the invitee exist
            method3 = PersonDAO()

            if type(invited_id) == list:
                for i in invited_id:
                    if not method3.check_if_person_exists(i):
                        return jsonify("Invitee Not Found"), 404
            elif type(invited_id) == int:
                if not method3.check_if_person_exists(invited_id):
                    return jsonify("Invitee Not Found"), 404

            # Check if Host exists
            if not method3.check_if_person_exists(host_id):
                return jsonify("Host Not Found"), 404

            host = method3.get_person_by_id(host_id)
            room = method.get_room_by_id(room_id)

            # Check if host meet role requirements
            # Student can be a host for...
            # - Office
            # - Student Space
            #
            # Instructor can be a host for...
            # - Student Space
            # - Office
            # - Lab
            #
            # Professor can host for:
            # - Student Space
            # - Office
            # - Lab
            # - Classroom
            #
            # Staff can host anything

            if room[3] in method3.access[host[2]]:
                method4 = BookingDAO()
                method5 = AvailablePersonDAO()

                if type(invited_id) == list:
                    b_id: list = []
                    for inv in invited_id:
                        if method5.verify_available_person_at_timeframe(inv, st_dt, et_dt):
                            return jsonify("Person has conflict"), 404
                        b_id.append(method4.create_new_booking(st_dt, et_dt, inv, host_id, room_id))

                    result: dict = {}
                    for index, row in enumerate(b_id):
                        result[index] = build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id), 200

                    return jsonify(result)
                elif type(invited_id) == int:
                    if AvailablePersonDAO().verify_available_person_at_timeframe(invited_id, st_dt, et_dt):
                        return jsonify("Person has conflict"), 404
                    b_id = method4.create_new_booking(st_dt, et_dt, invited_id, host_id, room_id)
                    return jsonify(build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)), 200
            else:
                return jsonify("Host does not have access to this room"), 404
        else:
            return jsonify("Room has conflict"), 404
    else:
        return jsonify("Room Not Found"), 404


def get_booking_by_id(b_id: int):
    method = BookingDAO()
    if method.check_if_booking_exists(b_id):
        data = method.get_booking_by_id(b_id)
        return jsonify({
            'room_id': data['room_id'],
            'host_id': data['host_id'],
            'invited_id': data['invited_id'],
            'st_dt': data['st_dt'],
            'et_dt': data['et_dt']

        }), 200


def get_busiest_hours():
    method = BookingDAO()
    busiest = method.get_busiest_hours()
    if not busiest:
        return jsonify("Not Found"), 404
    else:
        result_list: list = []
        for row in busiest:
            result_list.append({
                'st_dt': row[0],
                'et_dt': row[1],
                'active_hour': row[2]
            })
        return jsonify(result_list), 200


def get_all_bookings(limit_thingy=125):
    return None


def update_room(json: dict):
    return None