from flask import jsonify
import datetime as dt
from controller.Room import Room

class AvailableRoom:

    def build_unavailable_time_room_map_dict(self, row):
        result = {'unavailable_time_room_id': row[0], 'unavailable_time_room_start': row[1],
                  'unavailable_time_room_finish': row[2], 'room_id': row[3]}
        return result


    def add_unavailable_time_schedule(self, r_id, json):
        method = Room()
        start_time = json['st_dt']
        end_time = json['et_dt']
        exist = method.get_room_by_id(r_id)
        if not exist:
            return jsonify("Person doesn't exist")

        unavailable_schedule = method.createUnavailablePersonTime(p_id, start_time, end_time)
        if unavailable_schedule:
            result = {}
            return jsonify(result)

    def verify_available_user_at_timeframe(self, p_id, st_dt, et_dt):
        method = AvailablePersonDao()
        available_users_list = method.verify_available_user_at_timeframe(p_id, st_dt, et_dt)
        result_list = []
        for row in available_users_list:
            obj = self.build_available_time_person_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_all_unavailable_persons(self):
        method = PersonDAO()
        available_users_list = method.get_all_available_person()
        result_list = []
        for row in available_users_list:
            obj = self.build_available_time_person_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    def delete_unavailable_schedule(self, p_id, st_dt, et_dt):
        method = AvailablePersonDao()
        result = method.delete_unavailable_person_schedule(p_id, st_dt, et_dt)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")