from flask import jsonify

from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO

from models.AvailablePerson import AvailablePersonDAO
from models.AvailableRoom import AvailableRoomDAO


def create_new_booking(json: dict):
    b_name = json['booking_name']
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
                        b_id.append(method4.create_new_booking(b_name, st_dt, et_dt, inv, host_id, room_id))

                    result: dict = {'booking_name': b_name, 'bookings': {}}
                    bookings: dict = {}
                    for index, row in enumerate(b_id):
                        bookings[index] = {
                            'b_id': row,
                            'st_dt': st_dt,
                            'et_dt': et_dt,
                            'invited_id': invited_id[index],
                            'host_id': host_id,
                            'room_id': room_id,
                            'url': 'https://booking-system-pika.herokuapp.com/bookings/' + str(row)
                        }
                        result['bookings'] = bookings
                    return jsonify(result), 200
                elif type(invited_id) == int:
                    if AvailablePersonDAO().verify_available_person_at_timeframe(invited_id, st_dt, et_dt):
                        return jsonify("Person has conflict"), 404
                    b_id = method4.create_new_booking(b_name, st_dt, et_dt, invited_id, host_id, room_id)
                    return jsonify({
                        'booking_name': b_name,
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


def get_booking(booking):
    method = BookingDAO()
    if type(booking) == int:
        if method.check_if_booking_exists(booking):
            data = method.get_booking_by_id(booking)
            return jsonify({
                'booking_name': data[0],
                'room_id': data[1],
                'host_id': data[2],
                'invited_id': data[3],
                'start_time': data[4],
                'end_time': data[5],
                'room_url': 'https://booking-system-pika.herokuapp.com/rooms/' + str(data[1]),
                'host_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(data[2]),
                'invited_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(data[3])
            }), 200
        else:
            return jsonify("Booking Id Not Found"), 404
    elif type(booking) == str:
        booking = str(booking).replace('-', ' ')

        if method.check_if_booking_name_exists(booking):
            data = method.get_booking_by_name(booking)
            result: dict = {booking: {}}
            b = {}
            for index, row in enumerate(data):
                b[index] = {
                    'b_id': row[0],
                    'room_id': row[1],
                    'host_id': row[2],
                    'invited_id': row[3],
                    'start_time': row[4],
                    'end_time': row[5],
                    'room_url': 'https://booking-system-pika.herokuapp.com/rooms/' + str(row[1]),
                    'host_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(row[2]),
                    'invited_url': 'https://booking-system-pika.herokuapp.com/persons/' + str(row[3])

                }
            result[booking] = b
            return jsonify(result), 200
    else:
        return jsonify("TypeError. Input booking is not an integer (booking id) nor a string (booking name)"), 404


def get_all_bookings(limit_thingy: int = 125):
    method = BookingDAO()
    count = method.count_booking()
    if count != 0:
        data = method.get_all_booking(limit_thingy)
        bookings = {}
        result_b: dict = {'count': count, 'bookings': {}}
        for index, b_row in enumerate(data):
            bookings[index] = {
                'b_id': b_row[0],
                'start_time': b_row[1],
                'end_time': b_row[2],
                'url': 'https://booking-system-pika.herokuapp.com/bookings/' + str(b_row[0])
            }
        result_b['bookings'] = bookings
        return jsonify(result_b), 200
    else:
        return jsonify("No Bookings Found"), 404


def delete_booking(b_id):
    method = BookingDAO()
    if method.check_if_booking_exists(b_id):
        method.delete_booking(b_id)
        return jsonify("Booking Deleted Successfully"), 200
    else:
        return jsonify("No Bookings Found")


def update_booking(json: dict):
    b_id = json['b_id']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    invited_id = json['invited_id']
    host_id = json['host_id']
    room_id = json['room_id']
    method = BookingDAO()
    if method.check_if_booking_exists(b_id):
        method.update_booking(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        return jsonify(True), 200
    else:
        return jsonify('Booking Not Found'), 404


def delete_booking_host(json: dict):
    host = json['host_id']
    st_dt = json['start_time']
    et_dt = json['end_time']

    method = BookingDAO()
    method2 = PersonDAO()
    if method2.check_if_person_exists(host):
        data = method.delete_booking_host(host, st_dt, et_dt)
        result = {}
        for index, row in enumerate(data):
            result[index] = {
                'b_id': row
            }
        return jsonify(result), 200
    else:
        return jsonify('Host Not Found'), 404


def delete_invitee_from_booking(json: dict):
    host_id = json['host_id']
    invitee = json['invitee']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    method = BookingDAO()
    method2 = PersonDAO()
    if not method2.check_if_person_exists(host_id):
        return jsonify("Host Not found"), 404
    if type(invitee) == list:
        for i in invitee:
            if not method2.check_if_person_exists(i):
                return jsonify("Invitee Not found. ID is" + str(i)), 404
        b_id = {}
        for index, row in enumerate(invitee):
            b_id[index] = {
                'b_id': method.delete_booking_invitee(host_id, row, st_dt, et_dt)
            }
        return jsonify(b_id), 200
    elif type(invitee) == int:
        if not method2.check_if_person_exists(invitee):
            return jsonify({
                'b_id': method.delete_booking_invitee(host_id, invitee, st_dt, et_dt)
            })


#####################################################################
def get_free_time_of_day(json):
    booking_dao = BookingDAO()
    booking_id = json['b_id']
    date = json['date']
    # existent_booking = self.get_meetings_by_id(json).json
    # print(existent_booking)
    # person_dao = PersonDAO()
    # person_tupple = []
    # for value in existent_booking.values():
    #     person = person_dao.get_person_by_id(value['invited_id'])
    #
    #     if not person:
    #         return jsonify("Person not found"), 404
    #
    #     # hours = AvailablePersonDAO().get_all_day_schedule(value['invited_id'], date)
    #
    #     person_tupple.append(value['invited_id'])
    #
    # free_time = booking_dao.get_free_time_of_day(tuple(person_tupple), date)
    #
    # mega_map = {}
    # print(free_time, "This is the free time")
    # for i, b in enumerate(free_time):
    #     print(b)
    #     mega_map[i] = {'free_start': str(b[0]), 'free_end': str(b[1]), 'delta_time': str(b[2])}
    # print(mega_map)
    # return jsonify(mega_map)


#########################################
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


#
def get_persons_who_booked_in_room_at_given_timeframe():
    cursor = ''
