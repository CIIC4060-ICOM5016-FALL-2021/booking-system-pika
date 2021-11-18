import psycopg2
from config.dbcondig import db_root_config


class AvailableRoomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_unavailable_room_time(self, st_dt, et_dt,r_id):
        cursor = self.conn.cursor()
        query = 'insert into "availableroom" ' \
                '(st_dt, et_dt, room_id) values (%s, %s, %s);'
        cursor.execute(query, (st_dt, et_dt, r_id,))
        self.conn.commit()
        return True

    def get_unavailable_time_of_room_by_id(self, r_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from "booking" ' \
                'where room_id = %s; '
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def verify_available_room_at_timeframe(self, r_id, st_dt, et_dt):
       cursor = self.conn.cursor()
       query = "select r_id " \
               "from room as r, booking as b, availableroom as a " \
               "where b.st_dt != %s and b.et_dt !=%s and r.r_id != b.invited_id and a.room_id != r.r_id;"
       cursor.execute(query, (r_id,st_dt, et_dt, ))
       result = cursor.fetchone()
       return result


    def get_all_unavailable_room(self):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, room_id ' \
                'from "availableroom";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def delete_unavailable_room(self, r_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableroom" where ra_id = %s;'
        cursor.execute(query, (r_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_unavailable_room_schedule(self, room_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'delete from "availableroom" where room_id = %s and st_dt = %s and et_dt= %s; '
        cursor.execute(query, (room_id, st_dt, et_dt))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0