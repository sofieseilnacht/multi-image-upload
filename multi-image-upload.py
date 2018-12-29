import configparser
import os
from astrometry import client as astrometry_client
from aws import client as aws_client

# read configuration
config = configparser.ConfigParser()
config.read('myconfig.ini')
archive_flag = config['myapplication']['archive_flag']


# login
loginSession = astrometry_client.astrometryLogin()

# return file generator over S3 bucket
files = aws_client.listS3Files('pending/')
for file in files:

    # initial file meta data as part of log data (where from, who from, original url, ...)
    submission = astrometry_client.submitAstrometryUrl(file, loginSession)
    (head, tail) = os.path.split(file)

    imageUrl = aws_client.getFileUrl(file)

    if ('status' in submission) :
        if (submission['status'] == 'success') :
            status = astrometry_client.waitOnAstrometrySubmissionDone(submission['subid'])
            aws_client.createLog(tail, status)
        if (archive_flag) :
            aws_client.archiveImage(tail)
    else :
        aws_client.createErrorLog(tail, submission)
