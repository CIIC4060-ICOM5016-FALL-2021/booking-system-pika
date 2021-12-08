from flask import jsonify
from account.model import AccountDAO

def build_account_attrdict(self, row):
    result = {'p_id': row[0], 'p_fname': row[1], 'p_email': row[2], 'p_password': row[3]}
    return result

class Account:

    def get_account_by_email(self, json):
        dao = AccountDAO()
        return

    def create_new_account(self, json):
        dao = AccountDAO()
        return

    def delete_account(self, json):
        dao = AccountDAO()

        return