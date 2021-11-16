from flask import jsonify
import datetime as dt
from models.Room import RoomDAO


class Room:

    # Generate the Rows
    def build_room(self, row):
        result = {
            "r_id": row[0],
            "r_building": row[1],
            "r_dept": row[2],
            "r_type": row[3]
        }
        return result

    # Overloading
    def build_room_attr_dict(self, r_id, r_building, r_dept, r_type):
        return self.build_room([r_id, r_building, r_dept, r_type])

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
        r_building = json['r_type']
        r_dept = json['r_type']
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
            result = self.build_room(rooms_by_id)
            return jsonify(result), 200

    # test this
    def get_available_roomintimeslot(self, st_dt, et_dt):
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
