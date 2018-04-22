from flask import Flask, request, session
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
import datetime
import json

app = Flask(__name__)

location1 = {
    "name": "New Port 1",
    "max" : 10,
    "current" : 5
}

location2 = {
    "name": "New Port 2",
    "max" : 5,
    "current" : 0
}

location3 = {
    "name" : "External Garage",
    "max" : 3,
    "current" : 0
}

locations = {
    1: location1,
    2: location2,
    3: location3
}

locationNameToId = {
    "New Port 1": 1,
    "New Port 2": 2,
    "External Garage": 3
}

reservations = {}

def help():
    return "You can text 'Assist', 'Status', or 'Reserve <Location_Name_Here>' to interact with the system. Assist gives you this message ;) Status will return the parking status of all parking garages. Reserve allows you to reserve a spot at the specified location."

def setReservation(personId, locationName):
    locationId = locationNameToId[locationName]
    location = locations[locationId]
    print "Made it here 1"
    if personId in reservations:
        return "You have already have a spot reserved in location " + reservations[personId]["location"]
    if location["current"] < location["max"]:
        locations[locationId]["current"] = locations[locationId]["current"] + 1
        reservations[personId] = { "location": locationName, "Expiration": datetime.datetime.now() }
        return "You have a spot reserved for " + locationName + ", for the next hour."
    return "This location is full. Please reply with 'Status' to see all location information."

def getStatus(location):
    return "Location Status: " + location["name"] + " is at " + str(location["current"])  + "/" + str(location["max"])  + " capacity."

def status():
    return getStatus(locations[1]) + "\n" + getStatus(locations[2]) + "\n" + getStatus(locations[3])

options = {
    'assist' : help,
    'reserve' : setReservation,
    'status' : status
}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/")
def home():
    return "sup dawg, you shouldn't be here right now D;"

@app.route("/status")
def httpStatus():
    return json.dumps(locations, indent=4, sort_keys=True)

@app.route("/text", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    messageFromRequest = request.args.get('Body')
    userId = request.args.get('From') #using phone numbers as user ids
    userId = userId[2:]
    print "messageFromRequest: " + messageFromRequest
    print "userId: " + userId
    requestOptions = messageFromRequest.split(" ", 1)
    actionFunction = requestOptions[0].lower()
    if (len(requestOptions) > 1) and actionFunction in options:
        resp.message(options[actionFunction](userId, requestOptions[1]))
    else:
        if actionFunction in options:
            resp.message(options[actionFunction]())
        else:
            resp.message(options["assist"]())
    return str(resp)

@app.route("/enter/peron_id/<person_id>/location_id/<location_id>",  methods=['GET', 'POST'])
def enterGarage(person_id, location_id):
    print person_id
    print location_id
    if person_id in reservations:
        print "This person had a reservarion"
        print "Person " + person_id + " had a reservation, marking them as arrived."
        del reservations[person_id]
    if locations[int(location_id)]["current"] == locations[int(location_id)]["max"]:
        print "Full"
        return "This location is full, please try another."
    locations[int(location_id)]["current"] = locations[int(location_id)]["current"] + 1
    return "Person ID: " + person_id + ", location ID: " + location_id

@app.route("/exit/<location_id>", methods=['POST'])
def exitGarage(location_id):
    locationId = int(location_id)
    if locations[int(location_id)]["current"] == 0:
        return "Location: " + locations[locationId]["name"] + " is at 0, cannot remove any more."
    locations[locationId]["current"] = locations[locationId]["current"] - 1
    return "Location: " + locations[locationId]["name"] + " now has " + str(locations[locationId]["current"]) + " remaining"

@app.route("/status/<location_id>", methods=['GET'])
def getLocationStatus(location_id):
    locationId = int(location_id)
    current = locations[locationId]["current"]
    max = locations[locationId]["max"]
    if current == max:
        return "At max capacity."
    return str(current) +"/"+str(max) + " Spaces Used."