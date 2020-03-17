from .client import *
from .jobCalibration import *
from .progressBar import *


class Job:

    SUCCESS = 'success'
    SOLVING = 'solving'
    FAILURE = 'failure'

    JOB_OPTIONS = {'url_template':'----NONE----', 'file_suffix':'jobsettings.json', 'type':'JOB-OPTIONS', 'content-type': 'application/json'}
    JOB_LOG = {'url_template':'http://nova.astrometry.net/joblog/{0}/', 'file_suffix':'joblog.txt', 'type':'JOB-LOG', 'content-type': 'text/plain'}
    JOB_LOG2 = {'url_template':'http://nova.astrometry.net/joblog2/{0}/', 'file_suffix':'joblog2.txt', 'type':'JOB-LOG2', 'content-type': 'text/plain'}
    JSON_INFO = {'url_template':'http://nova.astrometry.net/api/jobs/{0}/info', 'file_suffix':'info.json', 'type':'JSON-INFO', 'content-type': 'application/json'}
    WCS_FITS_IMAGE  = {'url_template':'http://nova.astrometry.net/wcs_file/{0}', 'file_suffix':'wcs.fits', 'type':'WCS', 'content-type': 'application/fits'}
    NEW_FITS_IMAGE  = {'url_template':'http://nova.astrometry.net/new_fits_file/{0}', 'file_suffix':'new.fits', 'type':'NEW_FITS', 'content-type': 'application/fits'}
    RDLS_FITS_TABLE = {'url_template':'http://nova.astrometry.net/rdls_file/{0}', 'file_suffix':'rdls.fits', 'type':'RDLS', 'content-type': 'application/fits'}
    AXY_FITS_TABLE  = {'url_template':'http://nova.astrometry.net/axy_file/{0}', 'file_suffix':'axy.fits', 'type':'AXY', 'content-type': 'application/fits'}
    CORR_FITS_TABLE = {'url_template':'http://nova.astrometry.net/corr_file/{0}', 'file_suffix':'corr.fits', 'type':'CORR', 'content-type': 'application/fits'}
    ANNOTATED_IMAGE  = {'url_template':'http://nova.astrometry.net/annotated_display/{0}', 'file_suffix':'annotated.jpg', 'type':'ANNOTATED', 'content-type': 'image/jpeg'}
    RED_GREEN_IMAGE  = {'url_template':'http://nova.astrometry.net/red_green_image_display/{0}', 'file_suffix':'red_green.jpg' ,'type':'RED_GREEN', 'content-type': 'image/jpeg'}
    EXTRACTION_IMAGE = {'url_template':'http://nova.astrometry.net/extraction_image_display/{0}', 'file_suffix':'extraction.jpg', 'type':'EXTRACTION', 'content-type': 'image/jpeg'}

    def __init__(self, job_id, calibration):
        self.jobId = job_id
        self.calibration = calibration
        self.status = None

    def getStatus(self):
        if self.status != None:
            return self.status

        return getJobStatus(self.jobId)

    def waitUntilDone(self):
        progressBar = ProgressBar("Job:waitUntilDone("+str(self.jobId)+")")
        jobStatusJson = getJobStatus(self.jobId)
        while (jobStatusJson['status'] == None or jobStatusJson['status'] == '' or jobStatusJson['status'] == 'solving'):
            progressBar.incrementAndPause(10)
            jobStatusJson = getJobStatus(self.jobId)
            self.status = jobStatusJson['status']
        progressBar.done()

    def getCalibration(self):
        ##calibration_status = getJobCalibration2(self.jobId)
        if self.status == 'success' and self.calibration == None :
            self.calibration = JobCalibration(self.jobId, None)
            self.calibration.loadCalibrationData()

        return self.calibration

    def getFileName(self, imageType):
        return str(self.jobId)+imageType['file_suffix']

    def getCorrelationImage(self, imageType):
        url = imageType['url_template'].format(self.jobId)
        return getCalibrationImageFile(url)

    def getInfo(self):
        return getJobInfo(self.jobId)

