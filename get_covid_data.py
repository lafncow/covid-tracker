import requests
import json
from datetime import datetime

def get_config():
    return {
        "state": "Washington",
        "county": "King County",
        "low": "Have fun!",
        "moderate": "Avoid crowds",
        "substantial": "Wear a mask",
        "high": "Avoid public spaces"
    }

def get_cases(state=None, county=None):

    params = {}

    if state:
        params['state_name'] = state

    if county:
        params['county_name'] = county

    # Request data from the CDC API
    r = requests.get('https://data.cdc.gov/resource/nra9-vzzn.json', params=params)
    
    # Save result to temp file
    with open("temp.txt", "w") as temp_file:
        temp_file.write(r.text)

    # Parse data to array of dicts
    res_data = json.loads(r.text)

    return res_data

def get_latest(dataset):
    date_format = "%Y-%m-%d"
    latest_date = datetime.strptime("2000-01-01", date_format)
    results = []

    # Scan through to find latest date
    for row in dataset:
        # parse date
        row_date = datetime.strptime(row['date'][0:10], date_format)

        # Compare
        if row_date > latest_date:
            latest_date = row_date

    for row in dataset:
        # parse date
        row_date = datetime.strptime(row['date'][0:10], date_format)
        
        if row_date == latest_date:
            # Collect rows that are of latest date
            results.append(row)

    return results

config = get_config()

cases_data = get_cases(config['state'], config['county'])

latest = get_latest(cases_data)

status = latest[0]['community_transmission_level']

print(f"{latest[0]['date'][0:10]} Status: {status} {config[status]} ({latest[0]['cases_per_100k_7_day_count']})")