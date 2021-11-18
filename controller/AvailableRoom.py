from flask import jsonify
from controller.Room import Room
from models.AvailableRoom import AvailableRoomDAO


class AvailableRoom:

    def build_available_time_room_map(self, row):
        result = {'ra_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'room_id': row[3]}
        return result


    def build_unavailable_time_room_info(self, row):
        result = {'st_dt': row[0],
                  'et_dt': row[1], 'room_id': row[2]}
        return result

    def build_unavailable_room_attr_dict(self, pa_id, st_dt, et_dt, r_id):
        result = {'ra_id': pa_id, 'st_dt': st_dt,
                  'et_dt': et_dt, 'room_id': r_id}
        return result
    def add_unavailable_time_schedule(self, r_id, json):
        method = Room()
        start_time = json['st_dt']
        end_time = json['et_dt']
        exist = method.get_room_by_id(r_id)
        if not exist:
            return jsonify("room doesn't exist")

        unavailable_schedule = method.add_unavailable_time_schedule(r_id, start_time, end_time)
        if unavailable_schedule:
            result = {}
            return jsonify(result)

    def verify_available_room_at_timeframe(self, r_id, st_dt, et_dt):
        method = AvailableRoomDAO()
        available_room_list = method.verify_available_room_at_timeframe(r_id, st_dt, et_dt)
        result_list = []
        for row in available_room_list:
            obj = self.build_available_time_room_map(row)
            result_list.append(obj)
        print("ITS WORKING OVER HERE at aval room")
        return jsonify(result_list)

    def get_all_unavailable_rooms(self):
        method = Room()
        available_rooms_list = method.get_all_available_rooms()
        result_list = []
        for row in available_rooms_list:
            obj = self.build_available_time_room_map(row)
            result_list.append(obj)
        return jsonify(result_list)


    def create_unavailable_time_schedule(self, json):
        method = Room()
        room_id = json['room_id']
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        exist = method.room_by_id_exist(room_id)
        if not exist:
            return jsonify("Room doesn't exist")
        else:
            method2 = AvailableRoomDAO()
            ra_id = method2.create_unavailable_room_time(st_dt, et_dt, room_id)
            result = self.build_unavailable_room_attr_dict(ra_id, st_dt, et_dt, room_id)
            return jsonify(result)


    def delete_unavailable_schedule(self, r_id, st_dt, et_dt):
        method = AvailableRoomDAO()
        result = method.delete_unavailable_room_schedule(r_id, st_dt, et_dt)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")