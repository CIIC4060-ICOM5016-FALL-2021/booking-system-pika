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

    # creates new unavailable room entry
    def create_unavailable_room_time(self, r_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'insert into "availableroom" ' \
                '(st_dt, et_dt, room_id) values (%s, %s, %s) returning ra_id;'
        cursor.execute(query, (st_dt, et_dt, r_id,))
        pa_id = cursor.fetchone()[0]
        self.conn.commit()
        return pa_id

    # Returns the timeframe for a room (all day)
    def get_all_day_schedule(self, r_id, date):
        
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, \'unavailable\' as b_name, \'n/a\' as first_name, \'n/a\' as last_name ' \
                'from availableroom ar ' \
                'where ar.room_id = %s and ar.st_dt::date >= date %s and ar.et_dt::date <= date %s ' \
                'union select st_dt, et_dt, b_name, p_fname, p_lname ' \
                'from booking b natural inner join person p ' \
                'where host_id = p.p_id and b.room_id = %s and b.st_dt::date >= date %s and b.et_dt::date <= date %s;'
        cursor.execute(query, (r_id, date, date, r_id, date, date,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_all_schedule(self, r_id):
        cursor = self.conn.cursor()
        query = "select st_dt, et_dt from availableroom " \
                "where (availableroom.room_id = %s) " \
                "UNION select st_dt, et_dt " \
                "from booking where (booking.room_id = %s); "
        cursor.execute(query, (r_id, r_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # retrieves the unavailable room according to room id
    def get_unavailable_room_by_id(self, room_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, ra_id ' \
                'from availableroom ' \
                'where room_id = %s; '
        cursor.execute(query, (room_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_unavailable_room_by_ra_id(self, room_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt ' \
                'from availableroom ' \
                'where ra_id = %s; '
        cursor.execute(query, (room_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def verify_available_room_at_timeframe(self, r_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        # select host_id, st_dt, et_dt from booking where host_id =41 UNION select pa_id, st_dt, et_dt from availableperson where pa_id =41;
        query = "select exists(select booking.room_id, booking.st_dt, booking.et_dt " \
                "from booking " \
                "where (tsrange(booking.st_dt, booking.et_dt) && tsrange(%s, %s)) and booking.room_id=%s " \
                "union " \
                "select availableroom.room_id, availableroom.st_dt, availableroom.et_dt " \
                "from availableroom " \
                "where (tsrange(st_dt, et_dt) && tsrange(%s, %s)) and room_id=%s)  " \
                "as booleanresult;"
        cursor.execute(query, (st_dt, et_dt,r_id,st_dt, et_dt,r_id,))
        result = cursor.fetchone()
        return result

    def verify_conflict_at_timeframe(self, r_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select room_id, is_there_conflict, st_dt, et_dt from ( select room_id, st_dt, et_dt, tsrange(st_dt, ' \
                'et_dt) && tsrange(timestamp %s,timestamp %s) as is_there_conflict from (select room_id, st_dt, et_dt from availableroom ' \
                'where room_id = %s UNION select room_id, st_dt, et_dt from booking where room_id = %s) as ' \
                'hisdedpisded) t; '
        cursor.execute(query, (st_dt, et_dt, r_id, r_id))
        result = []
        for row in cursor:
            result.append(row)
        return result



    def get_all_unavailable_room(self):
        cursor = self.conn.cursor()
        query = 'select ra_id, st_dt, et_dt, room_id ' \
                'from "availableroom";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def delete_all_unavailable_room_by_ra_id(self, ra_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableroom" where ra_id = %s;'
        cursor.execute(query, (ra_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def delete_all_unavailable_room_by_room_id(self, r_id):
        cursor = self.conn.cursor()
        query = 'delete from "availableroom" where room_id = %s;'
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


    def get_all_day_schedule_by_role(self, p_role, date):

        cursor = self.conn.cursor()
        query = 'select distinct r_id, r_name, p.p_id from room ' \
                'inner join booking b on room.r_id = b.room_id ' \
                'inner join person p on p.p_id = b.host_id ' \
                'where p.p_role = %s ' \
                'and (b.st_dt::date <= date %s AND b.et_dt::date >= date %s);'
        cursor.execute(query, (p_role, date, date,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_rooms_by_role_timeframe(self, p_role, st_dt, et_dt,list_type):

        cursor = self.conn.cursor()
        query = 'select r_id, r_name from room ' \
                'where r_id not in ' \
                '(select distinct r_id ' \
                'from room ' \
                'inner join booking b on room.r_id = b.room_id ' \
                'inner join person p on p.p_id = b.host_id ' \
                'where p.p_role = %s and (tsrange(b.st_dt, b.et_dt) &&  ' \
                'tsrange(timestamp %s, timestamp %s)) and room.r_type in %s ' \
                'UNION select distinct r_id ' \
                'from room inner join availableroom b on room.r_id = b.room_id ' \
                'where  (tsrange(b.st_dt, b.et_dt) &&  tsrange(timestamp %s, timestamp %s)))' \
                'and room.r_type in %s;'
        cursor.execute(query, (p_role, st_dt, et_dt,list_type,st_dt, et_dt,list_type,))
        result = []
        for row in cursor:
            result.append(row)
        return result
