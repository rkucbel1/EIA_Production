#US Natural Gas Production
import json
import requests
import os

url_eia_production = os.environ.get('EIA_API_NG_PROD')
url_database = os.environ.get('LINK_NG_PROD')
token = os.environ.get('PA_API_TOKEN')

#Retrieve Natural Gas production data from EIA website
url = url_eia_production
source_NatGas = requests.get(url)

#Format data into useable json format
data_NatGas = json.loads(source_NatGas.text)

#Update database if needed

#format the date
year = data_NatGas['series'][0]['data'][0][0][:4]
month = data_NatGas['series'][0]['data'][0][0][4:6]
current_date = year + '-' + month

#Get the last datapoint from database
url = url_database
data = requests.get(url)
production = json.loads(data.text)
last_date = production[-1]['date']

#Update the database if current_date != last_date
if current_date == last_date:
    print('current_date:', current_date, 'is equal to last_date:', last_date, '- Database not updated')

else:
    headers = {'Authorization': token}

    payload = {
    'date': current_date,
    'ng_production': data_NatGas['series'][0]['data'][0][1],
    }

    resp = requests.post(url, headers=headers, data=payload)
    print(resp)



