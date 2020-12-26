from flask import session

KEY = 'spreadsheet_id'

def is_spreadsheet_id_set():
    if KEY in session:
        return True

    return False


def get_spreadsheet_id():
    return session[KEY]


def set_spreadsheet_id(credentials):
    session[KEY] = credentials


def delete_spreadsheet_id():
    del session[KEY]
