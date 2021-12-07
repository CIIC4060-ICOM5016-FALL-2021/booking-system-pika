import datetime as dt
from flask import jsonify


from models.Person import PersonDAO
from controller.Room import Room
from models.Room import RoomDAO
from models.AvailablePerson import AvailablePersonDAO


class Person:

    def build_person_map(self, row):
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'p_role': row[3], 'p_email': row[4],
                  'p_phone': row[5], 'p_gender': row[6]}
        return result

    def build_person_map_info(self, row):
        result = {'p_fname': row[0], 'p_lname': row[1], 'p_role': row[2],
                  'p_email': row[3], 'p_phone': row[4], 'p_gender': row[5]}
        return result

    def build_person_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        result = {'p_id': p_id, 'p_fname': p_fname, 'p_lname': p_lname, 'p_role': p_role, 'p_email': p_email,
                  'p_phone': p_phone, 'p_gender': p_gender}
        return result

    def build_person_update_attr_dict(self, p_fname, p_lname, p_email, p_phone, p_gender):
        result = {'p_fname': p_fname, 'p_lname': p_lname, 'p_email': p_email,
                  'p_phone': p_phone, 'p_gender': p_gender}
        return result

    def build_role_map_dict(self, row):
        result = {'p_role': row}
        return result

    def build_available_time_person_map(self, row):
        result = {'pa_id': row[0], 'st_dt': row[1],
                  'et_dt': row[2], 'person_id': row[3]}
        return result
    def build_mostusedroom_attrdict(self,row):
        result = {'start_time': row[0], 'finish_time': row[1], 'activebooking': row[2]}
        return result

    def build_mostbookedperson_attrdict(self,row):
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'count': row[3]}
        return result
    def build_mostsharedperson_attrdict(self,row):
        result = {'p_id': row[0]}
        return result
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
            obj = self.build_person_map(row)
            result_list.append(obj)
        return jsonify(result_list)

    def get_persons_by_id(self, p_id):
        method = PersonDAO()
        person_tuple = method.get_person_by_id(p_id)
        if not person_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_person_map_info(person_tuple)
            return jsonify(result), 200

    def persons_by_id_exist(self, p_id):
        method = PersonDAO()
        person_tuple = method.get_person_by_id(p_id)
        if not person_tuple:
            return False
        else:
            return True

    def get_person_role_by_id(self, p_id):
        dao = PersonDAO()
        person_role = dao.get_person_role_by_id(p_id)
        if not person_role:
            return jsonify("Person Not Found"), 404
        else:
            result = self.build_role_map_dict(person_role)
            print(result)
            return result

    def get_most_booked_persons(self):
        method = PersonDAO()
        bookedperson_tuple = method.get_most_booked_persons()
        if not bookedperson_tuple:
            return jsonify("Not Found"), 404
        else:
            result_list = []
            for row in bookedperson_tuple:
                obj = self.build_mostbookedperson_attrdict(row)
                result_list.append(obj)
            return jsonify(result_list)

    def get_most_used_room(self, p_id):
        method = PersonDAO()
        most_used = method.get_most_used_room(p_id, )
        method2 = RoomDAO()
        if not most_used:
            return jsonify("Not Found"), 404
        else:
            room = Room()
            most_used_room = method2.get_room(most_used[0])
            result = room.build_room_attr_dict(most_used[0], most_used_room[0], most_used_room[1],
                                               most_used_room[2])
            return jsonify(result), 200

    def get_person_that_most_share_with_person(self, json):
        method = PersonDAO()
        p_id = json['p_id']
        mostshared = method.get_person_that_most_share_with_person(p_id)
        if not mostshared:
            return jsonify("you don't share class with anyone")

        result = self.build_mostsharedperson_attrdict(mostshared)
        return jsonify(result)

    def update_person(self, json):
        p_id = json['p_id']
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        method = PersonDAO()
        exist = self.persons_by_id_exist(p_id)
        updated_info = method.update_person(p_id, p_fname, p_lname, p_email, p_phone, p_gender)
        if updated_info and exist:
            result = self.build_person_update_attr_dict(p_fname, p_lname, p_email, p_phone, p_gender)
            return jsonify(result)
        else:
            return jsonify('Not found person')

    def delete_person(self, p_id):
        method = PersonDAO()
        result = method.delete_person(p_id)
        if result:
            method2 = AvailablePersonDAO()
            method2.delete_unavailable_person_schedule(p_id)
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404

    def role_to_get_access_to_room_info(self, p_id):
        method = PersonDAO()
        role = method.get_person_role_by_id(p_id)

        if role == "0":
            result = method.get_info_for_student()
            return jsonify(result)
        elif role == "1":
            result = method.get_info_for_professor()
            return jsonify(result)
        elif role == "2":
            result = method.get_info_for_staff()
            return jsonify(result)
