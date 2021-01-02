import os
from datetime import datetime
from pytz import timezone
from time import time

import flask
import dotenv

from expense_logger import oauth, spreadsheet, credentials, spreadsheet_id


dotenv.load_dotenv()

app = flask.Flask(__name__, static_folder='../static')
app.secret_key = os.getenv('SECRET_KEY')


@app.before_request
def make_session_permanent():
    flask.session.permanent = True


@app.route('/')
def expense_form():
    if not credentials.is_credentials_set():
        return flask.redirect(flask.url_for('authorize'))
    elif not spreadsheet_id.is_spreadsheet_id_set():
        return flask.redirect(flask.url_for('spreadsheet_form'))

    return flask.render_template('expense_form.html')


@app.route('/post-expense', methods=['POST'])
def post_expense():
    if not credentials.is_credentials_set():
        flask.abort(401)

    try:
        amount = float(flask.request.form['amount'])
        description = str(flask.request.form['description'])
    except ValueError:
        flask.abort(400)

    entry_spreadsheet_id = spreadsheet_id.get_spreadsheet_id()

    timestamp = int(time())
    entry_datetime_with_timezone = datetime.now().astimezone(timezone('Europe/Riga')).strftime('%Y-%m-%d %H:%M:%S')

    row = [timestamp, entry_datetime_with_timezone, amount, description]

    spreadsheet.append_row(entry_spreadsheet_id, row)

    return flask.redirect(flask.url_for('expense_form'))

@app.route('/set-spreadsheet', methods=['GET'])
def spreadsheet_form():
    return flask.render_template('spreadsheet_id_form.html')


@app.route('/set-spreadsheet', methods=['POST'])
def set_spreadsheet():
    if not credentials.is_credentials_set():
        flask.abort(401)

    spreadsheet_id.set_spreadsheet_id(flask.request.form['spreadsheet_id'])

    return flask.redirect(flask.url_for('expense_form'))


@app.route('/authorize')
def authorize():
    authorization_url, state = oauth.get_request_token(
        get_oauth_callback_url()
    )

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/authorize-callback')
def oauth2_callback():
    state = flask.session['state']

    authorization_response = flask.request.url

    response_credentials = oauth.get_access_token(
        get_oauth_callback_url(),
        state,
        authorization_response
    )

    credentials.set_credentials(response_credentials)

    return flask.redirect(flask.url_for('expense_form'))


@app.route('/clear')
def clear_credentials():
    if credentials.is_credentials_set():
        credentials.delete_credentials()

    if spreadsheet_id.is_spreadsheet_id_set():
        spreadsheet_id.delete_spreadsheet_id()

    return flask.redirect(flask.url_for('expense_form'))


def get_oauth_callback_url():
    return flask.url_for('oauth2_callback', _external=True)
