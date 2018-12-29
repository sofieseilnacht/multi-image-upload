import requests
import json
import time
import botocore
from astrometry.config import *

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
        response = requests.post(upload_url, headers=headers, data={'request-json': json.dumps(settings)})

        if (response.status_code == 200) :
            body = response.json()

        else:
            print("request failed: "+imageUrl+", statuscode: "+str(response.status_code))
            body = {"url" : imageUrl, "status" : "http error", "error_code" : str(response.status_code)}

    except botocore.exceptions.ClientError as e:
        body = {"url" : imageUrl, "status" : "client error", "error_code" : str(e.response['Error']['Code'])}

    return body

def getAstrometryCalibrationResults(jobs) :
    # TODO - iterate jobs and create a results array
    return 'TODO'

def waitOnAstrometrySubmissionDone(submissionId):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = submit_status_url+str(submissionId)
    response = requests.get(url, headers=headers)


    while (response.status_code == 200) :
        body = response.json()
        processing_finished = body['processing_finished']

        # loop until a processing finished timestamp is in the response
        if (processing_finished != 'None') :
            body['job_calibrations'] = getAstrometryCalibrationResults(body['job_calibrations'])
            break

        time.sleep(15)
        response = requests.get(url, headers=headers)

    if (response.status_code != 200) :
        print("request failed: "+url+", statuscode: "+str(response.status_code))
        body = {"url" : url, "status" : "http error", "error_code" : str(response.status_code)}

    return body

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
        "positional_error" : 1
    }

    return settings

