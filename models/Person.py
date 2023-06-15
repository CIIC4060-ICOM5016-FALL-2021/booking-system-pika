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

    roledict = {
        1: R_STUDENT,
        2: R_PROF,
        3: R_STAFF,
        4: R_INSTRUCTOR,
        5: R_VISITOR

    }

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

    def create_new_person(self, p_fname, p_lname, p_role, p_email, p_phone, p_gender,p_password):
        cursor = self.conn.cursor()
        query = 'insert into "person" (p_fname, p_lname, p_role, p_email, p_phone,p_gender,p_password) values (%s,%s,%s,%s,%s,' \
                '%s,%s) returning p_id; '
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender,p_password,))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        return p_id


    def update_person(self, p_id, p_fname, p_lname, p_email, p_phone, p_gender,p_password):
        cursor = self.conn.cursor()
        query = 'update "person" ' \
                'set p_fname = %s, p_lname= %s, p_email= %s , p_phone = %s ,p_gender= %s,p_password = %s ' \
                'where p_id = %s '
        cursor.execute(query, (p_fname, p_lname, p_email, p_phone, p_gender, p_password, p_id))
        self.conn.commit()
        return True

    def get_account_by_email_and_password(self, p_email,p_password):
        cursor = self.conn.cursor()

        query = "select p_email, p_password, p_id, p_role from person where p_email = %s and p_password=%s;"
        # Execute commands n close
        cursor.execute(query, (p_email, p_password,))
        result = cursor.fetchone()
        return result

    # def get_person_id_by_email(self,p_email):
    #     cursor = self.conn.cursor()
    #     query = 'select p_id from person where p_email in %s; '
    #     cursor.execute(query,(p_email,))
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result
    def get_person_id_by_email(self,p_email):
        cursor = self.conn.cursor()
        query = 'select p_id from person where p_email = %s; '
        cursor.execute(query,(p_email,))

        result = cursor.fetchone()
        return result




    def get_account_by_email(self, p_email):
        cursor = self.conn.cursor()

        query = "select p_id,p_fname,p_role, p_email from person where p_email = %s;"

        # Execute commands n close
        cursor.execute(query, (p_email,))
        result = cursor.fetchone()
        return result


    def delete_person(self, p_id):
        cursor = self.conn.cursor()
        query = 'delete from person ' \
                'where p_id = %s;'
        cursor.execute(query, (p_id,))
        deleted_rows = cursor.rowcount
        self.conn.commit()
        return deleted_rows != 0

    def get_all_person(self):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname, p_role, p_email, p_phone ,p_gender,p_password ' \
                'from "person";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_person_by_id(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_fname, p_lname, p_role, p_email, p_phone, p_gender,p_password ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def get_dict_person_by_id(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_fname, p_lname, p_role, p_email, p_phone, p_gender,p_password ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))

        columnsnames = ["p_fname", "p_lname", "p_role", "p_email", "p_phone", "p_gender","p_password"]
        result = cursor.fetchone()

        dictionary = {}
        for i in range(0, len(columnsnames)):
            dictionary[columnsnames[i]] = result[i]

        return dictionary

    def get_all_available_person(self):
        cursor = self.conn.cursor()
        query = 'select  st_dt, et_dt, person_id ' \
                'from "availableperson";'
        cursor.execute(query)
        result = []
        # ok
        for row in cursor:
            result.append(row)
        return result

    def get_person_role_by_id(self, p_id):
        cursor = self.conn.cursor()
        query = 'select p_role ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        print(cursor)
        result = cursor.fetchone()[0]
        print(result, "RESULT")
        return result

    # retrieves the people who booked most and the times this person has booked
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

    # Retrieves the most used room
    def get_most_logged_person(self):
        cursor = self.conn.cursor()
        query = 'select person.p_id, count(booking.invited_id) as logged ' \
                'from booking inner join person on person.p_id = booking.invited_id inner join person on ' \
                'booking.invited_id = person.p_id ' \
                'group by person.p_id' \
                ' order by logged desc limit 1; '
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

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
        result = cursor.fetchone()
        cursor.close()
        return result

    # Retrieves the host id, and full name and the times this host has invited the given invitee's id
    def get_host_that_invited_this_person(self, p_id):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname , p_lname, count(b.invited_id) as shared from booking as b inner join person on ' \
                'person.p_id = b.host_id where b.invited_id = %s group by b.invited_id, p_id order by shared desc; '
        cursor.execute(query, (p_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_most_used_room(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'with most_used_room as ' \
                '(select distinct room_id, invited_id as user_id ' \
                'from booking ' \
                'where invited_id = %s ' \
                'union select distinct room_id, host_id as user_id ' \
                'from booking where host_id = %s) ' \
                'select room_id, count(user_id) as times_used ' \
                'from most_used_room group by room_id order by times_used ' \
                'desc limit 1;'
        cursor.execute(query, (p_id, p_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_info_for_student(self):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in (5)'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result


    def get_rooms_for_role(self,role_id):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in %s'
        cursor.execute(query, (role_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result


    def get_info_for_instructor(self):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in (1,4,5)'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_info_for_professor(self):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in (1,2,4,5)'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result
    def get_info_for_visitor(self):
        cursor = self.conn.cursor()
        query = 'select * from room where r_type in (5)'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result


    def get_info_for_staff(self):
        cursor = self.conn.cursor()
        query = 'select * from room'
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_all_person_but(self, p_id):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_password ' \
                'from "person" where p_id != %s;'
        cursor.execute(query, (p_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_all_person_by_role(self, p_role):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_password ' \
                'from person where p_role= %s;'
        cursor.execute(query, (p_role,))
        result = []
        for row in cursor:
            result.append(row)
        return result

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
        cursor.execute(query, )
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