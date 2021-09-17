#EIA Production and Inventory
import json
import requests
import os

url_eia_production = os.environ.get('EIA_API_CRUDE_PROD')
url_eia_imports = os.environ.get('EIA_API_CRUDE_IMPORTS')
url_database = os.environ.get('LINK_CRUDE_PROD')
token = os.environ.get('PA_API_TOKEN')

#Retrieve crude production data from EIA website
url = url_eia_production
data_crude = requests.get(url)

#Retrieve crude net imports data from EIA website
url = url_eia_imports
source_imports = requests.get(url)

#Format data into useable json format
data_crude = json.loads(data_crude.text)
data_imports = json.loads(source_imports.text)

#Update the database if needed

#Get the most recent datapoint
print('EIA current production date: ', data_crude['series'][0]['data'][0][0])
print('EIA current production: ', data_crude['series'][0]['data'][0][1])
print('EIAcurrent imports date: ', data_imports['series'][0]['data'][0][0])
print('EIA current imports: ', data_imports['series'][0]['data'][0][1])

#Format date to look like that in database for easy comparison
year = data_crude['series'][0]['data'][0][0][:4]
month = data_crude['series'][0]['data'][0][0][4:6]
current_date = year + '-' + month

#Get the last datapoint from database
url = url_database
data = requests.get(url)
production = json.loads(data.text)
last_date = production[-1]['date']
print('Database last updated date: ', last_date)

#Update the database if current_date != last_date
if current_date == last_date:
    print('current_date:', current_date, 'is equal to last_date:', last_date, '- Database not updated')

else:
    headers = {'Authorization': token}

    payload = {
    'date': current_date,
    'oil_production': data_crude['series'][0]['data'][0][1],
    'oil_imports': data_imports['series'][0]['data'][0][1],
    }

    resp = requests.post(url, headers=headers, data=payload)
    print(resp)



