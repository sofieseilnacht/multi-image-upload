import configparser
from pathlib import Path

home = str(Path.home())

# read configuration and create statics
config = configparser.ConfigParser()
config.read(home+'/.astrometry/myconfig.ini')
apikey = config['nova.astrometry.net']['apikey']
base_url = config['nova.astrometry.net']['base_url']
login_path = config['nova.astrometry.net']['login_path']

url_upload_path = config['nova.astrometry.net']['url_upload_path']
upload_url = base_url+url_upload_path
web_upload_url = "http://nova.astrometry.net/upload"

login_url = base_url+login_path
submit_status_url = base_url+"/api/submissions/"
job_status_url = base_url+"/api/jobs/"

#upload_url = base_url+url_upload_path
