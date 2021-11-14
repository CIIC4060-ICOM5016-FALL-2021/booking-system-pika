import psycopg2
from config.dbcondig import db_root_config


class BookingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='localhost'" % (
            db_root_config['dbname'],
            db_root_config['user'],
            db_root_config['password'],
            db_root_config['dbport']
        )
        self.conn = psycopg2.connect(connection_url)


    def createNewBooking(self, st_dt, et_dt, invited_id, host_id, room_id):
        cursor = self.conn.cursor()
        query = 'insert into "booking" (st_dt, et_dt, invited_id, host_id, room_id) values (%s,%s,%s,%s,%s) returning b_id;'
        cursor.execute(query, (st_dt, et_dt, invited_id, host_id, room_id,))
        b_id = cursor.fetchone()[0]
        self.conn.commit()
        return b_id

    def update_booking(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        cursor = self.conn.cursor()
        query = 'update "booking" ' \
                'set st_dt = %s, et_dt= %s, invited_id = %s, host_id= %s , room_id = %s ' \
                'where b_id = %s '
        cursor.execute(query, (st_dt, et_dt, invited_id, host_id, room_id, b_id))
        self.conn.commit()
        return True

    def delete_booking(self, b_id):
        cursor = self.conn.cursor()
        query = 'delete from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def getAllBookings(self):
        cursor = self.conn.cursor()
        query = 'select st_dt = %s, et_dt= %s, invited_id = %s, host_id= %s , room_id = %s from "booking";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBookingById(self, b_id):
        cursor = self.conn.cursor()
        query = 'select st_dt = %s, et_dt= %s, invited_id = %s, host_id= %s , room_id = %s ' \
                'from "booking" where b_id = %s;'
        cursor.execute(query, (b_id,))
        result = cursor.fetchone()
        return result

    # def getAllUnavailablePerson(self):
    #     cursor = self.conn.cursor()
    #     query = 'select room_id, st_dt, et_dt, invited_id ' \
    #             'from "booking";'
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result

