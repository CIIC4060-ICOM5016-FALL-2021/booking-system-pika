from flask import jsonify
from models.Room import RoomDAO


class Room:

    # Generate the Rows
    def build_room(self, row: tuple):
        result = {
            "r_building": row[0],
            "r_dept": row[1],
            "r_type": row[2]
        }
        return result

    def build_room1(self, row: tuple):
        result = {
            "r_id": row[0],
            "r_building": row[1],
            "r_dept": row[2],
            "r_type": row[3]
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

    def build_timeslot_attr_dict(self, r_id, st_dt, et_dt):
        return self.build_timeslot((r_id, st_dt, et_dt))

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
                result.append(self.build_room1(row))
            return jsonify(result)

    # Returns a query of most booked rooms
    # example: {r_id: serial, r_count: int}, in descending order
    def get_most_booked_rooms(self):
        method = RoomDAO()
        booked_rooms = method.get_most_booked_rooms()
        if not booked_rooms:
            return jsonify("There's either no Bookings or no Rooms created"), 404
        else:
            result = []
            for row in booked_rooms:
                result.append({
                    "r_id": row[0],
                    "timed_booked": row[1]
                })
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
    def update_room(self, json):
        r_id = json['r_id'] # 1
        r_building = json['r_building'] # "ADEM"
        r_dept = json['r_dept'] # "adem"
        r_type = json['r_type'] # 3
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

    # Retrieves all available rooms
    def get_available_rooms(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        method = RoomDAO()
        available_rooms = method.find_available_rooms(st_dt, et_dt)
        if not available_rooms:
            return jsonify("Room Not Found"), 404
        else:
            result_list = []
            for row in available_rooms:
                obj = self.build_room(row[1:])
                result_list.append(obj)
            return jsonify(result_list)
