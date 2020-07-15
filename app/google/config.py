import gspread
from oauth2client.service_account import ServiceAccountCredentials
import configparser
from pathlib import Path

home = str(Path.home())
# read configuration and create statics
config = configparser.ConfigParser()
config.read(home+'/.astrometry/myconfig.ini')
config.set("google", "home_dir", home)

json_keyfile = config['google']['credentials']

# reference for scopes - https://developers.google.com/identity/protocols/googlescopes
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
google_client = gspread.authorize(credentials)
