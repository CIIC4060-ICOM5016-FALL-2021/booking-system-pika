from flask import jsonify
from flask.json import JSONDecoder

from controller.AvailableRoom import AvailableRoom
from models.Booking import BookingDAO
from models.Room import RoomDAO
from controller.Room import Room
from controller.Person import Person
from controller.AvailablePerson import AvailablePerson

STUDENT = 1
PROFESSOR = 2
STAFF = 3
VISITOR = 4

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

    # def getFreeTimeForUsers(self, booking_id, json):
    #     bookingmethod = BookingDAO()
    #
    #     selectedbooking = bookingmethod.get_booking_by_id(b_id)
    #     if not selectedbooking:
    #         return jsonify("Booking Not Found"), 404
    #
    #     meeting_invited = bookingmethod.get_invited_list_by_meeting(b_id)
    #     meeting_invited.append(selectedbooking[3])
    #     result = {}
    #     person_dao = PersonDAO()
    #
    #     result_list = []
    #     for p_id in meeting_invited:
    #         user = person_dao.get_person_by_id(p_id)
    #         if not user:  # User Not Found
    #             return jsonify("User Not Found"), 404
    #         user_unavailable_time_slots = person_dao.get_unavailable_time_of_person_by_id(p_id)
    #         # start_date = date + " 0:00"
    #         # start_time = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    #         # finish_date = date + " 23:59"
    #         # finish_date = dt.datetime.strptime(finish_date, '%Y-%m-%d %H:%M')
    #
    #
    #         bookingmethod.format_time_stamp()
    #
    #         for slot in user_unavailable_time_slots:
    #             if slot[1] > start_time and slot[2] < finish_date:  # Compare as time (not string)
    #                 finish_time = slot[1]
    #                 obj = BaseUser().build_time_slot_attr_dict(start_time, finish_time)
    #                 result_list.append(obj)
    #                 start_time = slot[2]
    #         finish_time = finish_date
    #         result_list.append(BaseUser().build_time_slot_attr_dict(start_time, finish_time))  # Stores Free Time String
    #
    #     users_in_meeting = len(user_array)
    #     for string_date in result_list:
    #         # Intersection will all users
    #         if self.dateIntersectionCount(string_date, result_list) == users_in_meeting:
    #             return jsonify("All Users in Booking are free at the following hour", string_date), 200
    #     return jsonify("No overlapping times available between users at the specified date"), 200

    def create_new_booking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']

        room_dao = RoomDAO()

        room = room_dao.get_room(room_id)
        if not room:
            return jsonify("Room Not Found"), 404

        r_type = room[2]

        method = Person()
        role = method.get_person_role_by_id(host_id)

        if ((role["p_role"] == Person.ROLE_STAFF) or
                ((role["p_role"] == Person.ROLE_PROF) and (r_type == Room.TYPE_CLASSROOM)) or
                ((role["p_role"] == Person.ROLE_STUDENT) and (r_type == Room.TYPE_STUDY_SPACE))):

            # Checking if person and room are available at given timeframe
            available_room = AvailableRoom().verify_available_room_at_timeframe(room_id, st_dt, et_dt)
            available_person = AvailablePerson().verify_available_user_at_timeframe(invited_id, st_dt, et_dt)
            if not available_person:
                return jsonify("User is not available during specified time"), 409

            if not available_room:
                return jsonify("Sorry, this room is not available at said time"), 409

        # # for line in invited_id:
        # available_invitee = AvailablePerson().verify_available_user_at_timeframe(invited_id, st_dt, et_dt)
        # print("invitees seems to be working")
        # if not available_invitee:
        #     return jsonify("One or more Invitee not available")
        #
        # AvailablePerson().create_unavailable_time_schedule(host_id, st_dt, et_dt)
        #
        # AvailableRoom().create_unavailable_time_schedule(room_id, st_dt, et_dt)
        #
        # # for j in invited_id:
        # AvailablePerson().create_unavailable_time_schedule(j, st_dt, et_dt)
        # method = BookingDAO()
        # b_id = method.create_new_booking(st_dt, et_dt, invited_id, host_id, room_id)
        # result = self.build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        # return jsonify(result)
    #         result_list.append(obj)
    #     return jsonify(result_list)


    def get_all_booking(self):
        method = BookingDAO()
        bookings = method.get_all_booking()
        if not bookings:
            return jsonify("No Meetings, Free day!!!!!!!")
        else:
            result_list = []
            for row in bookings:
                obj = self.build_available_time_person_map(row)
                result_list.append(obj)
        return jsonify(result_list)

    def get_booking_by_id(self, b_id):
        method = BookingDAO()
        booking_tuple = method.get_booking_by_id(b_id)
        if not booking_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_booking_map_dict(booking_tuple)
            return jsonify(result), 200

    def update_booking(self, b_id, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
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
