from .client import *

class JobCalibration:

    def __init__(self, job_id, calibration_id):
        self.jobId = job_id
        self.calibrationId = calibration_id


    def getStatus(self):
        if self.status == None :
            self.loadCalibrationData()

        return self.status

    # def getJob(self):
    #     return Job(self.jobId, self)

    def loadCalibrationData(self):
        self.calibrationStatus = checkCalibrationStatus(self.jobId)

        if self.calibrationStatus != None :
            self.__privateSetCalibrationDetails()

    def __privateSetCalibrationDetails(self):
        self.parity = self.calibrationStatus['parity']
        self.orientation = self.calibrationStatus['orientation']
        self.pixscale = self.calibrationStatus['pixscale']
        self.radius = self.calibrationStatus['radius']
        self.ra = self.calibrationStatus['ra']
        self.dec = self.calibrationStatus['dec']

