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
    def get_all_rooms(self):
        cursor = self.conn.cursor()
        query = 'select r_id, r_building, r_type r_dept "Room";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Create
    def create_new_room(self, r_type):
        cursor = self.conn.cursor()
        query = 'insert into "Room" (r_name, r_name) values (%s, %s) returning room_id;'

        cursor.execute(query, (r_type,))
        room_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_id

    # Update
    def update_room(self, r_id, new_r_name, new_r_type):
        cursor = self.conn.cursor()
        query = 'update "Room" set room_name = %s, room_type_id = %s where room_id = %s;'
        cursor.execute(query, (new_r_name, new_r_type, r_id,))
        self.conn.commit()
        return True

    # Delete
    def delete_room(self, r_id):
        cursor = self.conn.cursor()
        query = "deleting Room %s..."
        cursor.execute(query, (r_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows != 0
