import datetime as dt
from flask import jsonify
from models.Person import PersonDAO
from controller.Person import Person
from controller.Room import Room
from models.Room import RoomDAO
from models.Availableperson import AvailablePersonDAO


class AvailablePerson:
    def build_available_time_person_map(self, row):
        result = {'pa_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'person_id': row[3]}
        return result

    def build_unavailable_time_person_info(self, row):
        result = {'st_dt': row[0],
                  'et_dt': row[1], 'person_id': row[2]}
        return result

    def build_unavailable_person_attr_dict(self, pa_id, st_dt, et_dt, p_id):
        result = {'pa_id': pa_id, 'st_dt': st_dt,
                  'et_dt': et_dt, 'person_id': p_id}
        return result

    def create_unavailable_time_schedule(self, json):
        method = Person()
        person_id = json['person_id']
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        exist = method.persons_by_id_exist(person_id)
        if not exist:
            return jsonify("Person doesn't exist")
        else:
            method2 = AvailablePersonDAO()
            pa_id = method2.create_unavailable_person_time(st_dt, et_dt, person_id)
            result = self.build_unavailable_person_attr_dict(pa_id, st_dt, et_dt, person_id)
            return jsonify(result)

    def verify_available_user_at_timeframe(self, p_id, st_dt, et_dt):
        method = AvailablePersonDAO()
        available_users_list = method.verify_available_user_at_timeframe(p_id, st_dt, et_dt)
        result_list = []
        for row in available_users_list:
            obj = self.build_available_time_person_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_all_unavailable_persons(self):
        method = AvailablePersonDAO()
        available_users_list = method.get_all_unavailable_person()
        if not available_users_list:
            return jsonify("Everyone is Available!!!!!!!")
        else:
            result_list = []
            for row in available_users_list:
                obj = self.build_available_time_person_map(row)
                result_list.append(obj)
        return jsonify(result_list)

    def get_unavailable_person_by_id(self, pa_id):
        method = AvailablePersonDAO()
        person = method.get_unavailable_person_by_id(pa_id)
        if not person:
            return jsonify("That person is available")
        else:
            result = self.build_unavailable_time_person_info(person)
        return jsonify(result)

    # def update_unavailable_schedule(self):
    def update_unavailable_schedule(self, pa_id, json):
        person_id = json['person_id']
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        method = AvailablePersonDAO()
        method2 = Person()
        exist = method2.persons_by_id_exist(person_id)
        updated_info = method.update_unavailable_person(pa_id, st_dt, et_dt, person_id)

        if updated_info and exist:
            result = self.build_unavailable_person_attr_dict(pa_id, st_dt, et_dt, person_id)
            return jsonify(result)
        else:
            return jsonify('Not found person')

    def delete_unavailable_schedule(self, pa_id):
        method = AvailablePersonDAO()
        result = method.delete_unavailable_person_schedule(pa_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
