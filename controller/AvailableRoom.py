from flask import jsonify
import datetime as dt

class AvailableRoom:

    def build_unavailable_time_room_map_dict(self, row):
        result = {'unavailable_time_room_id': row[0], 'unavailable_time_room_start': row[1],
                  'unavailable_time_room_finish': row[2], 'room_id': row[3]}
        return result