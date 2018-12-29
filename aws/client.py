import json
from aws.config import *

def getFileUrl(file):
    return s3_bucket_url+'/'+file

#Gives a list of image files in s3 Bucket
def listS3Files(prefix):
    #List files in specific S3 URL
    response = client.list_objects(Bucket=s3_imagebucket, Prefix=prefix)
    for content in response.get('Contents', []):
        key = content.get('Key')
        if key.endswith( ('.jpg', '.jpeg', '.png', '.gif') ):
            yield key

def archiveImage(file):
    copyResponse = s3.meta.client.copy_object(
        ACL='public-read',
        Bucket=s3_imagebucket,
        CopySource={'Bucket': s3_imagebucket, 'Key': "pending/"+file},
        Key="archive/"+file
    )
    if (copyResponse['ResponseMetadata']['HTTPStatusCode'] == 200) :
        deleteResponse = s3.meta.client.delete_object(Bucket=s3_imagebucket, Key="pending/"+file)

def createLog(name, data):
    logObject = s3.Object(s3_imagebucket, 'logs/'+name+".json")
    logObject.put(Body=json.dumps(data))

def createErrorLog(name, data):
    logObject = s3.Object(s3_imagebucket, 'errors/'+name+".json")
    logObject.put(Body=json.dumps(data))
