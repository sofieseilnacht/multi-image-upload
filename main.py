import configparser
from app.upload import uploadImagesNew
from pathlib import Path
import os, sys

cwd = os.getcwd()
sys.path.insert(0, cwd)
sys.path.insert(0, cwd+"/app")

# read configuration and create statics
home = str(Path.home())
config = configparser.ConfigParser()
config.read(home+'/.astrometry/myconfig.ini')
config.set("google", "home_dir", home)

#local_image_dir= config['nova.astrometry.net']['image_dir']
s3_imagebucket = config['aws.s3']['s3_bucket']
s3_bucket_url = config['aws.s3']['s3_bucket_url']
archive_flag = config['myapplication']['archive_flag']

uploadImagesNew(s3_imagebucket, s3_bucket_url, archive_flag)