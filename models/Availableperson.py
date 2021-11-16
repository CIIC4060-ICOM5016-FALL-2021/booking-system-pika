import psycopg2
from config.dbcondig import db_root_config
class AvailablePersonDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_unavailable_person_time(self, p_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'insert into "availableperson" ' \
                '(st_dt, et_dt, person_id) values (%s, %s, %s) returning pa_id;'
        cursor.execute(query, (st_dt, et_dt, p_id,))
        self.conn.commit()
        return True

    def get_all_unavailable_person(self):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, person_id ' \
                'from "availableperson";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def get_unavailable_time_of_person_by_id(self, p_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from "booking" ' \
                'where invited_id = %s ' \
                'or host_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def  verify_available_user_at_timeframe(self, p_id, st_dt, et_dt):
       cursor = self.conn.cursor()
       query = "select p_id " \
               "from person as p, booking as b, availableperson as a " \
               "where b.st_dt != %s and b.et_dt !=%s and p.p_id != b.invited_id and a.person_id != p.p_id; "
       cursor.execute(query, (p_id,st_dt, et_dt, ))
       result = cursor.fetchone()
       return result


    def get_all_unavailable_person(self):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, person_id ' \
                'from "availableperson";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def delete_unavailable_person(self, person_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableperson" where person_id = %s;'
        cursor.execute(query, (person_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_unavailable_person_schedule(self, p_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'delete from "availableperson" where person_id = %s AND st_dt= %s AND et_dt = %s; '
        cursor.execute(query, (p_id, st_dt, et_dt))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0