
class MetaData:

    def __init__(self, job_id):
        self.jobId = job_id

    def getMachineTags(self):
        if not hasattr(self, 'machineTags'):
            self.machineTags = getJobMachineTags(self.jobId)

        return self.machineTags

    def getTags(self):
        if not hasattr(self, 'tags'):
            self.tags = getJobTags(self.jobId)

        return self.tags

    def getAnnotations(self):
        if not hasattr(self, 'annotations'):
            self.annotations = getJobAnnotations(self.jobId)

        return self.annotations


