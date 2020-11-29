import os

import flask
import googleapiclient.discovery
import google_auth_oauthlib.flow
import google.oauth2.credentials


CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# see https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
SHEETS_VALUE_INPUT_OPTION = 'RAW'  # USER_ENTERED

SPREADSHEET_ID = '1NMknWqv4PQdhsbpzWA3xCBaIfM95Uo10M-EL3KXl4ak'
SPREADSHEET_RANGE = 'Sheet1'


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

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # pylint: disable=maybe-no-member
    sheet = googleapiclient.discovery.build(
        'sheets', 'v4', credentials=credentials).spreadsheets()

    row = [amount, description]

    body = {
        'values': [
            row
        ]
    }

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SPREADSHEET_RANGE,
        valueInputOption=SHEETS_VALUE_INPUT_OPTION,
        body=body
    ).execute()

    return flask.redirect(flask.url_for('index'))


@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='online',
        include_granted_scopes='false'
    )

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('index'))


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']

    return flask.redirect(flask.url_for('index'))


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
