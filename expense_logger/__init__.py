import os
from datetime import datetime
from pytz import timezone
from time import time

import flask
from flask import session
import dotenv

from expense_logger import oauth, spreadsheet, db, user


dotenv.load_dotenv()

app = flask.Flask(__name__, static_folder='../static')

app.config.from_mapping(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    DATABASE='expense_logger.sqlite',
)

db.init_app(app)


@app.before_request
def make_session_permanent():
    flask.session.permanent = True


@app.route('/')
def expense_form():
    if not 'credentials' in session:
        return flask.redirect(flask.url_for('authorize'))
    elif not 'spreadsheet_id' in session:
        return flask.redirect(flask.url_for('spreadsheet_form'))

    return flask.render_template('expense_form.html')


@app.route('/post-expense', methods=['POST'])
def post_expense():
    if not 'credentials' in session:
        flask.abort(401)

    try:
        amount = float(flask.request.form['amount'])
        description = str(flask.request.form['description'])
    except ValueError:
        flask.abort(400)

    entry_spreadsheet_id = session['spreadsheet_id']

    timestamp = int(time())
    entry_datetime_with_timezone = datetime.now().astimezone(
        timezone('Europe/Riga')).strftime('%Y-%m-%d %H:%M:%S')

    row = [timestamp, entry_datetime_with_timezone, amount, description]

    spreadsheet.append_row(entry_spreadsheet_id, row)

    return flask.redirect(flask.url_for('expense_form'))


@app.route('/set-spreadsheet', methods=['GET'])
def spreadsheet_form():
    return flask.render_template('spreadsheet_id_form.html')


@app.route('/set-spreadsheet', methods=['POST'])
def set_spreadsheet():
    if not 'credentials' in session:
        flask.abort(401)

    session['spreadsheet_id'] = flask.request.form['spreadsheet_id']

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

    response_credentials = oauth.get_credentials(
        get_oauth_callback_url(),
        state,
        authorization_response
    )

    user.process_user(response_credentials)

    return flask.redirect(flask.url_for('expense_form'))


@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']

    if 'spreadsheet_id' in session:
        del session['spreadsheet_id']

    return flask.redirect(flask.url_for('expense_form'))


def get_oauth_callback_url():
    return flask.url_for('oauth2_callback', _external=True)
