from .client import *
from .jobCalibration import JobCalibration


class Job:

    SUCCESS = 'success'
    SOLVING = 'solving'
    FAILURE = 'failure'

    def __init__(self, job_id):
        self.jobId = job_id
        self.calibration = None
        self.status = None

    def getStatus(self):
        if self.status != None:
            return self.status

        return getJobStatus(self.jobId)

    def waitUntilDone(self):
        jobStatusJson = getJobStatus(self.jobId)
        while (jobStatusJson['status'] == None or jobStatusJson['status'] == '' or jobStatusJson['status'] == 'solving'):
            time.sleep(10)
            jobStatusJson = getJobStatus(self.jobId)
            self.status = jobStatusJson['status']

    def getCalibration(self):
        ##calibration_status = getJobCalibration2(self.jobId)
        if self.status == 'success' and self.calibration == None :
            self.calibration = JobCalibration(self.jobId, None)
            self.calibration.checkCalibrationStatus()

        return self.calibration
