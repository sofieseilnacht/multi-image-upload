from app.aws.s3FileWriter import S3FileWriter
from .client import *
from app.astrometry.job import Job

class GoogleSheetLogger:

    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.googleClient = Client()
        self.successSheet = self.googleClient.openSheet(spreadsheet,"success")
        self.errorSheet = self.googleClient.openSheet(spreadsheet,"error")

    def logSuccess(self, name, job, imageUrl, s3FileWriter):
        logEntry = {'id': str(job.jobId),
                    'image-name' : name,
                    'ra' : job.calibration.ra,
                    'dec' : job.calibration.dec,
                    'parity' : job.calibration.parity,
                    'orientation' : job.calibration.orientation,
                    'pixscale' : job.calibration.pixscale,
                    'radius' : job.calibration.radius,
                    'job-settings' : s3FileWriter.getUrlByType(Job.JOB_OPTIONS),
                    'job-log' : s3FileWriter.getUrlByType(Job.JOB_LOG),
                    'job-log2' : s3FileWriter.getUrlByType(Job.JOB_LOG2),
                    'image-url' : imageUrl,
                    'job-info' : s3FileWriter.getUrlByType(Job.JSON_INFO),
                    'wcs-fits-url' : s3FileWriter.getUrlByType(Job.WCS_FITS_IMAGE),
                    'new-fits-url' : s3FileWriter.getUrlByType(Job.NEW_FITS_IMAGE),
                    'rdls-fits-url' : s3FileWriter.getUrlByType(Job.RDLS_FITS_TABLE),
                    'axy-fits-url' : s3FileWriter.getUrlByType(Job.AXY_FITS_TABLE),
                    'corr-fits-url' : s3FileWriter.getUrlByType(Job.CORR_FITS_TABLE),
                    'annotated-image-url' : s3FileWriter.getUrlByType(Job.ANNOTATED_IMAGE),
                    'red-green-image-url' : s3FileWriter.getUrlByType(Job.RED_GREEN_IMAGE),
                    'extraction-image-url' : s3FileWriter.getUrlByType(Job.EXTRACTION_IMAGE)}

        self.googleClient.appendToSuccessSheet(self.successSheet, logEntry)

    def logError(self, id, name, image_url, error_string):
        logEntry = {'id': str(id),
                    'image-name' : name,
                    'image-url' : image_url,
                    'log-url' : '',
                    'error' : error_string}

        self.googleClient.appendToErrorSheet(self.errorSheet, logEntry)