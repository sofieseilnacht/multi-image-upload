import boto3
import configparser

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')
s3_imagebucket = config['aws.s3']['s3_bucket']
s3_bucket_url = config['aws.s3']['s3_bucket_url']


s3 = boto3.resource('s3')
client = boto3.client('s3')


