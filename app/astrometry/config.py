import configparser

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')
apikey = config['nova.astrometry.net']['apikey']
base_url = config['nova.astrometry.net']['base_url']
login_path = config['nova.astrometry.net']['login_path']

url_upload_path = config['nova.astrometry.net']['url_upload_path']
upload_url = base_url+url_upload_path

login_url = base_url+login_path
submit_status_url = base_url+"/api/submissions/"
job_status_url = base_url+"/api/jobs/"

#upload_url = base_url+url_upload_path
