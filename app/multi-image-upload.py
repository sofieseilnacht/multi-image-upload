import os

from astrometry.client import *
from aws.client import *
from google.client import Client

#log in to astrometry and return a session
# def astrometryLogin(url, apikey):
#     try:
#         R = requests.post(url, data={'request-json': json.dumps({"apikey": apikey})})
#         print(R.text)
#         if (R.status_code == 200):
#             responseJson = R.json()
#             return responseJson["session"]
#     except requests.exceptions.RequestException as e:
#         print(e)
#         raise(e)
#
#     return None


# #Gives a list of image files in s3 Bucket
# def listS3Files(client, bucketName, prefix):
#     #List files in specific S3 URL
#     response = client.list_objects(Bucket=bucketName, Prefix=prefix)
#     for content in response.get('Contents', []):
#       key = content.get('Key')
#       if key.endswith( ('.jpg', '.jpeg', '.png', '.gif') ):
#           yield key

#gives list of files on local dir
# def listFiles(path):
#     folder = os.fsencode(path)
#     filenames = []
#     for file in os.listdir(folder):
#         filename = os.fsdecode(file)
#         if filename.endswith( ('.jpg', '.jpeg', '.png', '.gif') ): # whatever file types you're using...
#             filenames.append(filename)
#     filenames.sort() # now you have the filenames and can do something with them
#     return filenames


# def submitAstrometryUrl(file):
#     imageUrl = s3_bucket_url+'/'+file
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     settings = newAstromertyUploadSettings(imageUrl, loginSession)
#
#     try:
#         response = requests.post(upload_url, headers=headers, data={'request-json': json.dumps(settings)})
#
#         if (response.status_code == 200) :
#             body = response.json()
#
#         else:
#             print("request failed: "+imageUrl+", statuscode: "+str(response.status_code))
#             body = {"url" : imageUrl, "status" : "http error", "error_code" : str(response.status_code)}
#
#     except requests.exceptions.RequestException as e:
#         body = {"url" : imageUrl, "status" : "client error", "error_code" : str(e.response['Error']['Code'])}
#
#     return body

# def getAstrometryCalibrationResults(job_ids) :
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     calibrations = []
#
#     for job_id in job_ids:
#         job_url = base_url+'/api/jobs/'+str(job_id)+'/calibration/'
#         try:
#             response = requests.get(job_url, headers=headers)
#
#             if response.status_code == requests.codes.ok:
#                 body = response.json()
#
#             else:
#                 print("request failed: "+job_url+", statuscode: "+str(response.status_code))
#                 body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(response.status_code)}
#
#         except requests.exceptions.RequestException as e:
#             print("request failed: "+job_url+", statuscode: "+str(response.status_code))
#             body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(e.response['Error']['Code'])}
#
#         calibrations.append(body)
#
#     return calibrations

# def waitOnAstrometryJobsSuccess(job_ids):
#     headers = {'User-Agent': 'Mozilla/5.0'}
#
#     for job_id in job_ids:
#         url = job_status_url+str(job_id)
#         response = requests.get(url, headers=headers)
#
#         while (response.status_code == 200) :
#             body = response.json()
#
#             # loop until the job is done
#             status = body['status']
#             if (status == 'success' or status == 'failure') :
#                 break
#
#             time.sleep(20)
#             response = requests.get(url, headers=headers)

# def waitOnAstrometryJobDone(submissionId) :
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     url = submit_status_url+str(submissionId)
#     response = requests.get(url, headers=headers)
#
#     while (response.status_code == 200) :
#         body = response.json()
#
#         # loop until the jobs have been created
#         jobs = body['jobs']
#         if (len(jobs) != 0 and jobs[0] != None):
#             waitOnAstrometryJobsSuccess(jobs)
#             break
#
#         time.sleep(20)
#         response = requests.get(url, headers=headers)
#
#     if (response.status_code != 200) :
#         print("request failed: "+url+", statuscode: "+str(response.status_code))
#         body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}
#
#     return body

# def waitOnAstrometrySubmissionDone(submissionId):
#
#     # TODO - should account for failure in this call
#     body = waitOnAstrometryJobDone(submissionId)
#
#     url = submit_status_url+str(submissionId)
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     response = requests.get(url, headers=headers)
#
#     if (response.status_code == 200) :
#         body = response.json()
#
#         # if the jobs are done, check for calibrations
#         job_calibrations = body['job_calibrations']
#
#         # if no calibrations, then we are done
#         if (len(job_calibrations) != 0 and job_calibrations[0] != None):
#             # job_calibrations is a list of lists, so loop over each one and then exit the loop
#             for calibrations in job_calibrations:
#                 body['job_calibrations'] = getAstrometryCalibrationResults(calibrations)
#                 # TODO - FIX if the array has more than one entry then we overwrite
#
#     if (response.status_code != 200) :
#         print("request failed: "+url+", statuscode: "+str(response.status_code))
#         body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}
#
#     return body


#won't work for JB image because have to split pics between invert and regular
# def newAstromertyUploadSettings(url, session):
#     settings = {
#         # session: string, requried. Your session key, required in all requests
#         "session" : session,
#
#         # url: string, required. The URL you want to submit to be solved
#         "url" : url,
#
#         "upload_type" : "url",
#
#         # allow_commercial_use: string: “d” (default), “y”, “n”: licensing terms
#         "allow_commercial_use" : 'd',
#
#         # allow_modifications: string: “d” (default), “y”, “n”, “sa” (share-alike): licensing terms
#         "allow_modifications" : 'd',
#
#         # publicly_visible: string: “y”, “n”
#         "publicly_visible" : 'n',
#
#         # scale_units: string: “degwidth” (default), “arcminwidth”, “arcsecperpix”. The units for the “scale_lower”
#         # and “scale_upper” arguments; becomes the “–scale-units” argument to “solve-field” on the server side.
#         "scale_units" : 'degwidth',
#
#         # scale_type: string, “ul” (default) or “ev”. Set “ul” if you are going to provide “scale_lower” and
#         # “scale_upper” arguments, or “ev” if you are going to provide “scale_est” (estimate) and “scale_err” (error
#         # percentage) arguments.
#         "scale_type" : 'ul', #bounds
#
#         # scale_lower: float. The lower-bound of the scale of the image
#         "scale_lower" :'0.1',
#
#         # scale_upper: float. The upper-bound of the scale of the image.
#         "scale_upper'" : '180.0',
#
#         # scale_est: float. The estimated scale of the image.
#         ##settings['scale_est'] = '',
#
#         # scale_err: float, 0 to 100. The error (percentage) on the estimated scale of the image.
#         ##settings['scale_err'] = '',
#
#         # center_ra: float, 0 to 360, in degrees. The position of the center of the image.
#         ##settings['center_ra'] = '',
#
#         # center_dec: float, -90 to 90, in degrees. The position of the center of the image.
#         ##settings['center_dec'] = '',
#
#         # radius: float, in degrees. Used with center_ra,‘‘center_dec‘‘ to specify that you know roughly where
#         # your image is on the sky.
#         ##settings['radius'] = '',
#
#         # downsample_factor: float, >1. Downsample (bin) your image by this factor before performing source
#         # detection. This often helps with saturated images, noisy images, and large images. 2 and 4 are commonlyuseful
#         # values.
#         "downsample_factor" : '2',
#
#         # tweak_order: int. Polynomial degree (order) for distortion correction. Default is 2. Higher orders may
#         # produce totally bogus results (high-order polynomials are strange beasts).
#         "tweak_order" : '2',
#
#         # use_sextractor: boolean. Use the SourceExtractor program to detect stars, not our built-in program
#         ##settings['use_sextractor'] = '',
#
#         # crpix_center: boolean. Set the WCS reference position to be the center pixel in the image? By default the
#         # center is the center of the quadrangle of stars used to identify the image.
#         # settings['crpix_center'] = '???',
#
#         # parity: int, 0, 1 or 2. Default 2 means “try both”. 0 means that the sign of the determinant of the WCS
#         # CD matrix is positive, 1 means negative. The short answer is, “try both and see which one works” if you are
#         # interested in using this option. It results in searching half as many matches so can be helpful speed-wise.
#         "parity" : '2',
#
#         # image_width: int, only necessary if you are submitting an “x,y list” of source positions.
#         ##settings['image_width'] = '',
#
#         # image_height: int, only necessary if you are submitting an “x,y list” of source positions.
#         ##settings['image_height'] = '',
#
#         # positional_error: float, expected error on the positions of stars in your image. Default is 1.
#         "positional_error" : 1
#     }
#
#     return settings
#

# def uploadImages(imageBucket) :
#     google_client = Client()
#     #google_client.deleteSheet("astrometry.net")
#     success_ws = google_client.openSheet("astrometry.net","success")
#     error_ws = google_client.openSheet("astrometry.net","error")
#     exit(0)
#     # login
#     loginSession = astrometryLogin(login_url, apikey)
#
#     # return file generator over S3 bucket
#     # client = boto3.client('s3')
#     files = listS3Files(imageBucket, 'pending/')
#
#     #s3 = boto3.resource('s3')
#     for file in files:
#
#         # initial file meta data as part of log data (where from, who from, original url, ...)
#         setPublicReadPermissions(file)
#         imageUrl = s3_bucket_url+'/'+file
#         submission = submitAstrometryUrl(imageUrl,loginSession)
#         (head, tail) = os.path.split(file)
#
#         if ('status' in submission) :
#
#             if (submission['status'] == 'success') :
#
#                 status = waitOnAstrometrySubmissionDone(submission['subid'])
#                 createLog(tail, status)
#                 #addSuccessToSheet(success_ws, s3_bucket_url+'/'+s3_imagebucket+'/archive/'+file, status)
#             if (archive_flag) :
#                 archiveImage(tail, s3_imagebucket)
#
#                 #addErrorToSheet(error_ws, s3_bucket_url+'/'+s3_imagebucket+'/archive/'+file, submission)
#         else :
#             createErrorLog(tail, submission)
#
