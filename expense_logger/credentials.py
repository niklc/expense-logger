from flask import session


KEY = 'credentials'


def is_credentials_set():
    if KEY in session:
        return True

    return False


def get_credentials():
    return session[KEY]


def set_credentials(credentials):
    session[KEY] = credentials


def delete_credentials():
    del session[KEY]
