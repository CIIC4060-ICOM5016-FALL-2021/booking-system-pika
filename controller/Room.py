from flask import jsonify
from models.Room import RoomDAO


class Room:
    # CONSTANTS N STUFF
    TYPE_LAB = 1
    TYPE_CLASSROOM = 2
    TYPE_CONFERENCE = 3
    TYPE_OFFICE = 4
    TYPE_STUDY_SPACE = 5

    # Generate the Rows
    def build_room(self, row: tuple):
        result = {
            "r_building": row[0],
            "r_dept": row[1],
            "r_type": row[2]
        }
        return result

    # Overloading
    def build_room_attr_dict(self, r_id, r_building, r_dept, r_type):
        return self.build_room((r_id, r_building, r_dept, r_type))

    def build_timeslot(self, row: tuple):
        print(row, "ROW")
        result = {
            "r_id": row[0],
            "st_dt": row[1],
            "et_dt": row[2]
        }
        return result

    def build_most_booked_room(self, row: tuple):
        result = {
            "r_id": row[0],
            "timed_booked": row[1]
        }
        return result

    def build_timeslot_attr_dict(self, r_id, st_dt, et_dt):
        return self.build_timeslot((r_id, st_dt, et_dt))

    # Adds a query where timeframe which represents the time such room will not be available
    def add_unavailable_time_schedule(self, r_id, json):
        method = RoomDAO()
        start_time = json['st_dt']
        end_time = json['et_dt']
        exist = self.get_room_by_id(r_id)
        if not exist:
            return jsonify("Person doesn't exist")

        unavailable_schedule = method.create_unavailable_room_time(r_id, start_time, end_time)
        if unavailable_schedule:
            result = {}
            return jsonify(result)

    # Read
    #
    # Gets All Rooms

    def get_all_rooms(self):
        dao = RoomDAO()
        all_rooms = dao.get_all_rooms()
        if not all_rooms:
            return jsonify("There's no rooms! It feels, lonely.."), 404
        else:
            result = []
            for row in all_rooms:
                result.append(self.build_room(row))
            return jsonify(result)

    # Returns a query of most booked rooms
    # example: {r_id: serial, r_count: int}, in descending order
    def get_most_booked_rooms(self):
        method = RoomDAO()
        booked_rooms = method.get_most_booked_rooms()
        if not booked_rooms:
            return jsonify("Not Found"), 404
        else:
            result = []
            for row in booked_rooms:
                a = self.build_most_booked_room(row)
            return jsonify(result), 200

    # Create
    #
    # Creates a new Room]
    # It first checks if exists using id
    #
    def create_new_room(self, json):
        # r_id = json['r_id']
        r_building = json['r_building']
        r_dept = json['r_dept']
        r_type = json['r_type']
        dao = RoomDAO()
        # existing_room = dao.get_room(r_id)

        # Room with such name dos not exist
        # if not existing_room:
        room_id = dao.create_new_room(r_building, r_dept, r_type)
        result = self.build_room_attr_dict(room_id, r_building, r_dept, r_type)
        return jsonify(result), 201
        # else:
        #     return jsonify("A room with that ID already exists"), 409

    # Delete
    def delete_room(self, r_id):
        dao = RoomDAO()
        result = dao.delete_room(r_id)
        if result:
            return jsonify("Room Deleted Successfully"), 200
        else:
            return jsonify("Room Not Found"), 404

    # Update
    def update_room(self, r_id, json):
        r_building = json['r_building']
        r_dept = json['r_dept']
        r_type = json['r_type']
        dao = RoomDAO()
        existing_room = dao.get_room(r_id)
        if not existing_room:
            return jsonify("Room Not Found"), 404
        else:
            dao.update_room(r_id, r_building, r_dept, r_type)
            result = self.build_room_attr_dict(r_id, r_building, r_dept, r_type)
            return jsonify(result), 200

    # Put a number and get some room thingy
    def get_room_by_id(self, r_id):
        dao = RoomDAO()
        rooms_by_id = dao.get_room(r_id, )
        if not rooms_by_id:
            return jsonify("There's no rooms!"), 404
        else:
            print(rooms_by_id)
            result = self.build_room(rooms_by_id[0])
            return jsonify(result), 200

    # test this
    #TODO FIX
    def get_available_room_in_timeslot(self, st_dt, et_dt):
        dao = RoomDAO()
        available_rooms = dao.get_available_rooms_by_timeslot(st_dt, et_dt)
        if not available_rooms:
            return jsonify("Room Not Found"), 404
        else:
            return_list = []
            for line in available_rooms:
                return_list.append(self.get_room_by_id(line))

            result = []
            for row in return_list:
                result.append(self.build_room(row))
            return jsonify(result)

    def room_by_id_exist(self, p_id):
        method = RoomDAO()
        room_tuple = method.get_room(p_id)
        if not room_tuple:
            return False
        else:
            return True

    def get_all_available_rooms(self):
        method = RoomDAO()
        available_users_list = method.get_all_available_rooms()
        result_list = []
        for row in available_users_list:
            obj = self.build_timeslot(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_rooms(self, args: dict):
        dao = RoomDAO()
        rooms_by = dao.get_room_by(args)
        if not rooms_by:
            return jsonify("There's no rooms!"), 404
        else:
            result_list = []
            for row in rooms_by:
                result_list.append(self.build_room(row))
            return jsonify(result_list), 200
