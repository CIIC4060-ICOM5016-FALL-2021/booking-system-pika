from flask import jsonify
from models.Person import PersonDAO


class Person:
    def build_user_map_dict(self, row):
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'p_role': row[3],
                  'p_email': row[4], 'p_phone': row[5], 'p_gender': row[6]}
        return result

    def build_person_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        result = {}
        result['p_id'] = p_id
        result['p_fname'] = p_fname
        result['p_lname'] = p_lname
        result['p_role'] = p_role
        result['p_email'] = p_email
        result['p_phone'] = p_phone
        result['p_gender'] = p_gender
        return result

    def build_role_map_dict(self, p_role):
        result = {'p_role': p_role}
        return result

    def build_available_time_user_map_dict(self, row):
        result = {'pa_id': row[0], 'st_dt': row[1],
                  'et_dt': row[2], 'person_id': row[3]}
        return result

    def build_time_slot_attr_dict(self, st_dt, et_dt):
        result = {'start_time': st_dt, 'finish_time': et_dt}
        return result

    # ok
    def create_new_person(self, json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        method = PersonDAO()
        p_id = method.create_new_person(p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        result = self.build_person_attr_dict(p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        return jsonify(result)

    def get_all_persons(self):
        method = PersonDAO()
        person_list = method.get_all_person()
        if not person_list:
            return jsonify("Nobody is on the list! It feels, lonely.."), 404
        else:
            result_list = []
        for row in person_list:
            obj = self.build_user_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_persons_by_id(self, p_id):
        method = PersonDAO()
        person_tuple = method.get_person_by_id(p_id)
        if not person_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_user_map_dict(person_tuple)
            return jsonify(result), 200

    def get_all_available_persons(self):
        method = PersonDAO()
        available_users_list = method.get_all_available_person()
        result_list = []
        for row in available_users_list:
            obj = self.build_available_time_person_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_user_role_by_id(self, user_id):

        dao = PersonDAO()
        user_role = dao.getpersonrolebyid(user_id)
        if not user_role:  # User Not Found
            return jsonify("Person Not Found"), 404
        else:
            result = self.build_role_map_dict(user_role[0])
            return jsonify(result), 200

    def get_most_booked_persons(self):
        method = PersonDAO()
        bookedperson_tuple = method.get_most_booked_persons()
        if not bookedperson_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_user_map_dict(bookedperson_tuple)
            return jsonify(result), 200

    # def get_all_day_schedule_of_person(self,p_id):
    #       method = PersonDAO()
    #       date = json['date']
    #       user = method.getUserById(p_id)
    #       user_unavailable_time_slots = method.getUnavailableTimeOfUserById(p_id)
    #       if not user:  # User Not Found
    #           return jsonify("User Not Found"), 404
    #
    #       result_list = []
    #       start_date = date + " 0:00"
    #       start_time = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    #       finish_date = date + " 23:59"
    #       finish_date = dt.datetime.strptime(finish_date, '%Y-%m-%d %H:%M')
    #       for row in user_unavailable_time_slots:
    #           if row[1] > start_time and row[2] < finish_date:
    #               finish_time = row[1]
    #               obj = self.build_time_slot_attr_dict(start_time, finish_time)
    #               result_list.append(obj)
    #               start_time = row[2]
    #       finish_time = finish_date
    #       result_list.append(self.build_time_slot_attr_dict(start_time, finish_time))
    #       print(result_list)
    #       if len(result_list) != 1:
    #           return jsonify("Person is available at the following time frames", result_list), 200
    #       else:
    #           return jsonify("Person is available all day"), 200

    def update_person(self, json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        p_id = json['p_id']
        method = PersonDAO()
        updated_info = method.update_person(p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        if updated_info:
            result = self.build_person_attr_dict(p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
            return jsonify(result)
        else:
            return jsonify('Not found person')

    def delete_person(self, p_id):
        method = PersonDAO()
        result = method.delete_person(p_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404