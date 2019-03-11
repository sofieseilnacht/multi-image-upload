import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.google.config import *

class Client:
    table_headers = ['id','image-url', 'fits-url', 'parity', 'orientation', 'pixscale','radius','ra','dec']

    ## docs https://gspread.readthedocs.io/en/latest/index.html
    def openSheet(self, spreadsheet, worksheet):

        try:
            sheet = google_client.open(spreadsheet)
        except gspread.exceptions.GSpreadException as e:
            sheet = google_client.create(spreadsheet)
            # share the sheet to anyone for read
            sheet.share('sofie.seilnacht@berkeley.edu', perm_type='user', role='writer', notify=True, email_message="new sheet for you.")
            # https://gspread.readthedocs.io/en/latest/api.html
            #sheet.share('', role='reader', type='anyone')
            sheet.share(None, perm_type='anyone', role='reader', notify=True, email_message="new sheet for you.")

        ws = None
        try:
            ws = sheet.worksheet(worksheet)
        except gspread.exceptions.GSpreadException as e:
            ws = sheet.add_worksheet(worksheet,1,len(self.table_headers))
            ws.resize(1)
            ws.append_row(values=self.table_headers, value_input_option='RAW')

        return ws

    def addRowToSheet(self, worksheet, values):
        rowData= []
        i = 0
        for key in self.table_headers:
            rowData[i] = values[key]
            i+=1
        worksheet.append_row(values=rowData, value_input_option='RAW')

    def addSuccessToSheet(self, worksheet, imageUrl, fitsUrl, astrometryStatus):
        for calibration in astrometryStatus['job_calibrations']:
            successData = []
            i = 0
            successData[i]= imageUrl
            i+=1
            for key in self.table_headers:
                successData[i] = calibration[key]
                i+=1
            worksheet.append_row(values=successData, value_input_option='RAW')


    #def addErrorToSheet(worksheet, url, astrometrySubmission):


    def deleteSheet(self, spreadsheet):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
        gc = gspread.authorize(credentials)

        gc.del_spreadsheet(spreadsheet)

    def closeWorksheets(self):
        google_client.session.close()