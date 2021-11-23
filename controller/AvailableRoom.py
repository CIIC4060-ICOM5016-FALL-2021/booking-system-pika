from flask import jsonify
from controller.Room import Room
from models.AvailableRoom import AvailableRoomDAO
from models.Person import PersonDAO
from models.Room import RoomDAO


class AvailableRoom:

    def build_available_time_room_map(self, row):
        result = {
            'ra_id': row[0],
            'st_dt': row[1],
            'et_dt': row[2],
            'room_id': row[3]
        }
        return result

    def build_unavailable_room_map_attr(self, ra_id, st_dt, et_dt, r_id):
        result = {
            'ra_id': ra_id,
            'st_dt': st_dt,
            'et_dt': et_dt,
            'room_id': r_id
        }
        return result

    # Adds a new unavailable room entry, which can only be possible by staff (refer to make_room_unavailable)
    # Obviously, check if room exists before adding the entry
    def create_unavailable_room_dt(self, json):
        room_id = json['room_id']
        start_time = json['st_dt']
        end_time = json['et_dt']

        # Checks if the room exists
        room_dao = Room()
        exist = room_dao.get_room_by_id(room_id)
        if not exist:
            return jsonify("Oops! Seems this room doesn't exist"), 404

        # add entry and return back
        a_room_dao = AvailableRoomDAO()
        unavailable_dt = a_room_dao.create_unavailable_room_time(room_id, start_time, end_time)
        if unavailable_dt:
            result = {}
            return jsonify(result)

    # Wrapper, updates target room entry according to the person's role (STAFF ONLY)
    # False -> unnavailable
    # True -> Available
    def update_room_availability(self, p_id: int, r_id: int, st_dt, et_dt, state: bool = False):
        person_dao = PersonDAO()
        room_dao = RoomDAO()
        a_room_dao = AvailableRoomDAO()
        # check if person exists, and if its role matches staff
        if p_id == person_dao.R_STAFF:
            # room exists?
            if room_dao.get_room(r_id):
                # what to do
                if state:
                    result = a_room_dao.delete_unavailable_room_schedule(r_id, st_dt, et_dt)
                    return jsonify(result)
                else:
                    result = a_room_dao.create_unavailable_room_time(r_id, st_dt, et_dt)
                    return jsonify(result)
            else:
                return jsonify("Oops! Seems this room does not exists")
        else:
            return jsonify("I'm sorry, but you don't have access to make a room unavailable. Please talk to a staff "
                           "to change the availability of this room")

    # Check if the the room is unavailable at the given timeframe
    def verify_available_room_at_timeframe(self, r_id, st_dt, et_dt):
        method = AvailableRoomDAO()
        available_room_list = method.verify_available_room_at_timeframe(r_id, st_dt, et_dt)
        result_list = []
        for row in available_room_list:
            obj = self.build_available_time_room_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    # returns the entire available rooms query
    def get_all_unavailable_rooms(self):
        a_room_dao = AvailableRoomDAO()
        available_rooms_list = a_room_dao.get_all_unavailable_room()
        result_list = []
        for row in available_rooms_list:
            obj = self.build_available_time_room_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    # deletes the timeframe of a room who cannot be accessed given that it matches its id and the exact timeframe given
    def delete_unavailable_room(self, r_id, st_dt, et_dt):
        method = AvailableRoomDAO()
        result = method.delete_unavailable_room_schedule(r_id, st_dt, et_dt)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
