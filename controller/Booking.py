from flask import jsonify
from models.Booking import BookingDAO


class Booking:
    def build_booking_map_dict(self, row):
        result = {'b_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'invited_id': row[3],
                  'host_id': row[4], 'room_id': row[5]}
        return result

    def build_booking_attr_dict(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        return self.build_booking_map_dict([b_id, st_dt, et_dt, invited_id, host_id, room_id])

    def create_new_booking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        method = BookingDAO()
        b_id = method.create_new_booking(st_dt, et_dt, invited_id, host_id, room_id)
        result = self.build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        return jsonify(result)

    def get_all_booking(self):
        method = BookingDAO()
        booking_list = method.get_all_bookings()
        result_list = []
        for row in booking_list:
            result_list.append(self.build_booking_map_dict(row))
        return jsonify(result_list)

    def get_booking_by_id(self, b_id):
        method = BookingDAO()
        booking_tuple = method.get_booking_by_id(b_id)
        if not booking_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_booking_map_dict(booking_tuple)
            return jsonify(result), 200

    # def getAllUnavailableUsers(self):
    #     method = BookingDAO()
    #     unavailable_users_list = method.getAllUnavailableUsers()
    #     result_list = []
    #     for row in unavailable_users_list:
    #         obj = self.build_unavailable_time_user_dict(row)
    #         result_list.append(obj)
    #     return jsonify(result_list)

    def update_booking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        b_id = json['b_id']
        method = BookingDAO()
        updatedinfo = method.update_booking(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        if updatedinfo:
            result = self.build_booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
            return jsonify(result)
        else:
            return jsonify('Not found person')

    def delete_booking(self, b_id):
        method = BookingDAO()
        result = method.delete_booking(b_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404
