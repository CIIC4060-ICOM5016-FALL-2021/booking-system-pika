from flask import jsonify

from controller.AvailableRoom import AvailableRoom
from models.Booking import BookingDAO
from models.Person import PersonDAO
from models.Room import RoomDAO

from models.AvailablePerson import AvailablePersonDAO
from models.AvailableRoom import AvailableRoomDAO

from controller.Room import Room
from controller.Person import Person
from controller.AvailablePerson import AvailablePerson


class Booking:

    def build_booking_map_dict(self, row):
        result = {'b_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'invited_id': row[3],
                  'host_id': row[4], 'room_id': row[5]}
        print(result)
        return result

    def build_booking_attr_dict(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        if type(b_id) == list:
            result = {}
            for bookingid in b_id:
                result[b_id] = self.build_booking_map_dict([bookingid, st_dt, et_dt, invited_id, host_id, room_id])
            print(result)
            return result

        elif type(b_id) == int:

            return self.build_booking_map_dict([b_id, st_dt, et_dt, invited_id, host_id, room_id])

    def build_busy_times_map_dict(self, row):
        result = {'st_dt': row[0], 'et_dt': row[1], 'times_booked': row[2]}
        return result

    def build_most_booked_users_map_dict(self, row):
        result = {'p_id': row[0], 'times_booked': row[1]}
        return result

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

    def create_new_booking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']

        # Checking if the room exists
        room_dao = RoomDAO()
        room = room_dao.get_room_dict(room_id)
        if not room:
            return jsonify("Room Not Found"), 404

        # Checking if the room is available

        # Check if both the host and the invitee exists
        person_dao = PersonDAO()

        # Invitees may be actually a list of ids, therefore, we iterate over all of em
        print(invited_id)
        if type(invited_id) == list:
            for i in invited_id:
                print(person_dao.get_person_by_id(i))
                if not person_dao.get_person_by_id(i):

                    return jsonify("Oops! Seems one of your invitees do not exists in our database. Their id is: %s",
                                   i), 404


        elif type(invited_id) == int:
            print(person_dao.get_person_by_id(invited_id))
            if not person_dao.get_person_by_id(invited_id):
                return jsonify("Oops! Seems your invitee does not exists in our database. Its id is: %s",
                               invited_id), 404

        # Checks if the Host exists
        host = person_dao.get_dict_person_by_id(host_id)
        htr = host["p_role"]  # We will use this to check the host role
        rty = room["r_type"]  # the room's type, ie, what kind of room is
        if not host:
            return jsonify("I'm sorry, but this host does not exists in our database")

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
        if (
                (htr == person_dao.R_STUDENT and (rty == room_dao.T_OFFICE or rty == room_dao.T_STY_SPACE)) or
                (htr == person_dao.R_INSTRUCTOR and (
                        rty == room_dao.T_OFFICE or rty == room_dao.T_STY_SPACE or rty == room_dao.T_LAB)) or
                (htr == person_dao.R_PROF and (
                        rty == room_dao.T_OFFICE or rty == room_dao.T_STY_SPACE or rty == room_dao.T_CLASSROOM)) or
                (htr == person_dao.R_VISITOR and (rty == room_dao.T_STY_SPACE)) or
                (htr == person_dao.R_STAFF)
        ):

            # Host has the right role, so now we check if either the host, the room or the invitees have set any
            # period to not know about the outside world. For that, we input the id, and booking timeframe,
            # and search if there's any availableperson timeframe (which again, represents a "no, plz leave me
            # alone". If there is one, check if the timeframe overlaps with the booking timeframe, if so, panic


            if(not(AvailableRoomDAO().verify_conflict_at_timeframe(room_id,st_dt,et_dt))):




                # checks if
                if type(invited_id) == list:
                    b_id=[]
                    for inv in invited_id:


                        if (AvailablePersonDAO().verify_conflict_at_timeframe(inv,st_dt,et_dt)):
                            booking_dao = BookingDAO()
                            b_id.append(booking_dao.create_new_booking(st_dt,et_dt,inv,host_id,room_id))
                            print(b_id)
                elif type(invited_id) == int:
                    if  (AvailablePersonDAO().verify_conflict_at_timeframe(invited_id,st_dt,et_dt)):
                        booking_dao = BookingDAO()
                        b_id = booking_dao.create_new_booking(st_dt, et_dt, invited_id, host_id, room_id)

                result = self.build_booking_attr_dict(b_id,st_dt,et_dt,invited_id,host_id,room_id)
                print(result)
                print(jsonify(result))
                return jsonify(result)





        else:
            return jsonify("I'm sorry,not exists in our database")

    # returns a full query of all booking entries
    def get_all_booking(self):
        method = BookingDAO()
        bookings = method.get_all_booking()
        if not bookings:
            return jsonify("No Meetings, Free day!!!!!!!")
        else:
            result_list = []
            for row in bookings:
                obj = self.build_booking_map_dict(row)
                result_list.append(obj)
        return jsonify(result_list)

    # Returns a single booking entry according to its id
    def get_booking_by_id(self, b_id):
        method = BookingDAO()
        booking_tuple = method.get_booking_by_id(b_id)
        if not booking_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_booking_map_dict(booking_tuple)
            return jsonify(result), 200

    # updates a booking entry
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

    # deletes a booking entry (sort of)
    def delete_booking(self, b_id):
        method = BookingDAO()
        result = method.delete_booking(b_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404
