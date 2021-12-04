import psycopg2
from config.dbcondig import db_root_config


class AvailablePersonDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_unavailable_person_time(self, st_dt, et_dt, person_id):
        cursor = self.conn.cursor()
        query = 'insert into "availableperson" ' \
                '(st_dt, et_dt, person_id) values (%s, %s, %s) returning pa_id;'
        cursor.execute(query, (st_dt, et_dt, person_id,))
        pa_id = cursor.fetchone()[0]
        self.conn.commit()
        return pa_id

    def get_all_unavailable_person(self):
        cursor = self.conn.cursor()
        query = 'select  pa_id, st_dt, et_dt, person_id ' \
                'from "availableperson";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def get_unavailable_person_by_id(self, pa_id):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, person_id ' \
                'from "availableperson"' \
                'where pa_id = %s'
        cursor.execute(query, (pa_id,))
        result = cursor.fetchone()
        return result

    def get_unavailable_time_of_person_by_id_in_booking(self, p_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from "booking" ' \
                'where invited_id = %s ' \
                'or host_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def get_unavailable_time_of_person_by_id(self, pa_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from "availableperson" ' \
                'where pa_id = %s ;'
        cursor.execute(query, (pa_id,))
        result = cursor.fetchone()
        return result

    def get_unavailable_time_of_person_by_person_id(self, p_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from "availableperson" ' \
                'where person_id = %s ;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def verify_available_person_at_timeframe(self, p_id, st_dt, et_dt):
        # time.mktime(datetime.datetime.strptime(string2, "%Y-%m-%d %H:%M:%S").timetuple())
        cursor = self.conn.cursor()
        query = "select exists(select booking.invited_id, booking.host_id, booking.st_dt, booking.et_dt " \
                "from booking " \
                "where (tsrange(booking.st_dt, booking.et_dt) && tsrange(%s, %s)) and (booking.invited_id=%s or booking.host_id=%s)" \
                "union " \
                "select availableperson.person_id, availableperson.st_dt, availableperson.et_dt " \
                "from availableperson " \
                "where (tsrange(availableperson.st_dt, availableperson.et_dt) && tsrange(%s, %s)) and availableperson.person_id=%s)  " \
                "as booleanresult;"
        cursor.execute(query, (st_dt, et_dt, p_id, p_id,st_dt, et_dt, p_id,))
        result = cursor.fetchone()
        return result

    def verify_conflict_at_timeframe(self, p_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select person_id, is_there_conflict, st_dt, et_dt from ( select person_id, st_dt, et_dt, tsrange(st_dt, ' \
                'et_dt) && tsrange(%s, %s) as is_there_conflict from (select person_id, st_dt, et_dt from availableperson where ' \
                'person_id = %s UNION select invited_id as person_id, st_dt, et_dt from booking where invited_id = %s) as ' \
                'hisdedpisded ) t; '
        cursor.execute(query, (st_dt, et_dt, p_id, p_id))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def update_unavailable_person(self, pa_id, st_dt, et_dt, person_id):
        cursor = self.conn.cursor()
        query = 'update "availableperson" ' \
                'set st_dt= %s, et_dt= %s, person_id= %s ' \
                'where pa_id = %s '
        cursor.execute(query, (st_dt, et_dt, person_id, pa_id))
        self.conn.commit()
        return True

    def delete_all_unavailable_person_schedule(self, person_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableperson"' \
                ' where person_id = %s;'
        cursor.execute(query, (person_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_unavailable_person_schedule(self, pa_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableperson" ' \
                'where pa_id = %s; '
        cursor.execute(query, (pa_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_unavailable_person_schedule_at_certain_time(self, p_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'delete from "availableperson" ' \
                'where person_id = %s and st_dt= %s and et_dt= %s;'
        cursor.execute(query, (p_id, st_dt, et_dt))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    # Returns the timeframe for any person (all_day)
    def get_all_day_schedule(self, p_id, date):

        cursor = self.conn.cursor()
        query = "select st_dt, et_dt from availableperson " \
                "where (person_id = %s) " \
                "and (availableperson.st_dt::date <= date %s AND availableperson.et_dt::date >= date %s) " \
                "UNION select st_dt, et_dt " \
                "from booking where (host_id = %s or invited_id = %s) " \
                "and (booking.st_dt::date <= date %s AND booking.et_dt::date >= date %s) ;"
        cursor.execute(query, (p_id, date, date,p_id,p_id,date,date,))
        result = []
        for row in cursor:
            print(row, "ROW")
            result.append(row)
        return result
