from flask import jsonify
from models.Person import PersonDAO


class Person:

    def build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        return self.build_person_dict(
            [p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender]
        )

    def build_person_dict(self, row: list) -> object:
        """
        Generates a dictionary of one Person, which can be parsed by the
        » parse_new_person method
        Bellow Appears an example of the input...
        pid: 0, p_fname: Steve, p_lname: Rogers, p_role: 0, p_email: s.rogers@upr.edu, p_phone: Null, p_gender: 0
        @param row:
        @return:
        @rtype: object
        """
        result = {'p_id': row[0], 'p_fname': row[1], 'p_lname': row[2], 'p_role': row[3],
                  'p_email': row[4], 'p_phone': row[5], 'p_gender': row[6]}
        return result

    def parse_new_person(self, json):
        p_fname = json['p_fname']
        p_lname = json['p_lname']
        p_role = json['p_role']
        p_email = json['p_email']
        p_phone = json['p_phone']
        p_gender = json['p_gender']

        dao = PersonDAO()
        person_row = dao.create_new_user()
        result = self.build_user_attr_dict()

        return jsonify(result)

    def get_all_persons(self):
        return "All Persons are returned"

"""
        cursor = self.conn.cursor()
        query = 'insert into "Person" (p_fname, p_lname, p_role, p_email, p_phone,p_gender) values (%s,%s,%s,%s,%s,' \
                '%s) returning p_id; '
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        result = self.build_user_attr_dict(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender)
"""
