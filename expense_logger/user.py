from flask import session

from expense_logger import db


def process_user(response_credentials):
    session['credentials'] = response_credentials

    user_data = _get_existing_user_data(response_credentials['user_id'])
    if user_data:
        _set_session(user_data)
    else:
        _save_user(response_credentials)


def _get_existing_user_data(user_id):
    return db.get_db().execute(
        'SELECT * FROM user WHERE google_user_id = ?',
        (user_id,)
    ).fetchone()


def _set_session(user_data):
    session['credentials']['refresh_token'] = user_data['refresh_token']
    session['spreadsheet_id'] = user_data['spreadsheet_id']
    session['sheet_id'] = user_data['sheet_id']


def _save_user(credentials):
    connection = db.get_db()

    connection.execute(
        'INSERT INTO user (google_user_id, refresh_token) VALUES (?, ?)',
        (credentials['user_id'], credentials['refresh_token'])
    )

    connection.commit()


def set_sheet_config(user_id, spreadsheet_id, sheet_id):
    connection = db.get_db()

    connection.execute(
        'UPDATE user SET spreadsheet_id = ?, sheet_id = ? WHERE google_user_id = ?',
        (spreadsheet_id, sheet_id, user_id)
    )

    connection.commit()
