import configparser
from app.upload import uploadImages

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')

#local_image_dir= config['nova.astrometry.net']['image_dir']
s3_imagebucket = config['aws.s3']['s3_bucket']
s3_bucket_url = config['aws.s3']['s3_bucket_url']
archive_flag = config['myapplication']['archive_flag']

uploadImages(s3_imagebucket, s3_bucket_url, archive_flag)