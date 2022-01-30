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

    def __del__(self):
        self.conn.close()

    # creates a new booking entry, no checks here btw
    def create_new_booking(self, b_name: str, st_dt, et_dt, invited_id: int, host_id: int, room_id: int):
        cursor = self.conn.cursor()
        query = 'insert into "booking" (b_name, st_dt, et_dt, invited_id, host_id, room_id) ' \
                'values (%s,%s,%s,%s,%s,%s) returning b_id; '
        cursor.execute(query, (b_name, st_dt, et_dt, invited_id, host_id, room_id,))
        b_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return b_id

    def get_meetings_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'with bomeeting as ' \
                '(select booking.b_id, booking.b_name, booking.st_dt,booking.et_dt,booking.invited_id,booking.host_id,booking. room_id, subt.meeting ' \
                'from booking inner join ' \
                '(select b.host_id,b.st_dt,b.et_dt, row_number() over (order by st_dt) as meeting ' \
                'from booking as b group by  (b.host_id,b.st_dt,b.et_dt)) as subt on subt.host_id=booking.host_id ' \
                'and subt.st_dt=booking.st_dt and subt.et_dt=booking.et_dt) ' \
                'select bomeeting.b_id, bomeeting.b_name, bomeeting.st_dt,bomeeting.et_dt,bomeeting.invited_id,bomeeting.host_id,bomeeting.room_id ' \
                'from bomeeting where bomeeting.meeting = (select bomeeting.meeting from bomeeting where b_id= %s); '
        cursor.execute(query, (b_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Updates existing entry
    def update_booking(self, b_id, b_name, st_dt, et_dt, invited_id, host_id, room_id):
        cursor = self.conn.cursor()
        query = 'update "booking" ' \
                'set b_name = %s, st_dt = %s, et_dt= %s, invited_id = %s, host_id= %s , room_id = %s ' \
                'where b_id = %s '
        cursor.execute(query, (b_name, st_dt, et_dt, invited_id, host_id, room_id, b_id))
        self.conn.commit()
        cursor.close()
        return True

    # deletes an entry
    def delete_booking(self, b_id):
        cursor = self.conn.cursor()
        query = 'delete from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return deleted_rows != 0

    # returns the whole booking query
    def get_all_booking(self, limit_thingy: int):
        cursor = self.conn.cursor()
        query = 'select b_id, b_name, st_dt, et_dt, invited_id, host_id, room_id from "booking" limit %s;'
        cursor.execute(query, (limit_thingy,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # return a single column entry of the booking with given id
    def get_booking_by_id(self, b_id: int):
        cursor = self.conn.cursor()
        query = 'select b_name, st_dt, et_dt, invited_id, host_id, room_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_bookings_by_host(self,host_id):
        cursor = self.conn.cursor()
        query = 'select * from booking where host_id = %s;'
        cursor.execute(query,(host_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # returns a query of all hosts who have booked inside the given timeframe
    def get_host_at_dt(self, room_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select distinct host_id, p.p_fname, p.p_lname' \
                ' from booking natural inner join person p ' \
                'where booking.room_id = %s and ' \
                '(tsrange(booking.st_dt, booking.et_dt) && tsrange(timestamp %s, timestamp %s));'
        cursor.execute(query, (room_id, st_dt, et_dt,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # returns a query of all invitees whose booking is inside the given timeframe
    def get_invited_at_dt(self, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select invited_id, room_id from booking where  (tsrange(booking.st_dt, booking.et_dt) && tsrange(timestamp %s, timestamp %s));'
        cursor.execute(query, (st_dt, et_dt,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # returns all invitees found in all booking
    def get_invite_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'select invited_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_host_by_id(self, b_id):
        cursor = self.conn.cursor()
        query = 'select host_id ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_free_time_of_day(self, p_id, date):
        cursor = self.conn.cursor()
        query = "with allday as " \
                "(select booking.invited_id, booking.st_dt, booking.et_dt " \
                "from booking " \
                "where (tsrange(booking.st_dt, booking.et_dt) && tsrange(timestamp %s::date,timestamp %s::date  + interval '1 day - 1 second'))  " \
                "and (booking.invited_id in %s) " \
                "union " \
                "select availableperson.person_id, availableperson.st_dt, availableperson.et_dt " \
                "from availableperson " \
                "where (tsrange(st_dt, et_dt) && tsrange(timestamp %s::date, timestamp %s::date  + interval '1 day - 1 second')) and person_id in %s) " \
                "select gaps.free_start,gaps.free_end,gaps.delta_time " \
                "from (select  coalesce((lag(allday2.et_dt,1) " \
                "over (order by allday2.et_dt)), (allday2.st_dt::date::timestamp)) as free_start," \
                "allday2.st_dt as free_end, allday2.st_dt - (coalesce((lag(allday2.et_dt,1) over (order by allday2.et_dt)), (allday2.st_dt::date::timestamp))) as delta_time, " \
                "(allday2.st_dt - (coalesce((lag(allday2.et_dt,1) over (order by allday2.et_dt)), (allday2.st_dt::date::timestamp)))> interval '1 second') as ValidGap " \
                "from (select allday.invited_id, allday.st_dt, allday.et_dt " \
                "from allday " \
                "union select null as invited_id, allday.st_dt::date + interval '1 day - 1 second' as st_dt, " \
                "allday.st_dt::date + interval '1 day - 1 second' as et_dt from allday) as allday2) as gaps " \
                "where gaps.ValidGap=true ;"
        cursor.execute(query, (date, date, p_id, date, date, p_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # returns a single row who would be the most booked room
    def get_most_booked_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_dept, r_building, count(booking.room_id) as bookings ' \
                'from booking inner join room on room.r_id = booking.room_id ' \
                'GROUP BY r_id ,r_dept, r_building order by bookings desc limit 10; '
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Returns the timeframe of the most busiest hour around
    def get_busiest_hours(self):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, count(*) as activeinthehour' \
                ' from booking  ' \
                ' group by st_dt, et_dt ' \
                'order by activeinthehour desc limit 5;'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def check_if_booking_exists(self, b_id: int):
        cursor = self.conn.cursor()
        query = 'select exists(select 1 from booking where b_id = %s);'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def count_booking(self):
        cursor = self.conn.cursor()
        query = 'select count(*) as "count" ' \
                'from booking;'
        cursor.execute(query,)
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def get_all_meetings(self):
        cursor = self.conn.cursor()
        query = 'select et_dt, st_dt, b_name, host_id, room_id, count(host_id) as invitees ' \
                'from booking group by host_id, b_name, st_dt, et_dt, room_id;'
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def get_meetings_by_host(self, host_id):
        cursor = self.conn.cursor()
        query = 'select distinct on (b_name) b_id, b_name, st_dt, et_dt from booking where host_id = %s;'
        cursor.execute(query, (host_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result
