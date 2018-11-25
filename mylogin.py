import json
import configparser
import urllib.request
import requests


def myLogin(url, apikey):
    try:
        R = requests.post(url, data={'request-json': json.dumps({"apikey": apikey})})
        print(R.text)
    except requests.exceptions.RequestException as e:
        print(e.reason)
        raise(e)

    return R


config = configparser.ConfigParser()
config.read('myconfig.ini')
apikey = config['nova.astrometrics.net']['apikey']
login_url = config['nova.astrometrics.net']['login_url']

myHtml = myLogin(login_url, apikey)
print(myHtml)