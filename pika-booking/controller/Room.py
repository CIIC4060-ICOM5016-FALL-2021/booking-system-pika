from flask import jsonify
import datetime as dt
from models.Room import RoomDAO


class Room:

    # Generate the Rows
    def build_room(self, row):
        result = {"r_id": row[0], "r_building": row[1], "r_dept": row[2], "r_type": row[3]}
        return result

    # Overloading
    def build_room_args(self, r_id, r_building, r_dept, r_type):
        return self.build_room([r_id, r_building, r_dept, r_type])

    # Create
    #
    # Creates a new Room]
    # It first checks if exists using id
    #
    def create_room(self, json):
        r_id = json['r_id']
        r_building = json['r_building']
        r_dept = json['r_dept']
        r_type = json['r_type']
        dao = RoomDAO()
        existing_room = dao.get_room(r_id)

        # Room with such name dos not exist
        if not existing_room:
            room_id = dao.create_new_room(r_building, r_dept, r_type)
            result = self.build_room_args(r_id, r_building, r_dept, r_type)
            return jsonify(result), 201
        else:
            return jsonify("A room with that name already exists"), 409

