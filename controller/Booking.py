from flask import jsonify
from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO
from controller.Room import Room
from controller.Person import Person
from controller.Availableperson import AvailablePerson
STUDENT = 0
PROFESSOR = 1
STAFF = 2
VISITOR = 3


LABORATORY = 1
CLASSROOM = 2
CONFERENCE_ROOM = 3
STUDY_ROOM = 4
OFFICE = 5


class Booking:

    def build_booking_map_dict(self, row):
        result = {'b_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'invited_id': row[3],
                  'host_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        return self.build_booking_map_dict([b_id, st_dt, et_dt, invited_id, host_id, room_id])


    def build_busy_times_map_dict(self, row):
        result = {'st_dt': row[0], 'et_dt': row[1], 'times_booked': row[2]}
        return result

    def build_most_booked_users_map_dict(self, row):
        result = {'p_id': row[0], 'times_booked': row[1]}
        return result


    def create_new_booking(self, p_id, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']

        booking_dao = BookingDAO()
        person_dao = PersonDAO()
        room_dao = RoomDAO()

        # TODO Build BY TYPE Method (DONE)
        r_type = room_dao.get_room_by_type(room_id)
        if not room_dao.get_room(room_id):
            return jsonify("Room Not Found"), 404

        r_type = r_type[2]

        method = Person()
        role = method.get_user_role_by_id(p_id)
        
        if role == Person.ROLE_STUDENT or (role == Person.ROLE_PROF and r_type == Room.TYPE_CLASSROOM)  or \
                (role == Person.ROLE_STUDENT and r_type == Room.TYPE_STUDY_SPACE):

            # TODO Design this extra function
            available_room = Room().get_available_room_by_timeslot(room_id, st_dt, et_dt)

            available_person = AvailablePerson().verify_available_user_at_timeframe(p_id, st_dt, et_dt)
            if not available_person:
                return jsonify("User is not available during specified time"), 409

            if not available_room:
                return jsonify("Sorry, this room is not available at said time")

    #         result_list.append(obj)
    #     return jsonify(result_list)
    def get_free_time_users(self, b_id, json):
        bookingmethod = BookingDAO()

        selectedbooking = bookingmethod.get_booking_by_id(b_id)
        if not selectedbooking:
            return jsonify("Booking Not Found"), 404

        meeting_invited = bookingmethod.get_invited_list_by_meeting(b_id)
        meeting_invited.append(selectedbooking[3])
        result = {}
        person_dao = PersonDAO()
        return jsonify(result)
    def update_booking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        b_id = json['b_id']
        method = BookingDAO()
        updatedinfo = method.update_booking(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        if updatedinfo:
            result = self.build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
            return jsonify(result)
        else:
            return jsonify('Not found person')

    def delete_booking(self, b_id):
        method = BookingDAO()
        result = method.delete_booking(b_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404
