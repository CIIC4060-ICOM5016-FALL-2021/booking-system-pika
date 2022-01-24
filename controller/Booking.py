from flask import jsonify

from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO

from models.AvailablePerson import AvailablePersonDAO
from models.AvailableRoom import AvailableRoomDAO


class Booking(object):

    def build_timeframe_attrdict(self, row):
        result = {'start_time': row[0], 'finish_time': row[1], 'activebooking': row[2]}
        return result

    def build_booking_map_dict(self, row):
        result = {'b_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'invited_id': row[3],
                  'host_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):

        if type(b_id) == list:
            result = []
            for bookingid in b_id:
                result.append(self.build_booking_map_dict([bookingid, st_dt, et_dt, invited_id, host_id, room_id]))
            return result

        elif type(b_id) == int:

            return self.build_booking_map_dict([b_id, st_dt, et_dt, invited_id, host_id, room_id])

    """
    This method, as the name says, communicates with the model, which then creates a new booking entry
    To do this, the controller side first checks if:
    a) The room exists
    b) The host and invitee/s exists
    c) Both the invitee and the host are available in set timeframe
    d) The room is also available in set timeframe
    
    NOTE: Certain rooms cannot be added depending of the host's role
    
    Breaking each part...
    """

    def create_new_booking(self, json: dict):
        b_name = json['b_name']
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        print(json)
        # Checking if the room exists
        method = RoomDAO()
        if method.check_if_room_exists(room_id):
            # Checking if the room is available
            method2 = AvailableRoomDAO()
            if method2.verify_available_room_at_timeframe(room_id, st_dt, et_dt):
                print("WRKS HERE")
                # Check if both the host and the invitee exist
                method3 = PersonDAO()

                if type(invited_id) == list:
                    print("invited_id IS LIST")
                    for i in invited_id:
                        if not method3.check_if_person_exists(i):
                            return jsonify("Invitee Not Found"), 404
                elif type(invited_id) == int:
                    print("invited_id IS INT")
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
                print("Still working hehe")
                if room[3] in method3.access[host[2]]:
                    method4 = BookingDAO()
                    method5 = AvailablePersonDAO()
                    print("Also working over here")
                    print("invited datatype", type(invited_id))
                    if type(invited_id) == list:
                        b_id: list = []
                        for inv in invited_id:
                            if not method5.verify_available_person_at_timeframe(inv, st_dt, et_dt):
                                return jsonify("Person has conflict"), 404
                            b_id.append(method4.create_new_booking(b_name, st_dt, et_dt, inv, host_id, room_id))
                        print("working on the list case")
                        result = []
                        for index, row in enumerate(b_id):
                            result.append({
                                'b_id': row,
                                'st_dt': st_dt,
                                'et_dt': et_dt,
                                'invited_id': invited_id[index],
                                'host_id': host_id,
                                'r_id': room_id,
                            })
                        return jsonify(result), 200
                    elif type(invited_id) == int:
                        print("case for int")
                        if AvailablePersonDAO().verify_available_person_at_timeframe(invited_id, st_dt, et_dt):
                            return jsonify("Person has conflict"), 406
                        print("No explosions on the checks (int)")
                        b_id = method4.create_new_booking(b_name, st_dt, et_dt, invited_id, host_id, room_id)
                        return jsonify({
                            'b_name': b_name,
                            'b_id': b_id,
                            'st_dt': st_dt,
                            'et_dt': et_dt,
                            'invited_id': invited_id,
                            'host_id': host_id,
                            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/bookings/' + str(b_id)
                        }), 200
                else:
                    return jsonify("Host does not have access to this room"), 406
            else:
                return jsonify("Room has conflict"), 406
        else:
            return jsonify("Room Not Found"), 404

    # returns a full query of all booking entries
    def get_all_booking(self, limit_thingy=125):
        method = BookingDAO()
        count = method.count_booking()
        if count != 0:
            data = method.get_all_booking(limit_thingy)
            result = []
            for b_id, b_name, st_dt, et_dt, invited_id, host_id, room_id in data:
                result.append({
                    'b_id': b_id,
                    'b_name': b_name,
                    'st_dt': st_dt,
                    'et_dt': et_dt,
                    'invited_id': invited_id,
                    'host_id': host_id,
                    'room_id': room_id
                })
            return jsonify(result), 200
        else:
            return jsonify("No Bookings Found"), 404

    def get_bookings_by_host(self, host_id):
        method = BookingDAO()
        booked_rooms = method.get_bookings_by_host(host_id)
        if not booked_rooms:
            return jsonify("There's either no Bookings with this host"), 404
        else:
            result = []
            for b_id, st_dt, et_dt, invited_id, host_id, room_id, b_name in booked_rooms:
                result.append({
                    'b_id': b_id,

                    'st_dt': st_dt,
                    'et_dt': et_dt,
                    'invited_id': invited_id,
                    'host_id': host_id,
                    'room_id': room_id,
                    'b_name': b_name
                })
            return jsonify(result), 200
    # Returns a single booking entry according to its id

    def get_meetings_by_id(self, booking_id):
        booking_dao = BookingDAO()
        meeting_by_id = booking_dao.get_meetings_by_id(booking_id)

        if not meeting_by_id:
            return jsonify("There's no meetings by such booking id!"), 404
        else:
            result: list = []
            for b_id, b_name, st_dt, et_dt, invited_id, host_id, room_id in meeting_by_id:
                result.append({
                    "b_id": b_id,
                    "b_name": b_name,
                    "st_dt": st_dt,
                    "et_dt": et_dt,
                    "invited_id": invited_id,
                    "host_id": host_id,
                    "room_id": room_id
                })
            return jsonify(result), 200

    def get_booking_by_id(self, b_id):

        method = BookingDAO()
        b_name, st_dt, et_dt, invited_id, host_id, room_id = method.get_booking_by_id(b_id)
        if not room_id:
            return jsonify("Not Found"), 404
        else:
            return jsonify({
                "b_name": b_name,
                "st_dt": st_dt,
                "et_dt": et_dt,
                "invited_id": invited_id,
                "host_id": host_id,
                "room_id": room_id
            }), 200

    def get_host_at_dt(self, json):
        room_id = json['room_id']
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        method = BookingDAO()
        host_id = method.get_host_at_dt(room_id, st_dt, et_dt)

        if not host_id:
            return jsonify("Not Found"), 404
        else:
            result = {}
            result['host_id'] = host_id
            return jsonify(result), 200

    # updates a booking entry
    def update_booking(self, json):
        b_id = json['b_id']
        b_name = json['b_name']
        st_dt = json['start_time']
        et_dt = json['end_time']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        method = BookingDAO()
        updatedinfo = method.update_booking(b_id, b_name, st_dt, et_dt, invited_id, host_id, room_id)
        if updatedinfo:
            return jsonify({
                'b_id': b_id,
                'b_name': b_name,
                'st_dt': st_dt,
                'et_dt': et_dt,
                'invited_id': invited_id,
                'host_id': host_id,
                'room_id': room_id
            }), 200
        else:
            return jsonify('Unable to Update Booking'), 404

    def delete_booking(self, b_id):
        if type(b_id) == int:
            b_id = (b_id,)
        else:
            b_id = tuple(b_id)
        method = BookingDAO()
        result = method.delete_booking(b_id)
        if result:
            return jsonify("Booking Successfully Deleted"), 200
        else:
            return jsonify("No Bookings Found"), 404

    def get_shared_free_timeslot(self, json):
        booking_dao = BookingDAO()
        # booking_id = json['b_id']
        date = json['date']
        existent_booking = self.get_meetings_by_id(json)
        print(existent_booking)
        person_dao = PersonDAO()
        person_tupple = []
        for value in existent_booking.values():
            person = person_dao.get_person_by_id(value['invited_id'])

            if not person:
                return jsonify("Person not found"), 404

            # hours = AvailablePersonDAO().get_all_day_schedule(value['invited_id'], date)

            person_tupple.append(value['invited_id'])

        free_time = booking_dao.get_free_time_of_day(tuple(person_tupple),date)

        mega_map = {}
        print(free_time, "This is the free time")
        for i, b in enumerate(free_time):
            print(b)
            mega_map[i] = {'free_start': str(b[0]), 'free_end': str(b[1]), 'delta_time': str(b[2])}
        print(mega_map)
        return jsonify(mega_map)

    def get_busiest_hours(self):
        method = BookingDAO()
        busiest = method.get_busiest_hours()
        if not busiest:
            return jsonify("Not Found"), 404
        else:
            result_list = []
            for row in busiest:
                obj = self.build_timeframe_attrdict(row)
                result_list.append(obj)
            return jsonify(result_list)

    def get_shared_free_timeslot_users(self, json): ### PROB HERE
        booking_dao = BookingDAO()
        person_tupple = json['invited_id']
        date = json['date']

        free_time = booking_dao.get_free_time_of_day(tuple(person_tupple),date)
        mega_map = []
        for b in free_time:
            mega_map.append({'free_start': str(b[0]), 'free_end': str(b[1]), 'delta_time': str(b[2])})
        print(mega_map)
        return jsonify(mega_map)

    def get_all_meetings(self):
        method = BookingDAO()
        count = method.count_booking()
        if count != 0:
            data = method.get_all_meetings()
            result = []
            for et_dt, st_dt, b_name, host_id, room_id, num_invitees in data:
                result.append({
                    "b_name": b_name,
                    "st_dt": st_dt,
                    "et_dt": et_dt,
                    "host_id": host_id,
                    "room_id": room_id
                })
            return jsonify(result), 200
        else:
            return jsonify("No Bookings Found"), 404

    def get_meetings_by_host_id(self, host_id):
        method = BookingDAO()
        data = method.get_meetings_by_host(host_id)
        if not data:
            return jsonify("Not Found"), 404
        result = []
        for b_id, b_name, st_dt, et_dt in data:
            result.append({
                "b_id": b_id,
                "b_name": b_name,
                "st_dt": st_dt,
                "et_dt": et_dt
            })
        return jsonify(result), 200
