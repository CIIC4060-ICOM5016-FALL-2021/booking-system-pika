from flask import jsonify
import datetime as dt
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
        print(row, "ROW")
        result = {
            "r_building": row[0],
            "r_dept": row[1],
            "r_type": row[2]
        }
        return result

    # Overloading
    def build_room_attr_dict(self, r_id, r_building, r_dept, r_type):
        return self.build_room((r_id, r_building, r_dept, r_type))

    def build_timeslot_attrdict(self, r_id, st_dt, et_dt):
        result = {'Room ID': r_id, 'start_time': st_dt, 'finish_time': et_dt}
        return result

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
    def get_available_room_in_timeslot(self, st_dt, et_dt):
        dao = RoomDAO()
        available_rooms = dao.get_room(st_dt, et_dt)
        if not available_rooms:
            return jsonify("Room Not Found"), 404
        else:
            list = []
            for line in available_rooms:
                list.append(self.get_room_by_id(line))

            result = []
            for row in list:
                result.append(self.build_room(row))
            return jsonify(result)
