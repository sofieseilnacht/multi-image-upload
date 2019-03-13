import os

from .astrometry.client import *
from .aws.client import *
from .google.client import Client

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
        print('procesing: '+ file)
        # initial file meta data as part of log data (where from, who from, original url, ...)
        setPublicReadPermissions(file)
        imageUrl = s3_bucket_url+'/'+file
        submission = submitAstrometryUrl(imageUrl,loginSession)
        (head, tail) = os.path.split(file)

        if ('status' in submission) :

            if (submission['status'] == 'success') :

                status = waitOnAstrometrySubmissionDone(submission['subid'])
                createLog(tail, status['body'])
                #only get fits files if we get a calibration
                if (len(status['body']['job_calibrations']) > 0) :
                    createFitsFiles(tail, status['fits'])

                #if soln, create fits and move image to archive. if no fits, move image to error
                imageUrl = imageBucketUrl+'/'+imageBucketName+'/archive/'+file
                if (len(status['fits']) == 0) :
                    moveImage(tail, imageBucketName, 'error')
                    google_client.addErrorToSheet(error_ws, imageUrl, submission)

                else:
                   moveImage(tail, imageBucketName, 'archive')
                   fitsUrl = imageBucketUrl+'/'+imageBucketName+'/fits/'+file
                   google_client.addSuccessToSheet(success_ws, imageUrl, fitsUrl, status)


        else:
            createErrorLog(tail, submission)
            moveImage(tail, imageBucketName, 'error')
            google_client.addErrorToSheet(error_ws, imageUrl, submission)



