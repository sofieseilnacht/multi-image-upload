from .client import *
from .submission import Submission

class MetadataFactory:

    astrometryUrl = 'http://nova.astrometry.net'

    ## create factory: config file ref, api key, url key, S3 bucket
    def __init__(self, astrometryApiKey):
        self.astrometryApiKey = astrometryApiKey
        self.loginSession = astrometryLogin()

    def submitImage(self, url, invert):
        submissionJson = submitAstrometryUrl(url,self.loginSession)
        submission = Submission(submissionJson['subid'], submissionJson['status'])
        return submission

    def getImageMetadata(self, submission):
        submission = waitOnAstrometrySubmissionDone(submission.submissionId)

        return submission




