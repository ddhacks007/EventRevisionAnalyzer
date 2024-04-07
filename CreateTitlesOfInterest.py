import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def post(json_payload):
    url = f"http://{os.environ['host']}:{os.environ['port']}/event/schedule_title_fetch"

    json_data = json.dumps(json_payload)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
    else:
        print('Failed. Status code:', response.status_code)
        
if __name__ == '__main__':
    json_payload = {"titles": os.environ['titles'].split(",")}
    post(json_payload)
        