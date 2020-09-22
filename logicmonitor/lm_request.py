import requests
import json
import hashlib
import base64
import time
import hmac

def default_config():
    with open('config.json') as config:
        config = json.load(config)
    return config


def lm_request(lm_resourcePath, lm_filter='', lm_fields='', lm_size='', lm_config=default_config()):

    AccessId = lm_config["AccessId"]
    AccessKey = lm_config["AccessKey"]
    Company = lm_config["Company"]

    # Request Info
    httpVerb = 'GET'
    data = ''

    # Construct URL
    url = 'https://' + Company + '.logicmonitor.com/santaba/rest' + lm_resourcePath + lm_filter + lm_fields + lm_size

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate Request details
    requestVars = httpVerb + epoch + data + lm_resourcePath

    # Construct signature
    new_hmac = hmac.new(AccessKey.encode(), msg=requestVars.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(new_hmac.encode())

    # Construct headers
    auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    # Make request
    response = requests.get(url, data=data, headers=headers)

    # Print status and body of response
    # print(response.status_code)

    json_data = json.loads(response.content)
    # pprint.pprint(json_data['data'])
    return json_data['data']
