import json
import configparser
import requests


def astrometryLogin(url, apikey):
    try:
        R = requests.post(url, data={'request-json': json.dumps({"apikey": apikey})})
        print(R.text)
        if (R.status_code == 200):
            responseJson = R.json()
            return responseJson["session"]
    except requests.exceptions.RequestException as e:
        print(e)
        raise(e)

    return None

def AstrometryFileUpload(url, session):
    request = {}

    ### read section on POST a Multipart-Encoded File
    ### http://docs.python-requests.org/en/master/user/quickstart/

    # will need to find the docs for this API or reverse engineer the web app
    # sample code - https://github.com/dstndstn/astrometry.net/blob/master/net/client/client.py

    return request

def createAstrometryUrlUploadRequest(url, session):
    request = {}

    # session: string, requried. Your session key, required in all requests
    request['session'] = session

    # url: string, required. The URL you want to submit to be solved
    request['url'] = url

    # allow_commercial_use: string: “d” (default), “y”, “n”: licensing terms
    request['allow_commercial_use'] = 'd'

    # allow_modifications: string: “d” (default), “y”, “n”, “sa” (share-alike): licensing terms
    request['allow_modifications'] = 'd'

    # publicly_visible: string: “y”, “n”
    request['publicly_visible'] = 'n'

    # scale_units: string: “degwidth” (default), “arcminwidth”, “arcsecperpix”. The units for the “scale_lower”
    # and “scale_upper” arguments; becomes the “–scale-units” argument to “solve-field” on the server side.
    request['scale_units'] = 'degwidth'

    # scale_type: string, “ul” (default) or “ev”. Set “ul” if you are going to provide “scale_lower” and
    # “scale_upper” arguments, or “ev” if you are going to provide “scale_est” (estimate) and “scale_err” (error
    # percentage) arguments.
    request['scale_type'] = 'ul'

    # TODO - determine appropriate values for the following
    # scale_lower: float. The lower-bound of the scale of the image
    request['scale_lower'] = '???'

    # scale_upper: float. The upper-bound of the scale of the image.
    request['scale_upper'] = '???'

    # scale_est: float. The estimated scale of the image.
    request['scale_est'] = '???'

    # scale_err: float, 0 to 100. The error (percentage) on the estimated scale of the image.
    request['scale_err'] = '???'

    # center_ra: float, 0 to 360, in degrees. The position of the center of the image.
    request['center_ra'] = '???'

    # center_dec: float, -90 to 90, in degrees. The position of the center of the image.
    request['center_dec'] = '???'

    # radius: float, in degrees. Used with center_ra,‘‘center_dec‘‘ to specify that you know roughly where
    # your image is on the sky.
    request['radius'] = '???'

    # downsample_factor: float, >1. Downsample (bin) your image by this factor before performing source
    # detection. This often helps with saturated images, noisy images, and large images. 2 and 4 are commonlyuseful
    # values.
    request['downsample_factor'] = '???'

    # tweak_order: int. Polynomial degree (order) for distortion correction. Default is 2. Higher orders may
    # produce totally bogus results (high-order polynomials are strange beasts).
    request['tweak_order'] = '???'

    # use_sextractor: boolean. Use the SourceExtractor program to detect stars, not our built-in program
    request['use_sextractor'] = '???'

    # crpix_center: boolean. Set the WCS reference position to be the center pixel in the image? By default the
    # center is the center of the quadrangle of stars used to identify the image.
    # request['crpix_center'] = '???'

    # parity: int, 0, 1 or 2. Default 2 means “try both”. 0 means that the sign of the determinant of the WCS
    # CD matrix is positive, 1 means negative. The short answer is, “try both and see which one works” if you are
    # interested in using this option. It results in searching half as many matches so can be helpful speed-wise.
    request['parity'] = '2'

    # image_width: int, only necessary if you are submitting an “x,y list” of source positions.
    request['image_width'] = '???'

    # image_height: int, only necessary if you are submitting an “x,y list” of source positions.
    request['image_height'] = '???'

    # positional_error: float, expected error on the positions of stars in your image. Default is 1.
    request['positional_error'] = 1

    return request

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')
apikey = config['nova.astrometrics.net']['apikey']
base_url = config['nova.astrometrics.net']['base_url']
login_path = config['nova.astrometrics.net']['login_path']
url_upload_path = config['nova.astrometrics.net']['upload_path']
login_url = base_url+login_path
upload_url = base_url+url_upload_path

# login
loginSession = astrometryLogin(login_url, apikey)

# create request
request = createAstrometryUrlUploadRequest(upload_url,loginSession)



print(loginSession)