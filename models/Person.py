import psycopg2
from config.dbcondig import db_root_config
from models.Room import RoomDAO as Room


class PersonDAO(object):
    R_STUDENT = 1
    R_PROF = 2
    R_STAFF = 3
    R_INSTRUCTOR = 4
    R_VISITOR = 5

    MALE = 1
    FEMALE = 2
    NON_BINARY = 3

    genders = {
        MALE: "male",
        FEMALE: "female",
        NON_BINARY: "non_binary"
    }

    roles = {
        R_STUDENT: "student",
        R_PROF: "professor",
        R_STAFF: "staff",
        R_INSTRUCTOR: "instructor",
        R_VISITOR: "visitor"
    }

    access = {
        R_STUDENT: (Room.T_STY_SPACE, Room.T_LAB),
        R_PROF: (Room.T_LAB, Room.T_CLASSROOM, Room.T_OFFICE, Room.T_STY_SPACE),
        R_STAFF: (Room.T_LAB, Room.T_CLASSROOM, Room.T_CONFERENCE, Room.T_OFFICE, Room.T_STY_SPACE),
        R_INSTRUCTOR: (Room.T_LAB, Room.T_OFFICE, Room.T_STY_SPACE),
        R_VISITOR: (Room.T_STY_SPACE)
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

    # --- Helper Methods --- #

    def check_if_person_exists(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select exists(select 1 from person where p_id = %s);'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def count_person(self):
        cursor = self.conn.cursor()
        query = 'select count(*) as "count" from person;'
        cursor.execute(query,)
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def count_person_by_role(self, r_id):
        cursor = self.conn.cursor()
        query = 'select count(*) as count ' \
                'from "person" where p_role= %s;'
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    # --- Normal CRUD Methods --- #

    def get_all_person_by_role(self, p_role: int) -> list:
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname ' \
                'from "person" where p_role= %s;'
        cursor.execute(query, (p_role,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def create_new_person(self,
                          p_fname: str,
                          p_lname: str,
                          p_role: int,
                          p_email: str,
                          p_phone: str,
                          p_gender: str,
                          p_password: str
                          ):
        cursor = self.conn.cursor()
        query = 'insert into "person" (p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_password) ' \
                'values (%s, %s, %s, %s, %s, %s, %s) ' \
                'returning p_id;'
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_password,))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return p_id

    def update_person(self, p_id, p_fname, p_lname, p_phone, p_gender):
        cursor = self.conn.cursor()
        query = 'update "person" ' \
                'set p_fname = %s, p_lname = %s, p_phone = %s ,p_gender= %s ' \
                'where p_id = %s '
        cursor.execute(query, (p_fname, p_lname, p_phone, p_gender, p_id))
        self.conn.commit()
        return True

    def delete_person(self, p_id):
        cursor = self.conn.cursor()
        query = 'delete from person ' \
                'where p_id = %s;'
        cursor.execute(query, (p_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return deleted_rows != 0

    def get_all_person(self, limit: int) -> list:
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname from person limit %s;'
        cursor.execute(query, (limit,))
        result: list = []
        while True:
            rows = cursor.fetchmany(125)
            if not rows:
                break
            for row in rows:
                result.append(row)
        cursor.close()
        return result

    def get_person_by_id(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_fname, p_lname, p_role, p_email, p_phone, p_gender ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_person_by_name(self, p_fname: str, p_lname: str):
        cursor = self.conn.cursor()
        query = 'select p_id, p_role, p_email, p_phone, p_gender ' \
                'from "person" where p_fname = %s and p_lname = %s;'
        cursor.execute(query, (p_fname, p_lname,))
        result = cursor.fetchone()
        return result

    def get_info_according_to_role(self, r_id: int):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in %s'
        cursor.execute(query, (self.access[r_id],))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Retrieves the host id, and full name and the times this host has invited the given invitee's id
    def get_host_that_invited_this_person(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname , p_lname, count(b.invited_id) as shared from booking as b inner join person on ' \
                'person.p_id = b.host_id where b.invited_id = %s group by b.invited_id, p_id order by shared desc; '
        cursor.execute(query, (p_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # Retrieves the host id, and full name and the times this host has invited the given invitee's id
    def get_hosts_that_invited_this_person(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname , p_lname, count(b.invited_id) as shared ' \
                'from booking as b inner join person on ' \
                'person.p_id = b.host_id where b.invited_id = %s ' \
                'group by b.invited_id, p_id order by shared desc; '
        cursor.execute(query, (p_id,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # --- Statistics --- #

    # Retrieves the person that has been most invited and the amount of times
    def get_person_that_most_share_with_person(self, p_id: int):
        cursor = self.conn.cursor()
        query = "with bomeeting as " \
                "(select booking.b_id, " \
                "booking.st_dt, " \
                "booking.et_dt, " \
                "booking.invited_id, " \
                "booking.host_id, " \
                "booking.room_id, " \
                "subt.meeting " \
                "from booking inner join " \
                "(select b.host_id,b.st_dt,b.et_dt, row_number() over (order by st_dt) as meeting " \
                "from booking as b " \
                "group by  (b.host_id,b.st_dt,b.et_dt)) as subt " \
                "on subt.host_id=booking.host_id and subt.st_dt=booking.st_dt and subt.et_dt=booking.et_dt) " \
                "select  bomeeting.invited_id " \
                "from bomeeting " \
                "where bomeeting.meeting in " \
                "(select bomeeting.meeting from bomeeting where bomeeting.invited_id = %s) " \
                "group by bomeeting.invited_id order by count(bomeeting.invited_id) desc limit 1 offset 1;"
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()[0]
        cursor.close()
        return result

    def get_most_used_room_by_person(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select room_id, r_name, count(invited_id)' \
                'from booking natural inner join' \
                '(select r_id, r_name from room)' \
                'as roomy where invited_id = %s ' \
                'group by room_id, r_name ' \
                'order by count(invited_id) desc limit 1;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    # Retrieves the person who performed the most amount of bookings
    def get_person_who_booked_most(self, limit_thingy: int):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname, count(booking.host_id) as bookings ' \
                'from booking inner join person on person.p_id = booking.host_id ' \
                'GROUP BY p_id  order by bookings desc limit %s; '
        cursor.execute(query, (limit_thingy,))
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # --- Accounts --- #

    def get_account_info(self, p_email: str, p_password: str):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname ' \
                'from person where p_email = %s and p_password = %s;'
        cursor.execute(query, (p_email, p_password,))
        result = cursor.fetchone()
        cursor.close()
        return result
