import psycopg2
from config.dbcondig import db_root_config


class RoomDAO:
    # CONSTANTS N STUFF
    T_LAB = 1
    T_CLASSROOM = 2
    T_CONFERENCE = 3
    T_OFFICE = 4
    T_STY_SPACE = 5

    rooms = {
        T_LAB: 'laboratory',
        T_CLASSROOM: 'classroom',
        T_OFFICE: 'office',
        T_STY_SPACE: 'study_space',
        T_CONFERENCE: 'conference_hall'
    }

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def __del__(self):
        self.conn.close()

        # Returns a query of all rooms
    def get_all_rooms(self, limit_thingy: int) -> list:
        cursor = self.conn.cursor()
        query = 'select r_id, r_name, r_type, r_building, r_dept ' \
                'from room limit %s;'
        cursor.execute(query, (limit_thingy,))
        result: list = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # NOT IN USE
    # GET Target Room using its id
    def get_room(self, r_id: int):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_building, r_dept, r_type from room where r_id = %s;"
        # Execute commands n close
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def get_room_by_id(self, r_id: int):
        # Open Cursor for operations
        cursor = self.conn.cursor()
        query = "select r_name, r_building, r_dept, r_type " \
                "from room where r_id = %s;"
        # Execute commands n close
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_room_by_name(self, r_name: str):
        cursor = self.conn.cursor()
        query = 'select r_id, r_building, r_dept, r_type ' \
                'from room where r_name = %s;'
        cursor.execute(query, (r_name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # Returns a query of all available rooms
    def find_available_rooms(self, st_dt, et_dt):
        cursor = self.conn.cursor()
        query = 'select * from room where room.r_id not in (select distinct r_id from room inner join (select ' \
                't.room_id,t.is_there_conflict from ( select room_id, st_dt, et_dt, tsrange(st_dt, et_dt) && tsrange(' \
                '%s, %s) as is_there_conflict from (select availableroom.room_id, availableroom.st_dt, ' \
                'availableroom.et_dt from availableroom UNION select booking.room_id, booking.st_dt, booking.et_dt ' \
                'from booking) as hisdedpisded) t where t.is_there_conflict=true) as test on room.r_id=test.room_id) ; '
        cursor.execute(query, (st_dt, et_dt))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # creates a new room entry
    def create_new_room(self, r_building, r_dept, r_type,r_name):
        cursor = self.conn.cursor()
        query = "insert into room (r_building, r_dept, r_type, r_name)  values (%s, %s, %s, %s) returning r_id; "
        cursor.execute(query, (r_building, r_dept, r_type,r_name,))
        r_id = cursor.fetchone()[0]
        self.conn.commit()
        return r_id

    # Updates an existing entry
    def update_room(self, r_id, new_room_name, new_r_building, new_r_dept, new_r_type):
        cursor = self.conn.cursor()
        query = "update room set r_name = %s, r_building = %s, r_dept = %s, r_type = %s where r_id = %s;"
        cursor.execute(query, (new_room_name, new_r_building, new_r_dept, new_r_type, r_id,))
        self.conn.commit()
        cursor.close()
        return True

    # Deletes an entry
    def delete_room(self, r_id):
        cursor = self.conn.cursor()
        query = 'delete from room ' \
                'where r_id = %s;'
        cursor.execute(query, (r_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    # Returns a query which is the most booked room
    def get_most_booked_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_name, count(booking.room_id) as timed_booked ' \
                'from booking inner join room on booking.room_id = room.r_id ' \
                'GROUP BY r_id order by timed_booked desc limit 10; '
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def check_if_room_exists(self, r_id: int):
        cursor = self.conn.cursor()
        query = 'select exists(select 1 from room where r_id = %s);'
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def count_rooms(self):
        cursor = self.conn.cursor()
        query = 'select count(*) as "count" ' \
                'from room;'
        cursor.execute(query, )
        result = cursor.fetchone()[0]
        cursor.close()
        return result
