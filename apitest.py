import requests
tripCheckAPI = "a036194717464c84a1d0d623a518ed57"
camID = "236"
response = requests.get('https://api.odot.state.or.us/tripcheck/Cctv/Inventory?DeviceId='+camID+'&key='+tripCheckAPI+'&type=application/json') 
print(response.status_code)
print(response)