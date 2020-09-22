import requests
import json
import hashlib
import base64
import time
import hmac
from resouces.globals import *


def default_config():
    with open('config.json') as config:
        config = json.load(config)
    return config


def lm_put(resourcePath, data, config=default_config()):

    AccessId = config["AccessId"]
    AccessKey = config["AccessKey"]
    Company = config["Company"]

    # Request Info
    httpVerb = 'PUT'

    # Construct URL
    url = 'https://' + Company + '.logicmonitor.com/santaba/rest' + resourcePath

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate Request details
    requestVars = httpVerb + epoch + data + resourcePath

    # Construct signature
    new_hmac = hmac.new(AccessKey.encode(), msg=requestVars.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(new_hmac.encode())

    # Construct headers
    auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    # Make request
    response = requests.put(url, data=data, headers=headers)

    # Print status and body of response
    print(response.status_code)
    print(response.content)
