from flask import Flask, render_template, redirect, request, url_for
import requests
import json
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def runHome():
    return render_template("index.html")
@app.route("/traffic/<location>")
def runCam(location):
    tripCheckAPI = "84f28457c50744ca849e401d3d48c371"
    camIDs = {"bend": "674", "sisters": "236", "redmond": "848", "salem": "792", "portland": "246", "madras": "760", "govtcamp": "203", "eugene": "541"}
    dmsIDs = {"bend": "", "sisters": "178"}
    #camID = camIDs["sisters"]
    camID = camIDs[location]
    #camID = "236"
    #dmsID = "178"
    dmsID = dmsIDs["sisters"]
    rwisStation = "10RW006"
    response = requests.get('https://api.odot.state.or.us/tripcheck/Cctv/Inventory?DeviceId='+camID+'&key='+tripCheckAPI)
    dmsStatus = requests.get('https://api.odot.state.or.us/tripcheck/Dms/Status?DeviceId='+dmsID+'&key='+tripCheckAPI)
    weather = requests.get('https://api.odot.state.or.us/tripcheck/v2/Rwis/Status?StationId='+rwisStation+'&key='+tripCheckAPI) 
    speed = None
    print(response.status_code)
    myJson = response.json()
    dmsJson = dmsStatus.json()
    weatherJson = weather.json
    myJsonD = json.dumps(myJson)
    myJsonL = json.loads(myJsonD)
    link = myJson['CCTVInventoryRequest'][0]['cctv-url']
    dms1 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line1']
    dms2 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line2']
    dms3 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase1Line3']
    dms4 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line1']
    dms5 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line2']
    dms6 = dmsJson['dmsItems'][0]['dmsCurrentMessage']['phase2Line3']

    #['organization-information']#
    return render_template("traffic.html", camLink = link, dms1 = dms1, dms2 = dms2, dms3 = dms3, dms4 = dms4, dms5 = dms5, dms6 = dms6, city = location)
@app.route("/confirm", methods=["GET", "POST"])
def getCity():
    if request.method == "POST":
        city = request.form["cityName"]
        return redirect(url_for("runCam", location = city))

if(__name__ == "__main__"):
    Flask.run(app, host="0.0.0.0", debug=True)