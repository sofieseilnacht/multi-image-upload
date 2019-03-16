import gspread
from oauth2client.service_account import ServiceAccountCredentials

from app.google.config import *

class Client:
    table_headers = ['id','image-url', 'log-url', 'fits-url', 'parity', 'orientation', 'pixscale','radius','ra','dec']
    etable_headers = ['id','image-url','log-url', 'error']

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

    def addSuccessToSheet(self, worksheet, imageUrl, logUrl, fitsUrlList, calibrationResultList):
        for jobId in fitsUrlList.keys():
            if jobId in calibrationResultList :
                rowData = []
                for columnKey in self.table_headers:
                    if columnKey == 'id' :
                        rowData.append(str(jobId))
                    elif columnKey == 'image-url' :
                        rowData.append(imageUrl)
                    elif columnKey == 'log-url' :
                        rowData.append(logUrl)
                    elif columnKey == 'fits-url' :
                        rowData.append(fitsUrlList[jobId])
                    else :
                        rowData.append(calibrationResultList[jobId][columnKey])
                worksheet.append_row(values=rowData, value_input_option='RAW')

    def addErrorToSheet(self, worksheet, imageUrl,logUrl, astrometrySubmission):
        for calibration in astrometrySubmission['jobs']:
            errorData = []
            i = 0
            errorData[i]= imageUrl
            i+=1
            for key in self.table_headers:
                errorData[i] = calibration[key]
                i+=1
            worksheet.append_row(values=errorData, value_input_option='RAW')


    def deleteSheet(self, spreadsheet):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials.json', scope)
        gc = gspread.authorize(credentials)

        gc.del_spreadsheet(spreadsheet)

    def closeWorksheets(self):
        google_client.session.close()