import os
from datetime import datetime
from pytz import timezone
from time import time

import flask

from expense_logger import oauth, spreadsheet, credentials


PLACEHOLDER_SPREADSHEET_ID = '1NMknWqv4PQdhsbpzWA3xCBaIfM95Uo10M-EL3KXl4ak'


app = flask.Flask(__name__, static_folder='../static')
app.secret_key = 'random secret key 123'  # TODO


@app.route('/')
def index():
    if not credentials.isCredentialsSet():
        return flask.redirect('authorize')

    return flask.render_template('index.html')


@app.route('/post-expense', methods=['POST'])
def post_expense():
    if not credentials.isCredentialsSet():
        flask.abort(401)

    try:
        amount = float(flask.request.form['amount'])
        description = str(flask.request.form['description'])
    except ValueError:
        flask.abort(400)

    timestamp = int(time())
    entry_datetime_with_timezone = datetime.now().astimezone(timezone('Europe/Riga')).strftime('%Y-%m-%d %H:%M:%S')

    row = [timestamp, entry_datetime_with_timezone, amount, description]

    spreadsheet.append_row(PLACEHOLDER_SPREADSHEET_ID, row)

    return flask.redirect(flask.url_for('index'))


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

    credentials.setCredentials(response_credentials)

    return flask.redirect(flask.url_for('index'))


@app.route('/clear')
def clear_credentials():
    if credentials.isCredentialsSet():
        credentials.deleteCredentials()

    return flask.redirect(flask.url_for('index'))


def get_oauth_callback_url():
    return flask.url_for('oauth2_callback', _external=True)
