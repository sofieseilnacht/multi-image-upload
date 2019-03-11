import json

from app.aws.config import *

def getFileUrl(file):
    return s3_bucket_url+'/'+file


#Gives a list of image files in s3 Bucket
def listS3Files(bucketName, prefix):
    #List files in specific S3 URL
    response = client.list_objects(Bucket=bucketName, Prefix=prefix)
    for content in response.get('Contents', []):
        key = content.get('Key')
        if key.endswith( ('.jpg', '.jpeg', '.png', '.gif') ):
            yield key

#Gives a list of image files in s3 Bucket
# def listS3Files(prefix):
#     #List files in specific S3 URL
#     response = client.list_objects(Bucket=s3_imagebucket, Prefix=prefix)
#     for content in response.get('Contents', []):
#         key = content.get('Key')
#         if key.endswith( ('.jpg', '.jpeg', '.png', '.gif') ):
#             yield key

def setPublicReadPermissions(path):
    object_acl = s3.ObjectAcl(s3_imagebucket,path)
    response = object_acl.put(ACL='public-read')


# def archiveImage(file, bucket):
#     copyResponse = s3.meta.client.copy_object(
#         ACL='public-read',
#         Bucket=bucket,
#         CopySource={'Bucket': bucket, 'Key': "pending/"+file},
#         Key="archive/"+file
#     )
#     if (copyResponse['ResponseMetadata']['HTTPStatusCode'] == 200) :
#         deleteResponse = s3.meta.client.delete_object(Bucket=bucket, Key="pending/"+file)

def moveImage(file, bucket, key):
    copyResponse = s3.meta.client.copy_object(
        ACL='public-read',
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': "pending/"+file},
        Key=key+"/"+file
    )
    if (copyResponse['ResponseMetadata']['HTTPStatusCode'] == 200) :
        deleteResponse = s3.meta.client.delete_object(Bucket=bucket, Key="pending/"+file)

def createLog(name, data):
    logObject = s3.Object(s3_imagebucket, 'logs/'+name+".json")
    logObject.put(Body=json.dumps(data))
    setPublicReadPermissions('logs/'+name+".json")

def createFitsFiles(name, fitsFileList):
    for fitsJobID in fitsFileList.keys():
        fitsImage = fitsFileList[fitsJobID]
        fitsJobIDStr = "{0}".format(fitsJobID)
        name = 'fits/'+name+"-"+fitsJobIDStr+".fits"
        logObject = s3.Object(s3_imagebucket, name)
        logObject.put(Body= (fitsImage))
        setPublicReadPermissions(name)

def createErrorLog(name, data):
    logObject = s3.Object(s3_imagebucket, 'errors/'+name+".json")
    logObject.put(Body=json.dumps(data))
    setPublicReadPermissions('errors/'+name+".json")
