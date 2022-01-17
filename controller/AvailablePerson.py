from flask import jsonify

from models.AvailablePerson import AvailablePersonDAO
from models.Booking import BookingDAO
from models.Person import PersonDAO


def create_unavailable_time_schedule(json: dict):
    person_id = json['person_id']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    method = PersonDAO()

    if method.check_if_person_exists(person_id):
        method2 = AvailablePersonDAO()
        pa_id = method2.create_unavailable_person_time(st_dt, et_dt, person_id)
        return jsonify({
            "pa_id": pa_id,
            'st_dt': st_dt,
            'et_dt': et_dt,
            'p_id': person_id,
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(person_id)
        }), 200
    else:
        return jsonify("Person doesn't exist"), 404


def get_all_unavailable_persons(limit_thingy: int = 75):
    method = AvailablePersonDAO()
    count = method.count_unavailable_timeframes()
    if count != 0:
        data = method.get_all_unavailable_person(limit_thingy)
        unavailable: dict = {}
        result: dict = {'count': count, 'unavailable_timeframes': {}}
        for index, row in enumerate(data):
            unavailable[index] = {
                'pa_id': row[0],
                'st_dt': row[1],
                'et_dt': row[2],
                'person_id': row[3],
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(row[0])
            }
        result['unavailable_timeframes'] = unavailable
        return jsonify(result), 200


#################################
def update_unavailable_schedule(json: dict):
    pa_id = json['pa_id']
    person_id = json['person_id']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    method = AvailablePersonDAO()
    method2 = PersonDAO()
    method3 = BookingDAO()

    exist = method.check_if_person_exists(p_id)
    updated_info = method.update_person(p_id, p_fname, p_lname, p_phone, p_gender)
    if updated_info and exist:
        return jsonify(True), 200
    else:
        return jsonify('Not found person'), 404





        method2 = Person
        exist = method2.persons_by_id_exist(person_id)
        updated_info = method.update_unavailable_person(pa_id, st_dt, et_dt, person_id)

        if updated_info and exist:
            result = self.build_unavailable_person_attr_dict(pa_id, st_dt, et_dt, person_id)
            return jsonify(result)
        else:
            return jsonify('Not found person')

#######
def delete_unavailable_schedule(person_id: int):
    method = AvailablePersonDAO()
    method2 = PersonDAO()

    result = method.delete_unavailable_person_schedule(person_id)
    if result:
        return jsonify("DELETED")
    else:
       return jsonify("NOT FOUND")