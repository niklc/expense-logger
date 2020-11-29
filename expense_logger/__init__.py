import os

import flask

from expense_logger import google_services


SPREADSHEET_ID = '1NMknWqv4PQdhsbpzWA3xCBaIfM95Uo10M-EL3KXl4ak'


app = flask.Flask(__name__, static_folder='../static')
app.secret_key = 'random secret key 123'  # TODO


@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    return flask.render_template('index.html')


@app.route('/post-expense', methods=['POST'])
def post_expense():
    if 'credentials' not in flask.session:
        flask.abort(401)

    try:
        amount = float(flask.request.form['amount'])
        description = str(flask.request.form['description'])
    except ValueError:
        flask.abort(400)

    sheet = google_services.get_sheet(flask.session['credentials'])

    row = [amount, description]

    google_services.append_row(sheet, SPREADSHEET_ID, row)

    return flask.redirect(flask.url_for('index'))


@app.route('/authorize')
def authorize():
    authorization_url, state = google_services.authorize(get_oauth_callback_url())

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    authorization_response = flask.request.url

    credentials = google_services.oauth_callback(get_oauth_callback_url(), state, authorization_response)

    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('index'))


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']

    return flask.redirect(flask.url_for('index'))


def get_oauth_callback_url():
    return flask.url_for('oauth2callback', _external=True)

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
