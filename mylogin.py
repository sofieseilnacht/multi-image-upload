import json
import base64
# import urllib.request
import requests3
import sys

def getUrl(url):
    try:
        with urllib.request.urlopen(url) as response:
            html=response.read()
    except urllib.error.URLError as e:
        print(e.reason)
        raise
    return html

def myLogin(url):
    R = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": "xuwbkwswjjickoit"})})
    print(R.text)
    return R


myUrl = "https://google.com"
myHtml = myLogin(myUrl)
print(myHtml)