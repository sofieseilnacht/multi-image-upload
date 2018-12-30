import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.config import *

table_headers = ['id','image-url', 'parity', 'orientation', 'pixscale','radius','ra','dec']

## docs https://gspread.readthedocs.io/en/latest/index.html
def openSheet(spreadsheet, worksheet):

    try:
        sheet = google_client.open(spreadsheet)
    except gspread.exceptions.GSpreadException as e:
        sheet = google_client.create(spreadsheet)
        # share the sheet to anyone for read
        sheet.share('mike.seilnacht@gmail.com', perm_type='user', role='writer', notify=True, email_message="new sheet for you.")
        # https://gspread.readthedocs.io/en/latest/api.html
        #sheet.share('', role='reader', type='anyone')
        sheet.share(None, perm_type='anyone', role='reader', notify=True, email_message="new sheet for you.")

    ws = None
    try:
        ws = sheet.worksheet(worksheet)
    except gspread.exceptions.GSpreadException as e:
        ws = sheet.add_worksheet(worksheet,1,len(table_headers))
        ws.resize(1)
        ws.append_row(values=table_headers, value_input_option='RAW')

    return ws

def deleteSheet(spreadsheet):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
    gc = gspread.authorize(credentials)

    gc.del_spreadsheet(spreadsheet)

def closeWorksheets():
    google_client.session.close()