import psycopg2
from config.dbcondig import db_root_config


class PersonDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='localhost'" % (
            db_root_config['dbname'],
            db_root_config['user'],
            db_root_config['password'],
            db_root_config['dbport']
        )
        self.conn = psycopg2.connect(connection_url)


    def createNewPerson(self, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        cursor = self.conn.cursor()
        query = 'insert into "person" (p_fname, p_lname, p_role, p_email, p_phone,p_gender) values (%s,%s,%s,%s,%s,%s) returning p_id;'
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender,))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        return p_id

    def update_person(self, p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        cursor = self.conn.cursor()
        query = 'update "Person" ' \
                'set p_fname = %s, p_lname= %s, p_role = %s, p_email= %s , p_phone = %s ,p_gender= %s ' \
                'where p_id = %s '
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_id))
        self.conn.commit()
        return True

    def delete_person(self, p_id):
        cursor = self.conn.cursor()
        query = 'delete from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def getAllPerson(self):
        cursor = self.conn.cursor()
        query = 'select p_fname = %s, p_lname= %s, p_role = %s, p_email= %s , p_phone = %s ,p_gender= %s from "person";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPersonById(self, p_id):
        cursor = self.conn.cursor()
        query = 'select p_fname = %s, p_lname= %s, p_role = %s, p_email= %s , p_phone = %s ,p_gender= %s ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def getAllUnavailablePerson(self):
        cursor = self.conn.cursor()
        query = 'select room_id, st_dt, et_dt, host_id ' \
                'from "booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

