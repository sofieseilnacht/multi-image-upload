from .client import *
import json

class S3FileWriter:

    def __init__(self, bucketName, bucketUrl):
        self.bucket = bucketName
        self.urls = {}
        self.bucketUrl = bucketUrl  ## HACK - this should be derivable from S3 and the key

    def write(self, path, image, descriptor):
        if (image == None):
            return
        imageType = descriptor['type']
        contentType = descriptor['content-type']
        createImageFiles(self.bucket, path, image, contentType)
        self.urls[imageType] = self.getKeyUrl(path)

    def writeJson(self, path, data, descriptor):
        fileType = descriptor['type']
        contentType = descriptor['content-type']
        createImageFiles(self.bucket, path, json.dumps(data), contentType)
        self.urls[fileType] = self.getKeyUrl(path)

    def getUrlByType(self, urlType):
        if urlType['type'] in self.urls:
            return self.urls[urlType['type']]
        else:
            return None

    def getKeyUrl(self, key):
        return self.bucketUrl+'/'+key

