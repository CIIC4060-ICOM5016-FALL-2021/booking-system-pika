import datetime as dt
from flask import jsonify
from models.Person import PersonDAO
from controller.Person import Person
from controller.Room import Room
from models.Room import RoomDAO
from models.Availableperson import AvailablePersonDao


class AvailablePerson:
    def build_available_time_person_map(self, row):
        result = {'pa_id': row[0], 'st_dt': row[1],
                  'et_dt': row[2], 'person_id': row[3]}
        return result

    def build_unavailable_person_attr_dict(self, pa_id, st_dt, et_dt, p_id):
        result = {'pa_id': pa_id, 'st_dt': st_dt,
                  'et_dt': et_dt, 'person_id': p_id}
        return result

    def create_unavailable_time_schedule(self, json):
        method = Person()
        p_id = json['p_id']
        start_time = json['st_dt']
        end_time = json['et_dt']
        exist = method.get_persons_by_id(p_id)
        if not exist:
            return jsonify("Person doesn't exist")
        else:
            method2 = AvailablePersonDao()
            pa_id = method2.create_unavailable_time_schedule(p_id, start_time, end_time)
            result = self.build_unavailable_person_attr_dict( pa_id, start_time, end_time, p_id)
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
        method = AvailablePersonDao()
        available_users_list = method.get_all_unavailable_person()
        if not available_users_list:
            return jsonify("Everyone is Available!!!!!!!")
        else:
         result_list = []
         for row in available_users_list:
            obj = self.build_available_time_person_map(row)
            result_list.append(obj)
        return jsonify(result_list)
    # def update_unavailable_schedule(self):

    def delete_unavailable_schedule(self, p_id, st_dt, et_dt):
        method = AvailablePersonDao()
        result = method.delete_unavailable_person_schedule(p_id, st_dt, et_dt)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
