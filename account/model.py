import psycopg2
from config.dbcondig import db_root_config
from models.Person import PersonDAO


class AccountDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_new_account(self, a_email: str, a_password: str):
        cursor = self.conn.cursor()
        query = "insert into account (a_email, a_password)  values (%s, %s) returning a_id; "
        cursor.execute(query, (a_email, a_password,))
        a_id = cursor.fetchone()[0]
        self.conn.commit()
        return a_id

    def delete_account(self, a_id):
        cursor = self.conn.cursor()
        query = 'delete from account ' \
                'where a_id = %s;'
        cursor.execute(query, (a_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_account_by_email(self, a_email):
        cursor = self.conn.cursor()
        query = 'delete from account ' \
                'where a_email = %s;'
        cursor.execute(query, (a_email,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def get_account_by_email(self, a_email):
        cursor = self.conn.cursor()

        query_1 = "select a_id, a_email, a_password from account where a_email = %s;"
        query_2 = "select p_fname, p_role from person where p_email = %s;"
        res = {}

        # Execute commands n close
        cursor.execute(query_1, (a_email,))
        for i, j, in cursor.fetchone():
            res[i] = j

        cursor.execute(query_2, (a_email,))
        for i, j, in cursor.fetchone():
            res[i] = j
        return res
