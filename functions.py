import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import pytz

load_dotenv()

# Load env variables
user = os.environ.get('user')
password = os.environ.get('password')
workspaceId = os.environ.get('workspaceId')
modelId = os.environ.get('modelId')
processId = os.environ.get('processId')
fileId = os.environ.get('fileId')
timezone = os.environ.get('timezone')

def get_auth_token(user, password):
    url = 'https://auth.anaplan.com/token/authenticate'
    response = requests.request("POST", url, auth=(user, password))
    return response.json()['tokenInfo']['tokenValue']

anaplan_auth_token = get_auth_token(user, password)

headers = {
    'Authorization': f'AnaplanAuthToken {anaplan_auth_token}',
    'Content-Type': 'application/json'
}

timestamp = datetime.now(pytz.timezone(timezone)).strftime('%d/%m/%Y-%H:%M:%S')
textstring = f'LatestDateTime,{timestamp}'


def update_file():
    url = f'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/files/{fileId}'
    headers = {
        'Authorization': f'AnaplanAuthToken {anaplan_auth_token}',
        'Content-Type': 'application/octet-stream'
    }
    response = requests.request('PUT', url, data=textstring, headers=headers)
    return response


def run_process():
    url = f'https://api.anaplan.com/2/0/workspaces/{workspaceId}/models/{modelId}/processes/{processId}/tasks'
    payload = json.dumps({'localeName': 'en_US'})
    response = requests.request('POST', url, headers=headers, data=payload)
    return response


def logout():
    url = 'https://auth.anaplan.com/token/logout'
    response = requests.request("POST", url, headers=headers)
    return response


def update_time():
    update_file()
    run_process()
    logout()

