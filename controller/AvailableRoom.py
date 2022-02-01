from flask import jsonify
from models.AvailableRoom import AvailableRoomDAO
from models.Person import PersonDAO
from models.Room import RoomDAO


def schedule_stuff(data):
    result_st_dt = []
    result_et_dt = []
    for st_dt, et_dt in data:
        result_et_dt.append(et_dt)
        result_st_dt.append(st_dt)
    result = {
        "st_dt": result_st_dt,
        "et_dt": result_et_dt
    }
    return result


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
        unavailablecreator = json['person_id']

        # Checks if the room exists
        room_dao = RoomDAO()
        person_dao = PersonDAO()
        exist = room_dao.get_room(room_id)
        validhost = person_dao.get_person_role_by_id(unavailablecreator)
        if not exist:
            return jsonify("Oops! Seems this room doesn't exist "), 404

        if not validhost:
            return jsonify("I'm sorry, but this person does not exists in our database"), 200
        elif not (validhost == person_dao.R_STAFF):
            return jsonify("I'm sorry, but this person is not a staff! "
                           "Only staff members can modify the availability of rooms"), 200
        # add entry and return back
        a_room_dao = AvailableRoomDAO()
        ra_id = a_room_dao.create_unavailable_room_time(room_id, start_time, end_time)
        result = self.build_available_time_room_map([ra_id, start_time, end_time, room_id])
        return jsonify(result)

    # Wrapper, updates target room entry according to the person's role (STAFF ONLY)
    # False -> unnavailable
    # True -> Available
    def update_room_availability(self, json):
        p_id = json["p_id"]
        r_id = json["r_id"]
        st_dt = json["st_dt"]
        et_dt = json["et_dt"]
        state = json["state"]

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
    def verify_available_room_at_timeframe(self, json):
        r_id = json["r_id"]
        st_dt = json["st_dt"]
        et_dt = json["et_dt"]

        method = AvailableRoomDAO()
        available_room_list = method.verify_available_room_at_timeframe(r_id, st_dt, et_dt)
        result = {"Unavailable": available_room_list[0]}
        return jsonify(result)

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
    def delete_unavailable_room(self, json):
        r_id = json['r_id']
        st_dt = json['st_dt']
        et_dt = json['et_dt']

        method = AvailableRoomDAO()
        result = method.delete_unavailable_room_schedule(r_id, st_dt, et_dt)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")

    # Returns the timeframe for a room (all day)
    def get_all_day_schedule(self, json):
        room_id = json['room_id']
        date = json['date']

        dao = AvailableRoomDAO()
        room_dao = RoomDAO()

        existing_room = room_dao.get_room(room_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        else:
            res = dao.get_all_day_schedule(room_id, date)
            result: list = []
            for row in res:
                result.append({
                    "st_dt": row[0],
                    "et_dt": row[1],
                    "b_name": row[2],
                    "p_fname": row[3],
                    "p_lname": row[4]
                })
            return jsonify(result), 200

    def get_schedule(self, room_id):
        dao = AvailableRoomDAO()
        room_dao = RoomDAO()

        existing_room = room_dao.get_room(room_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        else:
            res = dao.get_all_schedule(room_id)
            result = schedule_stuff(res)
            return jsonify(result), 200

    def get_unavailable_room_by_room_id(self, room_id):
        dao = AvailableRoomDAO()
        room_dao = RoomDAO()

        existing_room = room_dao.get_room(room_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        else:
            res = dao.get_unavailable_room_by_id(room_id)
            result: list = []
            for st_dt, et_dt, ra_id in res:
                result.append({
                    "st_dt": st_dt,
                    "et_dt": et_dt,
                    "ra_id": ra_id
                })
            return jsonify(result), 200

    def get_unavailable_by_ra_id(self, room_id):
        dao = AvailableRoomDAO()
        room_dao = RoomDAO()

        existing_room = room_dao.get_room(room_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        else:
            res = dao.get_unavailable_room_by_ra_id(room_id)
            result_st_dt = []
            result_et_dt = []
            for st_dt, et_dt in res:
                result_et_dt.append(et_dt)
                result_st_dt.append(st_dt)
            result = {
                "st_dt": result_st_dt,
                "et_dt": result_et_dt
            }
            return jsonify(result), 200

    def delete_unavailable_room_by_room_id(self, room_id):
        method = AvailableRoomDAO()
        result = method.delete_all_unavailable_room_by_room_id(room_id)
        if result:
            return jsonify("DELETED"), 201
        else:
            return jsonify("NOT FOUND"), 404

    def delete_unavailable_room_by_ra_id(self, ra_id):
        method = AvailableRoomDAO()
        result = method.delete_all_unavailable_room_by_ra_id(ra_id)
        if result:
            return jsonify("DELETED"), 201
        else:
            return jsonify("NOT FOUND"), 404

    def get_all_day_schedule_by_role(self, json):
        p_role = json['p_role']
        date = json['date']
        dao = AvailableRoomDAO()
        res = dao.get_all_day_schedule_by_role(p_role, date)
        result = []
        for row in res:
            result.append({
                "r_id": row[0],
                "r_name": row[1],
            })
        return jsonify(result), 200

    def get_rooms_by_role_timeframe(self, json):
        p_role = json['p_role']
        st_dt = json['st_dt']
        et_dt = json['et_dt']

        list_access = PersonDAO.access[PersonDAO.roledict[p_role]]
        listresult = []
        for acc in list_access:
            print(acc)
            listresult.append(acc)


        dao = AvailableRoomDAO()
        res = dao.get_rooms_by_role_timeframe(p_role, st_dt, et_dt,listresult)
        result = []
        for row in res:
            result.append({
                "r_id": row[0],
                "r_name": row[1],
            })
        return jsonify(result), 200