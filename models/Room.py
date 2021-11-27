import psycopg2
from config.dbcondig import db_root_config


class RoomDAO:
    # CONSTANTS N STUFF
    T_LAB = 1
    T_CLASSROOM = 2
    T_CONFERENCE = 3
    T_OFFICE = 4
    T_STY_SPACE = 5

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Read

    # Returns a query of all rooms
    def get_all_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_building, r_type, r_dept ' \
                'from room;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # GET Target Room using its id
    def get_room(self, r_id: int):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_building, r_dept, r_type from room where r_id = %s;"
        # Execute commands n close
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    # Gets room by building, department, or type
    def get_room_by(self, args: dict):
        parser = ""
        for i, j in reversed(list(enumerate(args.items()))):
            if i == 0:
                parser += str(j[0]) + " = " + str(j[1])
            else:
                parser += str(j[0]) + " = " + str(j[1]) + " and "
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_id, r_building, r_dept, r_type from room where " + parser + ";"
        print(query)
        # Execute commands n close
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_room_by_type(self, r_type):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_building, r_dept, %s from room;"
        # Execute commands n close
        cursor.execute(query, r_type)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # creates a new room entry
    def create_new_room(self, r_building, r_dept, r_type):
        cursor = self.conn.cursor()
        query = "insert into room (r_building, r_dept, r_type)  values (%s, %s, %s) returning r_id; "
        cursor.execute(query, (r_building, r_dept, r_type,))
        r_id = cursor.fetchone()[0]
        print(r_id)
        self.conn.commit()
        return r_id

    # Updates an existing entry
    def update_room(self, r_id, new_r_building, new_r_dept, new_r_type):
        cursor = self.conn.cursor()
        query = "update room set r_building = %s, r_dept = %s, r_type = %s where r_id = %s;"
        cursor.execute(query, (new_r_building, new_r_dept, new_r_type, r_id,))
        self.conn.commit()
        return True

    # Deletes an entry
    def delete_room(self, r_id):
        cursor = self.conn.cursor()
        query = "deleting room %s..."
        cursor.execute(query, (r_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

    # TODO FIX
    def create_unavailable_room_time(self, r_id, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'insert into "availableroom" ' \
                '(st_dt, et_dt, ra_id) values (%s, %s, %s);'
        cursor.execute(query, (st_dt, et_dt, r_id,))
        self.conn.commit()
        return True

    # Returns a single row which is the most booked room
    def get_most_booked_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, count(booking.room_id) as timed_booked ' \
                'from booking inner join room on booking.room_id = room.r_id ' \
                'GROUP BY r_id order by timed_booked desc limit 10; '
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #TODO Fix
    def get_all_day_schedule_of_room(self):
        cursor = self.conn.cursor()
        # TODO Test this
        query = "select r_id from room;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Checks if the room is available at a given timeframe
    def get_available_room(self, st_dt, et_dt):
        cursor = self.conn.cursor()
        # TODO Test this
        query = "select r_id " \
                "from room as r, booking as b, availableroom as a " \
                "where b.st_dt != %s and b.et_dt !=%s and r.r_id != b.room_id and a.room_id != r.r_id;"
        cursor.execute(query, (st_dt, et_dt, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_all_available_rooms(self):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, room_id ' \
                'from "availableroom";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result