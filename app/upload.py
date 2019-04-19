import os

from .astrometry.client import *
from .aws.client import *
from .google.client import Client
from .astrometry.metadataFactory import MetadataFactory
from .astrometry.job import Job
from .aws.s3FileWriter import S3FileWriter
from .astrometry.submission import Submission
from .google.googleSheetLogger import GoogleSheetLogger

def hasFitsFiles(fitsList) :
    return len(fitsList) > 0

def createFitsUrlList (imageBucketUrl, imageBucketName, fitsFileList):
    fitsUrlList = {}
    for key in fitsFileList.keys() :
        fitsUrlList[key] = imageBucketUrl+'/'+imageBucketName+'/fits/'+fitsFileList[key]
    return fitsUrlList

def uploadImagesNew(imageBucketName, imageBucketUrl, archiveFlag):

    config = configparser.ConfigParser()
    config.read('myconfig.ini')
    apikey = config['nova.astrometry.net']['apikey']

    metadataFactory = MetadataFactory(apikey)
    logger = GoogleSheetLogger("astrometry.net")

    # return file generator over S3 bucket
    filePaths = listS3Files(imageBucketName, 'pending/')

    for filePath in filePaths:
        (path, name) = os.path.split(filePath)
        print('processing: '+ filePath)
        # initial file meta data as part of log data (where from, who from, original url, ...)
        setPublicReadPermissions(filePath)
        imageUrl = s3_bucket_url+'/'+filePath
        s3FileWriter = S3FileWriter(imageBucketName, s3_bucket_url)

        ## rest API call using astrometry.net account API key
        submitOptions = metadataFactory.getPrintableOptions(imageUrl,False)
        submission = metadataFactory.submitImage(imageUrl,False)
        jobList = submission.getSolvedJobs()
        settingsLogPrefix = 'logs/'+name+'/'+str(submission.submissionId)+'-'

        if len(jobList) == 0 :
            ## web API call as anonymous user
            #submission = metadataFactory.webSubmitImage(imageUrl,True)
            submitOptions = metadataFactory.getPrintableOptions(imageUrl,True)
            invertedSubmission = metadataFactory.webSubmitImage(imageUrl,True)
            jobList = invertedSubmission.getSolvedJobs()

        s3FileWriter.writeJson(settingsLogPrefix+'submitsettings.json',submitOptions,Job.JOB_OPTIONS)
        ## TODO - need to capture start and elapsed times
        ## TODO - add error handling and allow calls to throw exception - decompose into smaller simple functions
        if len(jobList) != 0 :
            imagePath = 'images/'+name+'/'
            ## wrap in try block
            for job in jobList:
                ## write out job detail files
                jobInfoLog = job.getInfo()
                jobLogPrefix = 'logs/'+name+'/'+str(job.jobId)+'-'
                s3FileWriter.writeJson(jobLogPrefix+'jobinfo.json',jobInfoLog,Job.JSON_INFO)

                ## write out the image files
                imageDescriptors = [Job.WCS_FITS_IMAGE, Job.NEW_FITS_IMAGE, Job.RDLS_FITS_TABLE, Job.AXY_FITS_TABLE, Job.CORR_FITS_TABLE, Job.ANNOTATED_IMAGE, Job.RED_GREEN_IMAGE, Job.EXTRACTION_IMAGE]
                imageFilePrefix = imagePath+str(job.jobId)+'-'
                for descriptor in imageDescriptors:
                    image = job.getCorrelationImage(descriptor)
                    imageFilename = job.getFileName(descriptor)
                    s3FileWriter.write(imageFilePrefix+imageFilename, image, descriptor)

                ## write out the job logs
                logDescriptors = [Job.JOB_LOG, Job.JOB_LOG2]
                logFilePrefix = 'logs/'+name+'/'+str(job.jobId)+'-'
                for descriptor in logDescriptors:
                    log = metadataFactory.getLogFile(job.jobId,descriptor)
                    logFilename = job.getFileName(descriptor)
                    s3FileWriter.write(logFilePrefix+logFilename, log, descriptor)

            archiveUrl = moveImage(name, imageBucketName, 'archive')
            logger.logSuccess(name, job, archiveUrl, s3FileWriter)
        else:
            archiveUrl = moveImage(name, imageBucketName, 'error')
            logger.logError(submission.submissionId, name, archiveUrl, "no solution")


# def uploadImages(imageBucketName, imageBucketUrl, archiveFlag) :
#     google_client = Client()
#     #google_client.deleteSheet("astrometry.net")
#     success_ws = google_client.openSheet("astrometry.net","success")
#     error_ws = google_client.openSheet("astrometry.net","error")
#
#     # login
#     loginSession = astrometryLogin()
#
#     # return file generator over S3 bucket
#     files = listS3Files(imageBucketName, 'pending/')
#
#     for file in files:
#         print('processing: '+ file)
#         # initial file meta data as part of log data (where from, who from, original url, ...)
#         setPublicReadPermissions(file)
#         imageUrl = s3_bucket_url+'/'+file
#         submissionStatus = submitAstrometryUrl(imageUrl, False, loginSession)
#         (head, tail) = os.path.split(file)
#
#         if ('status' in submissionStatus) :
#
#             if (submissionStatus['status'] == 'success') :
#
#                 submission = waitOnAstrometrySubmissionDone(submissionStatus['subid'])
#                 logUrl = createLog(tail, submission['body'])
#
#                 #if soln, create fits and move image to archive. if no fits, move image to error
#                 if (hasFitsFiles(submission['fits'])) :
#                     imageUrl = moveImage(tail, imageBucketName, 'archive')
#                     fitsFileUrlList = createFitsFiles(tail, submission['fits'])
#                     google_client.addSuccessToSheet(success_ws, imageUrl, logUrl, fitsFileUrlList, submission['body']['calibration_results'])
#                 else :
#                     imageUrl = moveImage(tail, imageBucketName, 'error')
#                     google_client.addErrorToSheet(error_ws, imageUrl, logUrl, submission['body'])
#
#         else:
#             logUrl = createErrorLog(tail, submissionStatus)
#             imageUrl = moveImage(tail, imageBucketName, 'error')
#             google_client.addErrorToSheet(error_ws, imageUrl, logUrl, submissionStatus)
#



