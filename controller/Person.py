from flask import jsonify

from models.AvailablePerson import AvailablePersonDAO
from models.Person import PersonDAO


def create_new_person(json: dict):
    p_fname = json['p_fname']
    p_lname = json['p_lname']
    p_role = json['p_role']
    p_email = json['p_email']
    p_phone = json['p_phone']
    p_gender = json['p_gender']
    p_password = json['p_password']
    method = PersonDAO()
    p_id = method.create_new_person(p_fname, p_lname, p_role, p_email, p_phone, p_gender, p_password)
    return jsonify({"p_id": p_id})


def get_all_persons(limit: int = 125):
    method = PersonDAO()
    count = method.count_person()
    if count != 0:
        data = method.get_all_person(limit)
        persons: dict = {}
        result: dict = {'count': count, 'persons': {}}
        for index, row in enumerate(data):
            persons[index] = {
                'p_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(row[0])
            }
        result['persons'] = persons
        return jsonify(result), 200
    else:
        return jsonify("There are no Persons around"), 404


def get_person(person):
    method = PersonDAO()
    if type(person) == int:
        if not method.check_if_person_exists(person):
            return jsonify("Person does not exist"), 404
        else:
            person_data = method.get_person_by_id(person)
            return jsonify({
                'first_name': person_data[0],
                'last_name': person_data[1],
                'gender': method.genders[person_data[5]],
                'role': method.roles[person_data[2]],
                'email': person_data[3],
                'phone': person_data[4]

            }), 200
    elif type(person) == str:
        p = str(person).split('-')
        if len(p) != 2:
            return jsonify("Full Name does not match First-Last name format"), 404
        person_data = method.get_person_by_name(p[0], p[1])
        if not person_data:
            return jsonify("Person does not exist"), 404
        else:
            return jsonify({
                'p_id': person_data[0],
                'gender': method.genders[person_data[4]],
                'role': method.roles[person_data[1]],
                'email': person_data[2],
                'phone': person_data[3]
            }), 200
    else:
        return jsonify("TypeError. Input person is not an integer (person id)"
                       " nor a string (person name separated by '-'"), 404


def get_persons_by_role(r_id):
    method = PersonDAO()
    count = method.count_person_by_role(r_id)
    if count != 0:
        data = method.get_all_person_by_role(r_id)
        result: dict = {'count': count, 'role': method.roles[r_id], 'persons': {}}
        persons = {}
        for index, row in enumerate(data):
            persons[index] = {
                'p_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(row[0])
            }
        result['persons'] = persons
        return jsonify(result), 200
    else:
        return jsonify("There are no Persons around"), 404


def update_person(json: dict):
    p_id = json['p_id']
    p_fname = json['p_fname']
    p_lname = json['p_lname']
    p_phone = json['p_phone']
    p_gender = json['p_gender']
    method = PersonDAO()
    exist = method.check_if_person_exists(p_id)
    updated_info = method.update_person(p_id, p_fname, p_lname, p_phone, p_gender)
    if updated_info and exist:
        return jsonify(True), 200
    else:
        return jsonify('Not found person'), 404


def delete_person(p_id: int):
    method = PersonDAO()
    result = method.delete_person(p_id)
    if result:
        method2 = AvailablePersonDAO()
        method2.delete_unavailable_person_schedule(p_id)
        return jsonify("Person Deleted Successfully")
    else:
        return jsonify("Person Not Found"), 404


def get_person_that_most_share_with_person(p_id: int):
    method = PersonDAO()
    if method.check_if_person_exists(p_id):
        data = method.get_person_that_most_share_with_person(p_id)
        return jsonify({
            'p_id': p_id,
            'shared_p_id': data
        }), 200
    else:
        return jsonify("Target person does not exists"), 404


def get_hosts_that_invited_this_person(invitee_id: int):
    method = PersonDAO()
    if method.check_if_person_exists(invitee_id):
        data = method.get_hosts_that_invited_this_person(invitee_id)
        result = {}
        for index, row in enumerate(data):
            result[index] = {
                'host_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'shared_times': row[3],
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(row[0])
            }
        return jsonify(result), 200

    else:
        return jsonify("Target person does not exists"), 404


def get_most_used_room_by_person(p_id: int):
    method = PersonDAO()
    if method.check_if_person_exists(p_id):
        data = method.get_most_used_room_by_person(p_id)
        return jsonify({
            'r_id': data[0],
            'r_name': data[1],
            'times_used': data[2],
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/rooms/' + str(data[0])
        })
    else:
        return jsonify("Target person does not exists"), 404


# Retrieves the person who performed the most amount of bookings
def get_person_who_booked_most(limit_thingy=10):
    method = PersonDAO()
    data = method.get_person_who_booked_most(limit_thingy)
    result = {}
    for index, row in enumerate(data):
        result[index] = {
            'p_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'bookings': row[3],
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(row[0])
        }
    return jsonify(result), 200


def get_account_info(json: dict):
    p_email = json['p_email']
    p_password = json['p_password']
    method = PersonDAO()
    data = method.get_account_info(p_email, p_password)
    if not data:
        return jsonify("Not Found"), 404
    else:
        return jsonify({
            'p_id': data[0],
            'first_name': data[1],
            'last_name': data[2],
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(data[0])
        }), 200
