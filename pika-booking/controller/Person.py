from flask import jsonify
from models.Person import BasePerson
class Person:
    def build_map_dict(self, row):
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'p_role': row[3],
                  'p_email': row[4],'p_phone': row[5] ,'p_gender': row[6]}
        return result

    def build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        result = {}
        result['p_id'] = p_id
        result['p_fname'] = p_fname
        result['p_lname'] = p_lname
        result['p_role'] = p_role
        result['p_email'] = p_email
        result['p_phone'] = p_phone
        result['p_gender'] = p_gender
        return result

    def createNewPerson(self,json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']

        cursor = self.conn.cursor()
        query = 'insert into "Person" (p_fname, p_lname, p_role, p_email, p_phone,p_gender) values (%s,%s,%s,%s,%s,%s) returning p_id;'
        cursor.execute(query, (p_fname, p_lname, p_role,p_email, p_phone,p_gender,))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        result = self.build_user_attr_dict(self, p_id, p_fname, p_lname, p_role , p_email,p_phone, p_gender)
        return jsonify(result)

    def updatePerson(self, json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']
        p_id = json['p_id']
        method =BasePerson()
        updatedinfo = method.updatePerson(self,p_id,p_fname, p_lname, p_role, p_email, p_phone, p_gender)
        if updatedinfo:
         result = self.build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)

         return jsonify(result)
        else:
            return jsonify('Not found person')

    def deletePerson(self, p_id):
        method = BasePerson()
        result = method.deletePerson(p_id)
        if  result:
           return jsonify("DELETED"), 200
         else:
             return jsonify("NOT FOUND"), 404

    def get_all_persons(self):
        return "All Persons are returned"
