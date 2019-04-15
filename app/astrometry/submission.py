from .client import *
from .job import Job
from .jobCalibration import JobCalibration
import time


class Submission:

    PROCESSING_STARTED = 'processing_started'
    PROCESSING_FINISHED = 'processing_finished'
    IN_PROGRESS = 'in_progress'
    NOT_STARTED = 'not_started'

    def __init__(self, submissionId, status):
        self.submissionId = submissionId
        self.processingStatus = self.NOT_STARTED
        self.submissionStatus = status

    def waitUntilProcessingDone(self):
        while( self.getProcessingStatus() != self.PROCESSING_FINISHED ):
            time.sleep(10)

        ##waitOnAstrometrySubmissionDone(self.submissionId)

    def waitOnJobs(self):
        while (len(self.submissionDetail['jobs']) == 0 or self.submissionDetail['jobs'][0] == None) :
            time.sleep(10)
            self.submissionDetail = checkSubmissionStatus(self.submissionId)

        jobList = self.getJobList()
        for job in jobList:
            job.waitUntilDone()


    def isDone(self):
        self.getProcessingStatus()
        return self.processingStatus == self.PROCESSING_FINISHED

    def getProcessingStatus(self):
        if not self.processingStatus == self.PROCESSING_FINISHED:
            self.checkSubmissionStatus()

        return self.processingStatus

    def getStatus(self):
        return self.submissionStatus

    def getJobList(self):
        jobList = []
        if (self.processingStatus == self.PROCESSING_FINISHED):
            for job_id in self.submissionDetail['jobs']:
                job = Job(job_id)
                jobList.append(job)
        else:
            return None

        return jobList

    def getJobCalibrationList(self):
        calibrationList = []

        ## refresh submissionDetail
        self.submissionDetail = checkSubmissionStatus(self.submissionId)

        if (self.processingStatus == self.PROCESSING_FINISHED):
            for calibrationPair in self.submissionDetail['job_calibrations']:
                calibration = JobCalibration(calibrationPair[0],calibrationPair[1])
                calibrationList.append(calibration)
        else:
            return None

        return calibrationList

    def checkSubmissionStatus(self):
        self.submissionDetail = checkSubmissionStatus(self.submissionId)

        if 'processing_started' not in self.submissionDetail:
            self.processingStatus = self.NOT_STARTED
        elif self.submissionDetail['processing_started'] == 'None':
            self.processingStatus = self.NOT_STARTED
        else:
            self.processingStatus = self.IN_PROGRESS

        if 'processing_finished' in self.submissionDetail \
                and self.submissionDetail['processing_finished'] != 'None' \
                and self.submissionDetail['processing_finished'] != '':
                self.processingStatus = self.PROCESSING_FINISHED

        return self.processingStatus





