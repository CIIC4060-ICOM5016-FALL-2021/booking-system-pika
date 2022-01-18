from flask import jsonify

from controller.AvailableRoom import schedule_stuff
from controller.Person import Person
from models.AvailablePerson import AvailablePersonDAO
from models.Person import PersonDAO


class AvailablePerson:
    def build_available_time_person_map(self, row):
        result = {'pa_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'person_id': row[3]}
        return result

    def build_unavailable_time_person_info(self, row):
        result = {'st_dt': row[0],
                  'et_dt': row[1],
                  'person_id': row[2]
                  }
        return result

    def build_unavailable_person_attr_dict(self, pa_id, st_dt, et_dt, p_id):
        result = {'pa_id': pa_id, 'st_dt': st_dt,
                  'et_dt': et_dt, 'person_id': p_id}
        return result

    ####################
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

    def verify_available_user_at_timeframe(self, p_id: int, st_dt, et_dt):

        method = AvailablePersonDAO()
        available_users_list = method.verify_available_person_at_timeframe(p_id, st_dt, et_dt)
        result = {"Unavailable": available_users_list[0]}

        return jsonify(result)

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

########
    def get_unavailable_person_by_id(self, pa_id):
        method = AvailablePersonDAO()
        person = method.get_unavailable_person_by_id(pa_id)
        if not person:
            return jsonify("That person is available")
        else:
            result = self.build_unavailable_time_person_info(person)
        return jsonify(result)

    def get_unavailable_person_by_person_id(self, pa_id):
        method = AvailablePersonDAO()

        person_dao = PersonDAO()
        existing_person = person_dao.get_person_by_id(pa_id)

        if not existing_person:
            return jsonify("That person is available")
        else:
            res = method.get_unavailable_person_by_person_id(pa_id)
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
########

    # def update_unavailable_schedule(self):
    def update_unavailable_schedule(self, json):
        pa_id = json['pa_id']
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

    def delete_unavailable_schedule(self, pa_id: int):
        method = AvailablePersonDAO()
        result = method.delete_unavailable_person_schedule(pa_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")

    # Deletes an entry where person is unavailable if given the exact timeframe
    def delete_unavailable_person_schedule_at_certain_time(self, json: dict):
        p_id = json["p_id"]
        st_dt = json["st_dt"]
        et_dt = json["et_dt"]

        dao = AvailablePersonDAO()
        person_dao = PersonDAO()

        existing_person = person_dao.get_person_by_id(p_id)

        if not existing_person:
            return jsonify("Room Not Found"), 404

        res = dao.delete_unavailable_person_schedule_at_certain_time(p_id, st_dt, et_dt)
        if res:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")

    # Returns the timeframe for a room (all day)
    def get_all_day_schedule(self, json: dict):
        person_id = json['p_id']
        date = json['date']

        dao = AvailablePersonDAO()
        person_dao = PersonDAO()

        existing_person = person_dao.get_person_by_id(person_id)

        if not existing_person:
            return jsonify("Room Not Found"), 404

        res = dao.get_all_day_schedule(person_id, date)
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
    def get_schedule(self,json):
        person_id = json['person_id']

        dao = AvailablePersonDAO()
        person_dao = PersonDAO()

        existing_room = person_dao.get_person_by_id(person_id)
        if not existing_room:
            return jsonify("Person Not Found"), 404
        else:
            res = dao.get_all_schedule(person_id)
            result = schedule_stuff(res)
            return jsonify(result), 200

    def delete_all_unavailable_person_schedule(self, json: dict):
        p_id = json["p_id"]

        dao = AvailablePersonDAO()
        person_dao = PersonDAO()

        if not person_dao.get_person_by_id(p_id):
            return jsonify("Room Not Found"), 404

        res = dao.delete_all_unavailable_person_schedule(p_id)
        if res:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
