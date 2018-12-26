import json
import configparser
from typing import Dict, Any, Union

import requests
import io
import os
import boto3
import botocore
import json

#log in to astrometry and return a session
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

#place holder to upload files to astrometry
def AstrometryFileUploadRequest(filename, url, session):
    request = {}
    with open(filename, mode = "rb") as file:
        filecontent = file.read()
    ### read section on POST a Multipart-Encoded File
    ### http://docs.python-requests.org/en/master/user/quickstart/

    # will need to find the docs for this API or reverse engineer the web app
    # sample code - https://github.com/dstndstn/astrometry.net/blob/master/net/client/client.py

    return request

#Gives a list of image files in s3 Bucket
def listS3Files(client, bucketName, prefix):
    #"""List files in specific S3 URL"""
    response = client.list_objects(Bucket=bucketName, Prefix=prefix)
    for content in response.get('Contents', []):
      yield content.get('Key')

#gives list of files on local dir
def listFiles(path):
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.jpg', '.jpeg', '.png', '.gif') ): # whatever file types you're using...
            filenames.append(filename)
    filenames.sort() # now you have the filenames and can do something with them
    return filenames

def createAstrometryImageUploadRequest(file, url, session):
    binary_stream = io.BytesIO()
    # Read all data from the buffer
    stream_data = binary_stream.read()

    request = {}
    #trying to figure out how to encode the file correctly to post to site
    ### read section on POST a Multipart-Encoded File
    ### http://docs.python-requests.org/en/master/user/quickstart/

    # will need to find the docs for this API or reverse engineer the web app
    # sample code - https://github.com/dstndstn/astrometry.net/blob/master/net/client/client.py


#won't work for JB image because have to split pics between invert and regular
def getAstromertyUploadSettings(url, session):
    settings = {}

    # session: string, requried. Your session key, required in all requests
    settings['session'] = session

    # url: string, required. The URL you want to submit to be solved
    settings['url'] = url
    settings['upload_type'] = 'url'

    # allow_commercial_use: string: “d” (default), “y”, “n”: licensing terms
    settings['allow_commercial_use'] = 'd'

    # allow_modifications: string: “d” (default), “y”, “n”, “sa” (share-alike): licensing terms
    settings['allow_modifications'] = 'd'

    # publicly_visible: string: “y”, “n”
    settings['publicly_visible'] = 'n'

    # scale_units: string: “degwidth” (default), “arcminwidth”, “arcsecperpix”. The units for the “scale_lower”
    # and “scale_upper” arguments; becomes the “–scale-units” argument to “solve-field” on the server side.
    settings['scale_units'] = 'degwidth'

    # scale_type: string, “ul” (default) or “ev”. Set “ul” if you are going to provide “scale_lower” and
    # “scale_upper” arguments, or “ev” if you are going to provide “scale_est” (estimate) and “scale_err” (error
    # percentage) arguments.
    settings['scale_type'] = 'ul' #bounds

    # TODO - determine appropriate values for the following
    # scale_lower: float. The lower-bound of the scale of the image
    settings['scale_lower'] = '0.1'

    # scale_upper: float. The upper-bound of the scale of the image.
    settings['scale_upper'] = '180.0'

    # scale_est: float. The estimated scale of the image.
    settings['scale_est'] = ''

    # scale_err: float, 0 to 100. The error (percentage) on the estimated scale of the image.
    settings['scale_err'] = ''

    # center_ra: float, 0 to 360, in degrees. The position of the center of the image.
    settings['center_ra'] = ''

    # center_dec: float, -90 to 90, in degrees. The position of the center of the image.
    settings['center_dec'] = ''

    # radius: float, in degrees. Used with center_ra,‘‘center_dec‘‘ to specify that you know roughly where
    # your image is on the sky.
    settings['radius'] = ''

    # downsample_factor: float, >1. Downsample (bin) your image by this factor before performing source
    # detection. This often helps with saturated images, noisy images, and large images. 2 and 4 are commonlyuseful
    # values.
    settings['downsample_factor'] = '2'

    # tweak_order: int. Polynomial degree (order) for distortion correction. Default is 2. Higher orders may
    # produce totally bogus results (high-order polynomials are strange beasts).
    settings['tweak_order'] = '2'

    # use_sextractor: boolean. Use the SourceExtractor program to detect stars, not our built-in program
    settings['use_sextractor'] = ''

    # crpix_center: boolean. Set the WCS reference position to be the center pixel in the image? By default the
    # center is the center of the quadrangle of stars used to identify the image.
    # settings['crpix_center'] = '???'

    # parity: int, 0, 1 or 2. Default 2 means “try both”. 0 means that the sign of the determinant of the WCS
    # CD matrix is positive, 1 means negative. The short answer is, “try both and see which one works” if you are
    # interested in using this option. It results in searching half as many matches so can be helpful speed-wise.
    settings['parity'] = '2'

    # image_width: int, only necessary if you are submitting an “x,y list” of source positions.
    settings['image_width'] = ''

    # image_height: int, only necessary if you are submitting an “x,y list” of source positions.
    settings['image_height'] = ''

    # positional_error: float, expected error on the positions of stars in your image. Default is 1.
    settings['positional_error'] = 1

    return settings

# read configuration and create statics
config = configparser.ConfigParser()
config.read('myconfig.ini')
apikey = config['nova.astrometry.net']['apikey']
base_url = config['nova.astrometry.net']['base_url']
login_path = config['nova.astrometry.net']['login_path']
url_upload_path = config['nova.astrometry.net']['url_upload_path']
login_url = base_url+login_path
upload_url = base_url+url_upload_path
image_dir= config['nova.astrometry.net']['image_dir']
s3_imagebucket = config['nova.astrometry.net']['s3_bucket']
s3_bucket_url = config['nova.astrometry.net']['s3_bucket_url']

# return file generator over S3 bucket
client = boto3.client('s3')
files = listS3Files(client, s3_imagebucket, '')

# login
loginSession = astrometryLogin(login_url, apikey)


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        ))


# iterate file generator
s3 = boto3.resource('s3')
for file in files:

    # put into a function that returns a subid
    try:
        s3.Bucket(s3_imagebucket).download_file(file, os.path.join(image_dir, os.path.basename(file)))
        imageUrl = s3_bucket_url+'/'+file
        headers = {'User-Agent': 'Mozilla/5.0'}
        settings = getAstromertyUploadSettings(imageUrl, loginSession)
        #settingsJson = json.dumps(settings)
        #req = requests.Request('POST',upload_url, headers=headers, json=settings)
        #prepared = req.prepare()
        #pretty_print_POST(req)

        payload={'request-json': settings}
        response = requests.post(upload_url, headers=headers, data=payload)


        if (response.status_code == 200 or response.status_code == 302) :
            uploadResponse = response.json()

            #check the response status
            body = json.load(response.text)
            status = body['status']

            if (status == 'success') :
                subid = body['subid']

            else :
                print("request failed: "+imageUrl+", statuscode: "+status)
        else:
            print("request failed: "+imageUrl+", statuscode: "+str(response.status_code))

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    # rite a function that takes a subid and gets submission status (GET)
    # sleep for 30 secs and and loop until all jobs are done (GET)

#    request = createAstrometryImageUploadRequest(filename, upload_url,loginSession)


# files = listFiles(image_dir)
# for filename in files:
#     # create request
#     print("filename: "+filename)
#     request = createAstrometryImageUploadRequest(file,upload_url,loginSession)

print(loginSession)