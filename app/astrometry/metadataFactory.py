from .client import *
from .submission import Submission
import re
from .job import Job

class MetadataFactory:

    astrometryUrl = 'http://nova.astrometry.net'

    ## create factory: config file ref, api key, url key, S3 bucket
    def __init__(self, astrometryApiKey):
        self.astrometryApiKey = astrometryApiKey
        self.loginSession = astrometryLogin()

    def submitImage(self, url, invert):
        submissionJson = submitAstrometryUrl(url, self.loginSession, invert)
        submission = Submission(submissionJson['subid'], submissionJson['status'])
        return submission

    def getImageMetadata(self, submission):
        submission = waitOnAstrometrySubmissionDone(submission.submissionId)

        return submission

    def getPrintableOptions(self, url, invert):
        settings = newAstromertyUploadSettings(url, '########', invert)
        return settings

    def getLogFile(self, jobId, descriptor):
        url = descriptor['url_template'].format(jobId)
        data = getLogFile(url)
        return data

    def getUploadCsrfToken(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        html = getUrlAsText(headers,'http://nova.astrometry.net/upload')
        searchObj = re.search('name=\'csrfmiddlewaretoken\'\svalue=\'(\w+)\'',html)
        csrfToken = searchObj.group(1)
        return csrfToken

    def webSubmitImage(self, url, invert):
        csrfToken = self.getUploadCsrfToken()
        ## form data post
        submissionId =  astrometryWebSubmit(url, self.loginSession, csrfToken, invert)

        # TODO - this needs error handling
        submissionStatus = checkSubmissionStatus(submissionId)
        submission = Submission(submissionId,"success")
        return submission


