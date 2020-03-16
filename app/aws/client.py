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
        if key.lower().endswith( ('.jpg', '.jpeg', '.png', '.gif', '.fits') ):
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
    return response

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
    setPublicReadPermissions('pending/'+file)
    copyResponse = s3.meta.client.copy_object(
        ACL='public-read',
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': "pending/"+file},
        Key=key+"/"+file
    )
    setPublicReadPermissions(key+'/'+file)
    if (copyResponse['ResponseMetadata']['HTTPStatusCode'] == 200) :
        deleteResponse = s3.meta.client.delete_object(Bucket=bucket, Key="pending/"+file)

    archiveUrl = getFileUrl(key+'/'+file)
    return archiveUrl

def createLog(name, data):
    url = getFileUrl('logs/'+name+'.json')
    logObject = s3.Object(s3_imagebucket, 'logs/'+name+'.json')
    logObject.put(Body=json.dumps(data),ContentType='application/json')
    setPublicReadPermissions('logs/'+name+'.json')
    return url

def createFitsFiles(name, fitsFileList):
    # return if no work to do
    if (len(fitsFileList) == 0) :
        return
    fitsUrlList = {}
    for fitsJobID in fitsFileList.keys():
        fitsJobIDStr = "{0}".format(fitsJobID)
        print('createFitsFile: '+fitsJobIDStr)
        fitsImage = fitsFileList[fitsJobID]
        name = 'fits/'+name+"-"+fitsJobIDStr+".fits"
        fitsUrlList[fitsJobID] = getFileUrl(name)
        logObject = s3.Object(s3_imagebucket, name)
        logObject.put(Body= (fitsImage), ACL='public-read')
        setPublicReadPermissions(name)
    return fitsUrlList

def createImageFiles(bucket, path, image, contentType):
    logObject = s3.Object(s3_imagebucket, path)
    logObject.put(Body= (image), ACL='public-read', ContentType=contentType)
    setPublicReadPermissions(path)

def createErrorLog(name, data):
    url = getFileUrl('errors/'+name+'.json')
    logObject = s3.Object(s3_imagebucket, 'errors/'+name+'.json')
    logObject.put(Body=json.dumps(data))
    setPublicReadPermissions('errors/'+name+'.json')
    return
