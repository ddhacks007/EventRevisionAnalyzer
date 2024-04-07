from datetime import datetime
import os
import json
import requests
import csv
from dotenv import load_dotenv

load_dotenv()

def post(json_payload):
    url = f"http://{os.environ['host']}:{os.environ['port']}/event/create"

    json_data = json.dumps(json_payload)

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)
    else:
        print('Failed. Status code:', response.status_code)

if __name__ == '__main__':
    with open(os.environ['event_data_path'], mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            json_payload = {}
            date_format = "%B %d, %Y"
            date_obj = datetime.strptime(row['Event date'], date_format).strftime("%m/%d/%Y")
            json_payload['date'] = date_obj
            json_payload['name'] = row['Event name']
            json_payload['description'] = row['Event description']
            json_payload['tags'] = ",".join([tag.strip() for tag in row['Tags'].split(',')])
            
            print(json_payload)
            post(json_payload)
            