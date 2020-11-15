import os.path
import pickle
from googleapiclient.discovery import build

import time
from pprint import pprint

# TODO: pass from ENV
SHEET_ID = '1NMknWqv4PQdhsbpzWA3xCBaIfM95Uo10M-EL3KXl4ak'

RANGE = 'Sheet1'
# RANGE = 'Sheet1!A1:D5'

def apend_row(sheet, row):
    values = [
        row
    ]

    _apend(sheet, values)

def apend_test(sheet):
    values = [
        ['123', 'foo'],
        ['234', 'bar'],
    ]

    _apend(sheet, values)

def _apend(sheet, values):
    body = {
        'values': values
    }

    result = sheet.values().append(
        spreadsheetId=SHEET_ID,
        range=RANGE,
        valueInputOption='RAW',
        body=body
    ).execute()

    print('{0} cells appended.'.format(
        result.get('updates').get('updatedCells')
    ))

def get_sheet_data(sheet):
    request = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE)

    response = request.execute()

    pprint(response)

def create(sheet):
    ts = round(time.time())
    title = 'sheets_api_test-' + str(ts)

    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = sheet.create(
        body=spreadsheet,
        fields='spreadsheetId'
    ).execute()

    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))

def get_sheet():
    creds = _get_creds()

    service = build('sheets', 'v4', credentials=creds)

    # pylint: disable=maybe-no-member
    return service.spreadsheets()

def _get_creds():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    return creds