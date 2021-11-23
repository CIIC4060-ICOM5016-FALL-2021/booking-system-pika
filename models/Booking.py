import psycopg2
from config.dbcondig import db_root_config


# Simple function to generate timestamps in python, sort of
def format_time_stamp(year, month, day, hour=0, minute=0, second=0, tz='-04'):
    if 0 <= hour < 10:
        hour = '0' + str(hour)
    if 0 <= minute < 10:
        minute = '0' + str(minute)
    if 0 <= second < 10:
        second = '0' + str(second)
    if 0 <= month < 10:
        month = '0' + str(month)
    if 0 <= day < 10:
        day = '0' + str(day)

    # Example timestamp string: '2016-06-22 19:10:25-04'
    # With leading zeroes just in case
    result = '' + str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(
        second) + tz
    return result


class BookingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # creates a new booking entry, no checks here btw
    def create_new_booking(self, st_dt, et_dt, invited_id, host_id, room_id):
        cursor = self.conn.cursor()
        query = 'insert into "booking" (st_dt, et_dt, invited_id, host_id, room_id) values (%s,%s,%s,%s,%s) returning ' \
                'b_id; '
        cursor.execute(query, (st_dt, et_dt, invited_id, host_id, room_id,))
        b_id = cursor.fetchone()[0]
        self.conn.commit()
        return b_id

    # Updates existing entry
    def update_booking(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        cursor = self.conn.cursor()
        query = 'update "booking" ' \
                'set st_dt = %s, et_dt= %s, invited_id = %s, host_id= %s , room_id = %s ' \
                'where b_id = %s '
        cursor.execute(query, (st_dt, et_dt, invited_id, host_id, room_id, b_id))
        self.conn.commit()
        return True

    # deletes an entry
    def delete_booking(self, b_id):
        cursor = self.conn.cursor()
        query = 'delete from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    # returns the whole booking query
    def get_all_booking(self):
        cursor = self.conn.cursor()
        query = 'select b_id, st_dt, et_dt, invited_id, host_id, room_id from "booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # return a single column entry of the booking with given id
    def get_booking_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, invited_id, host_id, room_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        return result

    # returns a query of all hosts who have booked inside the given timeframe
    def get_host_at_dt(self, st_dt, et_dt: int):
        cursor = self.conn.cursor()
        query = 'select host_id, room_id from booking where tsrange(st_dt, et_dt) && tsrange(%s, %s);'
        cursor.execute(query, (st_dt, et_dt,))
        result = cursor.fetchone()
        return result

    # returns a query of all invitees whose booking is inside the given timeframe
    def get_invited_at_dt(self, room_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select invited_id, room_id from booking where tsrange(st_dt, et_dt) && tsrange(%s, %s);'
        cursor.execute(query, (st_dt, et_dt,))
        result = cursor.fetchone()
        return result

    # returns all invitees found in all booking
    def get_invite_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'select invited_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        return result

    def get_host_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'select host_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        return result

    # returns a single row who would be the most booked room
    def get_most_booked_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id ,r_dept,r_building, count(booking.room_id) as bookings ' \
                'from booking inner join room on room.r_id = booking.room_id ' \
                'GROUP BY r_id ,r_dept,r_building order by bookings desc limit 10; '
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
