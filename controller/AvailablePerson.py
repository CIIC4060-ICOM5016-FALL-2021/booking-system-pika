from flask import jsonify

from controller import Person
from models.AvailablePerson import AvailablePersonDAO
from models.Booking import BookingDAO
from models.Person import PersonDAO


#############################
# GET PERSON SCHEDULE.
# INCLUDES BOOKING SCHEDULES
# AND UNAVAILABLE SPACES
#############################
def get_schedule(person_id: int):

    method1 = AvailablePersonDAO()
    method2 = PersonDAO()

    if method2.check_if_person_exists(person_id):
        data = method1.get_all_schedule(person_id)

        result: list = []
        for st_dt, et_dt, schedule, name in data:
            result.append({
                'name': name,
                'start_time': st_dt,
                'end_time': et_dt,
                'schedule_id': schedule,
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/unavailable-schedule/'
                       + str(schedule) if name == 'unavailable'
                else 'https://booking-system-pika.herokuapp.com/pika-booking/bookings/' + str(schedule)
            })

        return jsonify(result), 200
    else:
        return jsonify("Person Not Found"), 404


#############################
# CREATE UNAVAILABLE
# TIMEFRAME
#############################
def create_unavailable_schedule(json):
    method = PersonDAO()
    person_id = json['person_id']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    if method.check_if_person_exists(person_id):
        method2 = AvailablePersonDAO()
        pa_id = method2.create_unavailable_person_time(st_dt, et_dt, person_id)
        return jsonify({'pa_id': pa_id}), 200
    else:
        return jsonify("Person doesn't exist"), 404


#############################
# GET ALL UNAVAILABLE
# TIMEFRAMES IN DATABASE
#############################
def get_all_unavailable_persons():
    method = AvailablePersonDAO()
    unavailable_persons = method.get_all_unavailable_person()
    if not unavailable_persons:
        return jsonify("There are no separated spaces"), 404
    else:
        result: list = []
        for pa_id, st_dt, et_dt, person_id in unavailable_persons:
            result.append({
                'pa_id': pa_id,
                'person_id': person_id,
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/unavailable-schedule/' + str(pa_id),
                'person_url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(person_id)
            })
        return jsonify(result), 200


#############################
# UPDATE UNAVAILABLE
# TIMEFRAME
#############################
def update_unavailable_schedule(json: dict):
    pa_id = json['pa_id']
    person_id = json['person_id']
    st_dt = json['st_dt']
    et_dt = json['et_dt']
    method = AvailablePersonDAO()
    method2 = PersonDAO()
    if method2.check_if_person_exists(person_id):
        method.update_unavailable_person(pa_id, st_dt, et_dt, person_id)
        return jsonify(True), 200
    else:
        return jsonify('Not found person'), 404


#############################
# GET 24h SCHEDULE FOR A
# PERSON AT A GIVEN DATE
#############################
def get_all_day_schedule(json: dict):
    person_id = json['person_id']
    date = json['date']

    method = AvailablePersonDAO()
    method2 = PersonDAO()

    if method2.check_if_person_exists(person_id):
        data = method.get_all_day_schedule(person_id, date)
        result: list = []
        for st_dt, et_dt, schedule, name in data:
            result.append({
                'name': name,
                'start_time': st_dt,
                'end_time': et_dt,
                'schedule_id': schedule,
                'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/unavailable-schedule/'
                       + str(schedule) if name == 'unavailable'
                else 'https://booking-system-pika.herokuapp.com/pika-booking/bookings/' + str(schedule)
            })
        return jsonify(result), 200
    else:
        return jsonify("Person doesn't exist"), 404


def get_unavailable_person_by_id(pa_id):
    method = AvailablePersonDAO()
    person = method.get_unavailable_person_by_id(pa_id)
    if not person:
        return jsonify("No unavailable schedule found"), 404
    else:
        return jsonify({
            'start_time': person[0],
            'end_time': person[1],
            'person_id': person[2],
            'url': 'https://booking-system-pika.herokuapp.com/pika-booking/persons/' + str(person[0])
        }), 200


####################################################################
def get_unavailable_person_by_person_id(person_id: int):
    method = AvailablePersonDAO()

    person_dao = PersonDAO()
    existing_person = person_dao.get_person_by_id(person_id)

    if not existing_person:
        return jsonify("That person is available")
    else:
        res = method.get_unavailable_person_by_person_id(person_id)
        result_st_dt = []
        result_et_dt = []
        for st_dt, et_dt in res:
            result_et_dt.append(et_dt)
            result_st_dt.append(st_dt)
        result = {
            "st_dt": result_st_dt,
            "et_dt": result_et_dt
        }
        return jsonify(result), 200
