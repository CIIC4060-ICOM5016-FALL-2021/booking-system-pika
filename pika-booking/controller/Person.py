from flask import jsonify
from models.Person import PersonDAO
class Person:
    def build_map_dict(self, row):
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'p_role': row[3],
                  'p_email': row[4],'p_phone': row[5],'p_gender': row[6]}
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

    def createnewperson(self,json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        method = PersonDAO()
        p_id = method.createnewperson(p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        result = self.build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        return jsonify(result)

    def getallpersons(self):
        method = PersonDAO()
        person_list = method.getallperson()
        result_list = []
        for row in person_list:
            obj = self.build_user_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getpersonsbyid(self, p_id):
        method = PersonDAO()
        person_tuple = method.getpersonbyid(p_id)
        if not person_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_user_map_dict(person_tuple)
            return jsonify(result), 200

    def getallavailablepersons(self):
        method = PersonDAO()
        available_users_list = method.getallavailableperson()
        result_list = []
        for row in available_users_list:
            obj = self.build_available_time_user_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def updateperson(self, json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        p_id = json['p_id']
        method =PersonDAO()
        updatedinfo = method.updateperson(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        if updatedinfo:
         result = self.build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
         return jsonify(result)
        else:
             return jsonify('Not found person')

    def deleteperson(self, p_id):
        method = PersonDAO()
        result = method.deleteperson(p_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404


