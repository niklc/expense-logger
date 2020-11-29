import googleapiclient.discovery
import google_auth_oauthlib.flow
import google.oauth2.credentials


CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# see https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
SHEETS_VALUE_INPUT_OPTION = 'RAW'

SPREADSHEET_RANGE = 'Sheet1'


def get_sheet(credentials):
    credentials = google.oauth2.credentials.Credentials(**credentials)

    # pylint: disable=maybe-no-member
    return googleapiclient.discovery.build(
        'sheets', 'v4', credentials=credentials).spreadsheets()


def append_row(sheet, sheet_id, row):
    body = {
        'values': [
            row
        ]
    }

    sheet.values().append(
        spreadsheetId=sheet_id,
        range=SPREADSHEET_RANGE,
        valueInputOption=SHEETS_VALUE_INPUT_OPTION,
        body=body
    ).execute()


def authorize(redirect_uri):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = redirect_uri

    return flow.authorization_url(
        access_type='online',
        include_granted_scopes='false'
    )


def oauth_callback(callback_url, state, authorization_response):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = callback_url

    flow.fetch_token(authorization_response=authorization_response)

    return flow.credentials
