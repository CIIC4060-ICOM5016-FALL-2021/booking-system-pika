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

    def create_new_user(self, p_email, p_phone, p_gender, p_name):
        return

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
        query = 'delete from "Person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0
