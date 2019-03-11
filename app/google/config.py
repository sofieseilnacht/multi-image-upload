import gspread
from oauth2client.service_account import ServiceAccountCredentials
import configparser

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')
json_keyfile = config['google']['credentials']

# reference for scopes - https://developers.google.com/identity/protocols/googlescopes
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
google_client = gspread.authorize(credentials)
