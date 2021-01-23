import googleapiclient.discovery
import google.oauth2.credentials
from flask import session


SHEETS_VALUE_INPUT_OPTION = 'RAW'


def append_row(spreadsheet_id, sheet_id, row):
    sheet = _get_sheet()

    body = {
        'values': [
            row
        ]
    }

    sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_id,
        valueInputOption=SHEETS_VALUE_INPUT_OPTION,
        body=body
    ).execute()


def _get_sheet():
    google_credentials = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    # pylint: disable=maybe-no-member
    return googleapiclient.discovery.build(
        'sheets', 'v4', credentials=google_credentials
    ).spreadsheets()
