from .client import *
from .job import Job

class JobCalibration:

    def __init__(self, job_id, calibration_id):
        self.jobId = job_id
        self.calibrationId = calibration_id


    def getStatus(self):
        if self.status == None :
            self.checkCalibrationStatus()

        return self.status

    def getJob(self):
        return Job(self.jobId)

    def checkCalibrationStatus(self):
        self.calibrationStatus = checkCalibrationStatus(self.jobId)

        if self.calibrationStatus == None :
            self.status = self.IN_PROGRESS
        elif 'processing_finished' not in self.submissionStatus:
            if 'processing_started' not in self.submissionStatus:
                self.status = self.IN_PROGRESS
            else:
                self.status = self.PROCESSING_STARTED
        else:
            self.__privateSetCalibrationDetails()
            self.status = self.PROCESSING_FINISHED

        return self.status

    def __privateSetCalibrationDetails(self):
        self.parity = self.calibrationStatus['parity']
        self.orientation = self.calibrationStatus['orientation']
        self.pixscale = self.calibrationStatus['pixscale']
        self.radius = self.calibrationStatus['radius']
        self.ra = self.calibrationStatus['ra']
        self.dec = self.calibrationStatus['dec']

