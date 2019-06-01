# This Python script retrieves the last 24H Rain value from your Netatmo Rainmeter
# Register for an api on Netatmo Dev website
# Create a new virtual sensor on your Domoticz server


# Fill below variables with your netatmo username, password, and Weather Station MAC address
username = "YOUR_NETATMO_USERNAME"
password = "YOUR_NETATMO_PASSWORD"
device_id = "YOUR_WEATHER_STATION_MAC"

# Netatmo API Settings
client_id = "YOUR_NETATMO_API_CLIENT_ID"
client_secret = "YOUR_NETATMO_API_CLIENT_SECRET"

#Domoticz Settings - Fill variable belows with your domoticz credential, hostname and Vitual Sensor idx
user_domo = "YOUR_DOMOTICZ_USERNAME"
password_domo  = "YOUR_DOMOTICZ_PASSWORD"
domo_host = "YOUR_DOMOTICZ_SERVER_HOSTNAME"
vsensor_idx = "YOUR_VIRTUAL_SENSOR_IDX"



# End of configuration -  Do Not Change anything below
################################################################################
import requests

payload = {'grant_type': 'password',
           'username': username,
           'password': password,
           'client_id': client_id,
           'client_secret': client_secret,
           'scope': 'read_station'}
try:
    response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
    response.raise_for_status()
    access_token=response.json()["access_token"]
    refresh_token=response.json()["refresh_token"]
    scope=response.json()["scope"]
except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)
    quit()


params = {
    'access_token': access_token ,
    'device_id': device_id
}

try:
    response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
    response.raise_for_status()
    data = response.json()["body"]
except requests.exceptions.HTTPError as error:
    print(error.response.status_code, error.response.text)
    quit()


for i in data['devices'][0]['modules']:
    data_type = i['data_type']
    if "Rain" in data_type:
      print ("Rainmeter found! Getting Rain 24H value")
      rain24 = str(i['dashboard_data']['sum_rain_24'])
     # Updating Domoticz vSensor 
     # Send HTTP GET request to server and attempt to receive a response
      domo_url = 'http://' + user_domo + ':' +  password_domo +  '@' + domo_host + '/json.htm?type=command&param=udevice&idx=' +  vsensor_idx +  '&nvalue=0&svalue=' +  rain24
      response = requests.get(domo_url)
      # If the HTTP GET request can be served
      if response.status_code == 200:
        quit()
      else:
        print ("Error, review you settings. HTTP Error" + str(response.status_code))
        quit()
