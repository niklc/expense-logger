import googleapiclient.discovery
import google.oauth2.credentials


# see https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
SHEETS_VALUE_INPUT_OPTION = 'RAW'

SPREADSHEET_RANGE = 'Sheet1'


def append_row(credentials, sheet_id, row):
    sheet = _get_sheet(credentials)

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


def _get_sheet(credentials):
    credentials = google.oauth2.credentials.Credentials(**credentials)

    # pylint: disable=maybe-no-member
    return googleapiclient.discovery.build(
        'sheets', 'v4', credentials=credentials).spreadsheets()
