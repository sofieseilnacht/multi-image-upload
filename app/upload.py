import os

from .astrometry.client import *
from .aws.client import *
from .google.client import Client

def hasFitsFiles(fitsList) :
    return len(fitsList) > 0

def createFitsUrlList (imageBucketUrl, imageBucketName, fitsFileList):
    fitsUrlList = {}
    for key in fitsFileList.keys() :
        fitsUrlList[key] = imageBucketUrl+'/'+imageBucketName+'/fits/'+fitsFileList[key]
    return fitsUrlList

def uploadImages(imageBucketName, imageBucketUrl, archiveFlag) :
    google_client = Client()
    #google_client.deleteSheet("astrometry.net")
    success_ws = google_client.openSheet("astrometry.net","success")
    error_ws = google_client.openSheet("astrometry.net","error")

    # login
    loginSession = astrometryLogin()

    # return file generator over S3 bucket
    files = listS3Files(imageBucketName, 'pending/')

    for file in files:
        print('processing: '+ file)
        # initial file meta data as part of log data (where from, who from, original url, ...)
        setPublicReadPermissions(file)
        imageUrl = s3_bucket_url+'/'+file
        submissionStatus = submitAstrometryUrl(imageUrl,loginSession)
        (head, tail) = os.path.split(file)

        if ('status' in submissionStatus) :

            if (submissionStatus['status'] == 'success') :

                submission = waitOnAstrometrySubmissionDone(submissionStatus['subid'])
                logUrl = createLog(tail, submission['body'])

                #if soln, create fits and move image to archive. if no fits, move image to error
                if (hasFitsFiles(submission['fits'])) :
                    imageUrl = moveImage(tail, imageBucketName, 'archive')
                    fitsFileUrlList = createFitsFiles(tail, submission['fits'])
                    google_client.addSuccessToSheet(success_ws, imageUrl, logUrl, fitsFileUrlList, submission['body']['calibration_results'])
                else :
                    imageUrl = moveImage(tail, imageBucketName, 'error')
                    google_client.addErrorToSheet(error_ws, imageUrl, logUrl, submission['body'])

        else:
            logUrl = createErrorLog(tail, submissionStatus)
            imageUrl = moveImage(tail, imageBucketName, 'error')
            google_client.addErrorToSheet(error_ws, imageUrl, logUrl, submissionStatus)




