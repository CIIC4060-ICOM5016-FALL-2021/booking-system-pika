import psycopg2
from config.dbcondig import db_root_config


class RoomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    # Read

    # GET All
    def get_all_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_building, r_type, r_dept ' \
                'from room;'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # GET Target Room
    #
    # NOTE:
    # This looks by id
    #
    def get_room(self, r_id):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_id, r_building, r_dept, r_type from room where r_id =%s;"
        # Execute commands n close
        cursor.execute(query, (r_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Gets room by building, department, or type
    # TODO: Make this more general
    def get_room_by(self, r_building="", r_dept="", r_type=""):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select %s, %s, %s from room;"
        # Execute commands n close
        cursor.execute(query, (r_building, r_dept, r_type ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Create
    def create_new_room(self, r_building, r_dept, r_type):
        cursor = self.conn.cursor()
        query = "insert into room (r_building, r_dept, r_type)  values (%s, %s, %s) returning r_id; "
        cursor.execute(query, (r_building, r_dept, r_type,))
        r_id = cursor.fetchone()[0]
        print(r_id)
        self.conn.commit()
        return r_id

    # Update
    def update_room(self, r_id, new_r_building, new_r_dept, new_r_type):
        cursor = self.conn.cursor()
        query = "update room set r_building = %s, r_dept = %s, r_type = %s where r_id = %s;"
        cursor.execute(query, (new_r_building, new_r_dept, new_r_type, r_id,))
        self.conn.commit()
        return True

    # Delete
    def delete_room(self, r_id):
        cursor = self.conn.cursor()
        query = "deleting room %s..."
        cursor.execute(query, (r_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0

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

    def get_available_room(self, st_dt, et_dt):
        cursor = self.conn.cursor()
        # TODO Test this
        query = "select r_id " \
                "from room as r, booking as b, availableroom as a" \
                "where b.st_dt != %s and b.et_st !=%s and r.r_id != b.room_id and a.r_id != r.rid;"
        cursor.execute(query, (st_dt, et_dt, ))
        result = []
        for row in cursor:
            result.append(row)
        return result