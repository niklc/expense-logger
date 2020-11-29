import googleapiclient.discovery
import google.oauth2.credentials

from expense_logger import credentials

SHEETS_VALUE_INPUT_OPTION = 'RAW'

SPREADSHEET_RANGE = 'Sheet1'


def append_row(sheet_id, row):
    sheet = _get_sheet()

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


def _get_sheet():
    google_credentials = google.oauth2.credentials.Credentials(
        **credentials.getCredentials()
    )

    # pylint: disable=maybe-no-member
    return googleapiclient.discovery.build(
        'sheets', 'v4', credentials=google_credentials
    ).spreadsheets()
