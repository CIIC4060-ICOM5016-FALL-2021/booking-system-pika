from flask import jsonify

from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO

from models.AvailablePerson import AvailablePersonDAO
from models.AvailableRoom import AvailableRoomDAO


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
                        result[index] = {
                            'b_id': row,
                            'st_dt': st_dt,
                            'et_dt': et_dt,
                            'invited_id': invited_id[index],
                            'host_id': host_id,
                            'room_id': room_id,
                            'url': 'https://booking-system-pika.herokuapp.com/bookings/' + str(row)
                        }
                    return jsonify(result), 200
                elif type(invited_id) == int:
                    if AvailablePersonDAO().verify_available_person_at_timeframe(invited_id, st_dt, et_dt):
                        return jsonify("Person has conflict"), 404
                    b_id = method4.create_new_booking(st_dt, et_dt, invited_id, host_id, room_id)
                    return jsonify({
                        'b_id': b_id,
                        'st_dt': st_dt,
                        'et_dt': et_dt,
                        'invited_id': invited_id,
                        'host_id': host_id,
                        'url': 'https://booking-system-pika.herokuapp.com/bookings/' + str(b_id)
                    }), 200
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
            'room_id': data[4],
            'host_id': data[3],
            'invited_id': data[2],
            'start_time': data[0],
            'end_time': data[1],
            'room_url': 'https://booking-system-pika.herokuapp.com/rooms/' + str(data[4]),
            'host_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(data[3]),
            'invited_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(data[2])
        }), 200


def get_busiest_hours():
    method = BookingDAO()
    busiest = method.get_busiest_hours()
    if not busiest:
        return jsonify("Not Found"), 404
    else:
        result: dict = {}
        for index, row in enumerate(busiest):
            result[index] = {
                'st_dt': row[0],
                'et_dt': row[1],
                'active_hour': row[2]
            }
        return jsonify(result), 200


def get_all_bookings(limit_thingy: int = 125):
    method = BookingDAO()
    count = method.count_booking()
    if count != 0:
        data = method.get_all_booking(limit_thingy)
        bookings = {}
        result_b: dict = {'count': count, 'bookings': {}}
        for index, b_row in enumerate(data):
            bookings[index] = {
                'p_id': b_row[0],
                'first_name': b_row[1],
                'last_name': b_row[2],
                'url': 'https://booking-system-pika.herokuapp.com/bookings/' + str(b_row[0])
            }
        result_b['persons'] = bookings
        return jsonify(result_b), 200
    else:
        return jsonify("There are no Persons around"), 404


def update_room(json: dict):
    return None


def delete_booking(b_id):
    return None


def get_shared_free_timeslot(json):
    return None