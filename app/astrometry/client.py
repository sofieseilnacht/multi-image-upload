import requests
import json
import time
import botocore

from app.astrometry.config import *

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

#log in to astrometry and return a session
def astrometryLogin():
    try:
        R = requests.post(login_url, data={'request-json': json.dumps({"apikey": apikey})})
        print(R.text)
        if (R.status_code == 200):
            responseJson = R.json()
            return responseJson["session"]
    except requests.exceptions.RequestException as e:
        print(e)
        raise(e)

    return None


def submitAstrometryUrl(imageUrl, loginSession):
    headers = {'User-Agent': 'Mozilla/5.0'}
    settings = newAstromertyUploadSettings(imageUrl, loginSession)

    try:
        print('submitAstrometryUrl: '+imageUrl)
        response = requests.post(upload_url, headers=headers, data={'request-json': json.dumps(settings)})

        if (response.status_code == 200) :
            body = response.json()

        else:
            print("request failed: "+imageUrl+", statuscode: "+str(response.status_code))
            body = {"url" : imageUrl, "status" : "http error", "error_code" : str(response.status_code)}

    except botocore.exceptions.ClientError as e:
        print("request failed: "+upload_url+", error_code: "+ str(e.response['Error']['Code']))
        body = {"url" : imageUrl, "status" : "client error", "error_code" : str(e.response['Error']['Code'])}

    return body

# def getAstrometryCalibrationResults(job_ids) :
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     calibrations = {}
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
#         calibrations[job_id ] = body
#
#     return calibrations

def getJobInfo(job_id) :
    headers = {'User-Agent': 'Mozilla/5.0'}
    job_url = base_url+'/jobs/'+str(job_id)+'/info/'

    try:
        response = requests.get(job_url, headers=headers)

        if response.status_code == requests.codes.ok:
            body = response.json()
        else:
            print("request failed: "+job_url+", statuscode: "+str(response.status_code))
            body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(response.status_code)}

    #TODO - think about letting exception to reach top most error handler
    except requests.exceptions.RequestException as e:
        print("request failed: "+job_url+", statuscode: "+str(response.status_code))
        body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(e.response['Error']['Code'])}

    return body

def getCalibrationsFitsFiles(calibration_ids) :
    fitsFiles = {}

    # if no work to do, then return
    if len(calibration_ids) == 0 or calibration_ids[0] == None :
        return fitsFiles

    # iterate over the (job_id, calibration_id) tuples
    for calibration_pair in calibration_ids:
        job_id = calibration_pair[0]
        calibration_id = calibration_pair[1]

        fitsFiles[job_id] = getCalibrationsFitsFile(job_id)

        # EXPERIMENT - with job info
        # job_info = getJobInfo(job_id)

    return fitsFiles

def getCalibrationsFitsFile(job_id) :
    headers = {'User-Agent': 'Mozilla/5.0'}

    #http://nova.astrometry.net/new_fits_file/JOBID
    job_url = base_url+'/new_fits_file/'+str(job_id)
    try:
        response = requests.get(job_url, headers=headers)

        if response.status_code == requests.codes.ok:
            body = response.content
        else:
            print("request failed: "+job_url+", statuscode: "+str(response.status_code))
            body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(response.status_code)}

    except requests.exceptions.RequestException as e:
        print("request failed: "+job_url+", statuscode: "+str(response.status_code))
        body = {"url" : job_url, "jobid" : job_id, "status" : "http error", "error_code" : str(e.response['Error']['Code'])}

    return body

def waitOnAstrometryJobsSuccess(job_ids):
    headers = {'User-Agent': 'Mozilla/5.0'}

    for job_id in job_ids:
        url = job_status_url+str(job_id)
        response = requests.get(url, headers=headers)

        print("waitOnAstrometryJobsSuccess: "+str(job_id)+' ', end='')
        while (response.status_code == 200) :
            body = response.json()

            # loop until the job is done
            status = body['status']
            if (status == 'success' or status == 'failure') :
                break

            print('.', end='', flush=True)
            time.sleep(15)
            response = requests.get(url, headers=headers)
        print(' done')
# def waitOnAstronomyJob(submissionId) :
#     #
#     body = waitOnAstrometryJobDone(submissionId)
#     waitOnAstrometryJobsSuccess(body['jobs'])
#     return body

def waitOnAstrometryJobDone(submissionId) :
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = submit_status_url+str(submissionId)
    response = requests.get(url, headers=headers)

    print('waitOnAstrometryJobDone: ' + str(submissionId)+ ' ', end='')
    done = False

    while (not done) :
        body = response.json()

        # loop until the jobs have been created or communication failure
        jobs = body['jobs']
        if (len(jobs) != 0 and jobs[0] != None):
            done = True
            break
        elif (response.status_code != 200):
            done = True
            break

        print('.', end='', flush=True)
        time.sleep(15)
        response = requests.get(url, headers=headers)

    if (response.status_code != 200) :
        print("request failed: "+url+", statuscode: "+str(response.status_code))
        body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}

    print(' done')
    return body

def getJobCalibration(job_id):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = base_url+'/api/jobs/'+str(job_id)+'/calibration/'

    print("getJobCalibration: "+str(job_id), end='')
    response = requests.get(url, headers=headers)

    while (response.status_code != 200) :
        print('.', end='', flush=True)
        time.sleep(15)
        response = requests.get(url, headers=headers)

    if (response.status_code != 200) :
        print("request failed: "+url+", statuscode: "+str(response.status_code))
        body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}
    else:
        body = response.json()

    print(' done')
    return body


def getJobCalibrations(job_ids):
    calibrations = {}
    # iterate over the (job_id, calibration_id) tuples
    for job_id in job_ids:

        calibrations[job_id] = getJobCalibration(job_id)

    return calibrations

def waitOnAstrometrySubmissionDone(submissionId):

    # wait until the submission has created and run a job
    body = waitOnAstrometryJobDone(submissionId)
    waitOnAstrometryJobsSuccess(body['jobs'])
    # refresh job data
    body = waitOnAstrometryJobDone(submissionId)
    body['calibration_results'] = getJobCalibrations(body['jobs'])
    fits = getCalibrationsFitsFiles(body['job_calibrations'])

    # url = submit_status_url+str(submissionId)
    # print('waitOnAstrometrySubmissionDone: '+url)
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(url, headers=headers)
    #
    # if (response.status_code == 200) :
    #     body = response.json()
    #
    #     # if the jobs are done, check for calibrations
    #     job_calibrations = body['job_calibrations']
    #
    #     # if no calibrations, then we are done
    #     if (len(job_calibrations) != 0 and job_calibrations[0] != None):
    #         for calibration_pair in job_calibrations :
    #             job_id = calibration_pair[0]
    #             calibration_id = calibration_pair[1]
    #             #body['job_calibrations'] = getAstrometryCalibrationResults(job_id)
    #             fits_results[job_id] = getCalibrationsFitsFile(job_id)
    # if (response.status_code != 200) :
    #     print("request failed: "+url+", statuscode: "+str(response.status_code))
    #     body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}

    return {'body':body,'fits':fits}

# def waitOnAstrometrySubmissionDoneOld(submissionId):
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     url = submit_status_url+str(submissionId)
#     response = requests.get(url, headers=headers)
#
#
#     while (response.status_code == 200) :
#         body = response.json()
#         processing_finished = body['processing_finished']
#         jobs = body[jobs]
#         # loop until a processing finished timestamp is in the response
#         if (processing_finished != 'None') :
#             body['job_calibrations'] = getAstrometryCalibrationResults(body['job_calibrations'])
#             break
#
#         time.sleep(15)
#         response = requests.get(url, headers=headers)
#
#     if (response.status_code != 200) :
#         print("request failed: "+url+", statuscode: "+str(response.status_code))
#         body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}
#
#     return body

#won't work for JB image because have to split pics between invert and regular
def newAstromertyUploadSettings(url, session):
    settings = {
        # session: string, requried. Your session key, required in all requests
        "session" : session,

        # url: string, required. The URL you want to submit to be solved
        "url" : url,

        "upload_type" : "url",

        # allow_commercial_use: string: “d” (default), “y”, “n”: licensing terms
        "allow_commercial_use" : 'd',

        # allow_modifications: string: “d” (default), “y”, “n”, “sa” (share-alike): licensing terms
        "allow_modifications" : 'd',

        # publicly_visible: string: “y”, “n”
        "publicly_visible" : 'n',

        # scale_units: string: “degwidth” (default), “arcminwidth”, “arcsecperpix”. The units for the “scale_lower”
        # and “scale_upper” arguments; becomes the “–scale-units” argument to “solve-field” on the server side.
        "scale_units" : 'degwidth',

        # scale_type: string, “ul” (default) or “ev”. Set “ul” if you are going to provide “scale_lower” and
        # “scale_upper” arguments, or “ev” if you are going to provide “scale_est” (estimate) and “scale_err” (error
        # percentage) arguments.
        "scale_type" : 'ul', #bounds

        # scale_lower: float. The lower-bound of the scale of the image
        "scale_lower" :'0.1',

        # scale_upper: float. The upper-bound of the scale of the image.
        "scale_upper'" : '180.0',

        # scale_est: float. The estimated scale of the image.
        ##settings['scale_est'] = '',

        # scale_err: float, 0 to 100. The error (percentage) on the estimated scale of the image.
        ##settings['scale_err'] = '',

        # center_ra: float, 0 to 360, in degrees. The position of the center of the image.
        ##settings['center_ra'] = '',

        # center_dec: float, -90 to 90, in degrees. The position of the center of the image.
        ##settings['center_dec'] = '',

        # radius: float, in degrees. Used with center_ra,‘‘center_dec‘‘ to specify that you know roughly where
        # your image is on the sky.
        ##settings['radius'] = '',

        # downsample_factor: float, >1. Downsample (bin) your image by this factor before performing source
        # detection. This often helps with saturated images, noisy images, and large images. 2 and 4 are commonlyuseful
        # values.
        "downsample_factor" : '2',

        # tweak_order: int. Polynomial degree (order) for distortion correction. Default is 2. Higher orders may
        # produce totally bogus results (high-order polynomials are strange beasts).
        "tweak_order" : '2',

        # use_sextractor: boolean. Use the SourceExtractor program to detect stars, not our built-in program
        ##settings['use_sextractor'] = '',

        # crpix_center: boolean. Set the WCS reference position to be the center pixel in the image? By default the
        # center is the center of the quadrangle of stars used to identify the image.
        # settings['crpix_center'] = '???',

        # parity: int, 0, 1 or 2. Default 2 means “try both”. 0 means that the sign of the determinant of the WCS
        # CD matrix is positive, 1 means negative. The short answer is, “try both and see which one works” if you are
        # interested in using this option. It results in searching half as many matches so can be helpful speed-wise.
        "parity" : '2',

        # image_width: int, only necessary if you are submitting an “x,y list” of source positions.
        ##settings['image_width'] = '',

        # image_height: int, only necessary if you are submitting an “x,y list” of source positions.
        ##settings['image_height'] = '',

        # positional_error: float, expected error on the positions of stars in your image. Default is 1.
        "positional_error" : 1,

        # invert : 'on' or 'off' to invert image for solution
        "invert" : 'off'
    }

    return settings

