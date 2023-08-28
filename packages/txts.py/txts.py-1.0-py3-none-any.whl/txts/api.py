import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "txts.py/1.0 (txts-team/txts.py)"}

def handleCodes(StatusCode, Force=False):
    """[Handles HTTP Status Codes]

    Args:
        StatusCode ([int]): [Status code provided by the server],
        Force ([bool]): [Always return status code]

    Raises:
        ConnectionRefusedError: [Raised when anything but a status code of 200 is given]
    """

    if StatusCode == 200 and Force == False:
        return 
    else:
        Codes = {
            "200": "OK",
            "400": "Bad request",
            "401": "API Key Error",
            "403": "Forbidden; Access denied",
            "404": "Not Found",
            "412": "Precondition failed",
            "420": "Invalid Record; Record could not be saved",
            "421": "User Throttled; User is throttled, try again later",
            "422": "Locked; The resource is locked and cannot be modified",
            "423": "Already Exists; Resource already exists",
            "424": "Invalid Parameters; The given parameters were invalid",
            "500": "Internal Server Error; Some unknown error occurred on the server",
            "502": "Bad Gateway; A gateway server received an invalid response",
            "503": "Service Unavailable; Server cannot currently handle the request or you have exceeded the request rate limit. Try again later or decrease your rate of requests.",
            "520": "Unknown Error; Unexpected server response which violates protocol",
            "522": "Origin Connection Time-out; CloudFlare's attempt to connect timed out",
            "524": "Origin Connection Time-out; A connection was established between CloudFlare and the server, but it timed out before an HTTP response was received",
            "525": "SSL Handshake Failed; The SSL handshake between CloudFlare and the server failed"}
        if Force == True:
            status = f'{str(StatusCode)} {Codes[str(StatusCode)]}'
            return status
        try:
            raise ConnectionRefusedError(
                "Server returned the following HTTP status code: " + str(StatusCode) + " " + Codes[str(StatusCode)])
        except KeyError:
            raise ConnectionRefusedError(
                "Server returned the following HTTP status code: " + str(StatusCode) + " Unknown status code")

def TokenSeshHandler(url):
    sesh = requests.Session()
    get = sesh.get(url)
    token = BeautifulSoup(get.text, 'html.parser').find('input',
                     {'name':'__RequestVerificationToken'})['value']
    return token, sesh

class TxtInstance:

    def __init__(self, url):
        self.url = url.rstrip('/')
        print(url)
    
    def Status(self):
        Rerequest = requests.get(
                
                self.url, headers=headers)
        return handleCodes(Rerequest.status_code, Force=True)
    
    def EditPage(self, username, secret, content):
        complete_url = (f'{self.url}/@{username}/edit')
        try:
            token, sesh = TokenSeshHandler(complete_url)
        except:
            raise Exception(
                'Failed to get __RequestVerificationToken')
        payload = {'__RequestVerificationToken': token, 
           'content': content,
            'secret': secret}
        try:
            poster = sesh.post(complete_url, data=payload, headers=headers)
            soup = BeautifulSoup(poster.text, 'html.parser')
        except:
            raise Exception(
                'Failed to send request')
        if 'edited successfully' in (soup):
            return
        elif 'Invalid page secret' in (soup): 
            raise Exception(
                'Invalid page secret')
        else:
            raise ConnectionRefusedError(
            'Request was refused by server, \'content\' may be invalid')