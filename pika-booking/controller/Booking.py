from flask import jsonify
from models.Booking import BookingDAO
class Booking:
    def build_booking_map_dict(self, row):
        result = {'b_id': row[0], 'st_dt': row[1], 'et_dt': row[2], 'invited_id': row[3],
                  'host_id': row[4],'room_id': row[5]}
        return result

    def build_Booking_attr_dict(self, b_id, st_dt, et_dt, invited_id, host_id, room_id):
        result = {}
        result['b_id'] = b_id
        result['st_dt'] = st_dt
        result['et_dt'] = et_dt
        result['invited_id'] = invited_id
        result['host_id'] = host_id
        result['room_id'] = room_id
        return result

    def createNewBooking(self,json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        method = BookingDAO()
        b_id = method.createNewBooking(st_dt, et_dt, invited_id, host_id, room_id)
        result = self.build_Booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        return jsonify(result)

    def getAllBooking(self):
        method = BookingDAO()
        booking_list = method.getAllBookings()
        result_list = []
        for row in booking_list:
            result_list.append(self.build_booking_map_dict(row))
        return jsonify(result_list)

    def getBookingById(self, booking_id):
        method = BookingDAO()
        booking_tuple = method.getBookingById(booking_id)
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

    def updateBooking(self, json):
        st_dt = json['st_dt']
        et_dt = json['et_dt']
        invited_id = json['invited_id']
        host_id = json['host_id']
        room_id = json['room_id']
        b_id = json['b_id']
        method =BookingDAO()
        updatedinfo = method.update_booking(b_id, st_dt, et_dt, invited_id, host_id, room_id)
        if updatedinfo:
         result = self.build_Booking_attr_dict(b_id, st_dt, et_dt, invited_id, host_id, room_id)
         return jsonify(result)
        else:
             return jsonify('Not found person')

    def deleteBooking(self, b_id):
        method = BookingDAO()
        result = method.delete_booking(b_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND"), 404


