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
