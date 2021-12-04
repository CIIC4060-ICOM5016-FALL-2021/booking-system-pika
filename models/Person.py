import psycopg2
from config.dbcondig import db_root_config


class PersonDAO:
    R_STUDENT = 1
    R_PROF = 2
    R_STAFF = 3
    R_INSTRUCTOR = 4
    R_VISITOR = 5

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (db_root_config['dbname'],
                                                                            db_root_config['user'],
                                                                            db_root_config['password'],
                                                                            db_root_config['dbport'],
                                                                            db_root_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def create_new_person(self, p_fname, p_lname, p_role, p_email, p_phone, p_gender):
        cursor = self.conn.cursor()
        query = 'insert into "person" (p_fname, p_lname, p_role, p_email, p_phone,p_gender) values (%s,%s,%s,%s,%s,' \
                '%s) returning p_id; '
        cursor.execute(query, (p_fname, p_lname, p_role, p_email, p_phone, p_gender,))
        p_id = cursor.fetchone()[0]
        self.conn.commit()
        return p_id

    def update_person(self, p_id, p_fname, p_lname, p_email, p_phone, p_gender):
        cursor = self.conn.cursor()
        query = 'update "person" ' \
                'set p_fname = %s, p_lname= %s, p_email= %s , p_phone = %s ,p_gender= %s ' \
                'where p_id = %s '
        cursor.execute(query, (p_fname, p_lname, p_email, p_phone, p_gender, p_id))
        self.conn.commit()
        return True

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
        query = 'select p_id, p_fname, p_lname, p_role, p_email, p_phone ,p_gender ' \
                'from "person";'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_person_by_id(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_fname, p_lname, p_role, p_email, p_phone, p_gender ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))
        result = cursor.fetchone()
        return result

    def get_dict_person_by_id(self, p_id: int):
        cursor = self.conn.cursor()
        query = 'select p_fname, p_lname, p_role, p_email, p_phone, p_gender ' \
                'from "person" where p_id = %s;'
        cursor.execute(query, (p_id,))

        columnsnames = ["p_fname", "p_lname", "p_role", "p_email", "p_phone", "p_gender"]
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
    def get_most_booked_persons(self):
        cursor = self.conn.cursor()
        query = 'select p_id, p_fname , p_lname,  count(booking.host_id) as bookings ' \
                'from booking inner join person on person.p_id = booking.host_id ' \
                'GROUP BY p_id  order by bookings desc limit 10; '
        cursor.execute(query)
        result = []
        for row in cursor:
            print(row)
            result.append(row)
        return result

    # Retrieves the most used room
    def get_most_logged_person(self):
        cursor = self.conn.cursor()
        query = 'select p_id, count(booking.invited_id) as logged ' \
                'from booking inner join person on person.p_id = booking.invited_id inner join person on ' \
                'booking.invited_id = person.p_id ' \
                'group by p_id ' \
                ' order by logged desc limit 1; '
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Retrieves the person that has been most invited and the amount of times
    def get_person_that_most_share_with_person(self, p_id):
        cursor = self.conn.cursor()
        query = "with bomeeting as " \
                "(select booking.b_id,booking.st_dt,booking.et_dt,booking.invited_id,booking.host_id,booking. room_id, subt.meeting " \
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



    # TODO -> Make more complex
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

    def get_info_for_student(self):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, room_id, host_id' \
                'from booking;  '
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_info_for_professor(self):
        cursor = self.conn.cursor()
        query = 'select st_dt, et_dt, room_id, host_id, invite_id' \
                'from booking;  '
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_info_for_staff(self):
        cursor = self.conn.cursor()
        query = 'select *' \
                'from booking;  '
        cursor.execute(query, )
        result = []
        for row in cursor:
            result.append(row)
        return result
