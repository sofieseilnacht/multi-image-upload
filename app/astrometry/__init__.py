import configparser
from pathlib import Path

# read configuration and create statics
home = str(Path.home())
config = configparser.ConfigParser()
config.read(home+'/.astrometry/myconfig.ini')
config.set("google", "home_dir", home)

apikey = config['nova.astrometry.net']['apikey']
base_url = config['nova.astrometry.net']['base_url']
login_path = config['nova.astrometry.net']['login_path']
url_upload_path = config['nova.astrometry.net']['url_upload_path']
login_url = base_url+login_path
upload_url = base_url+url_upload_path
submit_status_url = base_url+"/api/submissions/"
#image_dir= config['nova.astrometry.net']['image_dir']
# s3_imagebucket = config['aws.s3']['s3_bucket']
# s3_bucket_url = config['aws.s3']['s3_bucket_url']
