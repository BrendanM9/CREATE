from flask import Flask, render_template, redirect, request, url_for
import requests
import json
app = Flask(__name__)
def celsiusToFahrneheit(thisTemp):
    f = (thisTemp*9/5)
    f += 32
    f = f*100
    f = int(f)
    f = f/100
    f = str(f) + "˚F"
    return f
def mmToIn(thisPrecip):
    i = (thisPrecip*0.0393701)
    i = str(i) + " in"
    return i
def kphToMph(thisSpeed):
    m = (thisSpeed*0.621371)
    m = m * 100
    m = int(m)
    m = m /100
    m = str(m) + " MPH"
    return m
@app.route("/", methods=["GET", "POST"])
def runHome():
    return render_template("index.html")
@app.route("/traffic/<location>")
def runCam(location):
    tripCheckAPI = "84f28457c50744ca849e401d3d48c371"
    camIDs = {"bend": "674", "sisters": "236", "redmond": "848", "salem": "792", "portland": "246", "madras": "760", "govtcamp": "203", "eugene": "541"}
    cityNames = {"bend": "Bend", "sisters": "Sisters", "redmond": "Redmond", "salem": "Salem", "portland": "Portland", "madras": "Madras", "govtcamp": "Government Camp", "eugene": "Eugene"}
    dmsIDs = {"bend": "", "sisters": "178", "redmond": "", "salem": "", "portland": "524", "madras": "", "govtcamp": "185", "eugene": ""}
    weather = {"bend": "KS39", "sisters": "ODT02", "redmond": "KRDM", "salem": "KSLE", "portland": "KPDX", "madras": "KS33", "govtcamp": "ODT15", "eugene": "KEUG"}
    lat = {"bend": 44.059221, "sisters": 44.284, "redmond": 44.248, "salem": 44.931, "portland": 45.563, "madras": 44.659808, "govtcamp": 45.349, "eugene": 44.043999}
    long = {"bend": -121.25976, "sisters": -121.529, "redmond": -121.217, "salem": -122.978, "portland": -122.607, "madras": -121.167526, "govtcamp": -121.939, "eugene": -123.152}
    #camID = camIDs["sisters"]
    camID = camIDs[location]
    cityName = cityNames[location]
    thisLat = str(lat[location])
    thisLong = str(long[location])
    weatherStation = weather[location]
    #camID = "236"
    #dmsID = "178"
    dmsID = dmsIDs[location]
    rwisStation = "10RW006"
    response = requests.get('https://api.odot.state.or.us/tripcheck/Cctv/Inventory?DeviceId='+camID+'&key='+tripCheckAPI)
    dmsStatus = requests.get('https://api.odot.state.or.us/tripcheck/Dms/Status?DeviceId='+dmsID+'&key='+tripCheckAPI)
    weather = requests.get('https://api.odot.state.or.us/tripcheck/v2/Rwis/Status?StationId='+rwisStation+'&key='+tripCheckAPI) 
    points = requests.get('https://api.weather.gov/points/'+thisLat+'%2C'+thisLong)
    pointsJson = points.json()
    observationListLink = pointsJson['properties']['observationStations']
    observationsList = requests.get(observationListLink)
    observationsListJson = observationsList.json()
    observationLink = observationsListJson['features'][0]['id']
    observations = requests.get("https://api.weather.gov/stations/"+weatherStation+"/observations")
    observationsJson = observations.json()
    observationData = observationsJson['features'][0]['properties']
    desc = observationData['textDescription']
    desc = "Condition: "+ desc
    temp = observationData['temperature']['value']
    if(temp != None):
        temp = celsiusToFahrneheit(temp)
        temp = "Temperature: "+ temp
    else:
        temp = "Temperature:"
    dew = observationData['dewpoint']['value']
    if(dew != None):
        dew = celsiusToFahrneheit(dew)
        dew = "Dew Point: "+dew
    else:
        dew = "Dew Point:"
    if(observationData['precipitationLast3Hours']['value'] != None):
        precipitation = observationData['precipitationLast3Hours']['value']
        precipitation = mmToIn(precipitation)
        precipitation = "Preciptitation: "+str(precipitation)
    else:
        precipitation = "Precipitation: 0 in"
    if(observationData['windSpeed']['value'] != None):
        speed = observationData['windSpeed']['value']
        speed = kphToMph(speed)
    else:
        speed = "0 MPH"
    speed = str(speed)
    wind = "Wind Speed: "+ speed
    #wind = str(wind) + "MPH"
    speed = None
    print(response.status_code)
    myJson = response.json()
    dmsJson = dmsStatus.json()
    weatherJson = weather.json()
    myJsonD = json.dumps(myJson)
    myJsonL = json.loads(myJsonD)
    link = myJson['CCTVInventoryRequest'][0]['cctv-url']
    if(dmsID != ""):
        dms1 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line1']
        dms2 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line2']
        dms3 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line3']
        dms4 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line1']
        dms5 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line2']
        dms6 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line3']
    else:
        dms1 =""
        dms2 =""
        dms3 =""
        dms4=""
        dms5 =""
        dms6=""
    #['organization-information']#
    return render_template("traffic.html", camInfo = myJson, dmsInfo = dmsJson,  camLink = link, dms1 = dms1, dms2 = dms2, dms3 = dms3, dms4 = dms4, dms5 = dms5, dms6 = dms6, city = cityName, weatherInfo = observationData, desc = desc, temp = temp, dew = dew, precipitation = precipitation, wind = wind)
@app.route("/confirm", methods=["GET", "POST"])
def getCity():
    if request.method == "POST":
        city = request.form["cityName"]
        return redirect(url_for("runCam", location = city))

if(__name__ == "__main__"):
    Flask.run(app, host="0.0.0.0", debug=True)

    #'''weatherInfo = observationsJson,'''