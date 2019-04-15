
class AstrometryException:

    def __init__(self, url, jobId, status, detail):
        self.url = url
        self.jobId = jobId
        self.status = status
        self.detail = detail

