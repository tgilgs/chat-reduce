from flask import Flask, render_template, request, session, url_for, redirect, abort, json

import requests
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

# Required Parameters: - Access Code  - Client ID  - Client secret
# Output: - A JSON object containing a valid access token
def getAccessToken(code):
    url = "https://api.ciscospark.com/v1/access_token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': 'http://localhost:8080/oauth'
    }
    accessData = requests.post(url, data)
    return accessData.json()

# Required Data: - Access Token
# Output: - An array of all rooms
def listRooms():
    url = "https://api.ciscospark.com/v1/rooms"
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    roomData = (requests.get(url, headers=headers)).json()

    rooms = []
    rooms.append([item["title"] for item in roomData["items"]])
    return rooms

# Required Parameters: - Access Token
# Output: - A JSON object containing the user's Cisco Spark details
def getUserProfile():
    url = "https://api.ciscospark.com/v1/people/me"
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    userDetails = requests.get(url, headers=headers)
    return userDetails.json()

# 'Main' page with a list of all the rooms the user is part of
@app.route('/main')
def main():
    rooms = listRooms()

    # with open('roomList.txt', 'w') as f:
    #     for room in rooms:
    #         f.write("%s\n" %room)

    # with open('rooms.txt', 'w') as f:
    #         json.dump(rooms,f, ensure_ascii = False)

    userDetails = getUserProfile()
    session['displayName'] = userDetails['displayName']

    return render_template("main.html", key = session['displayName'])

# 'Authorised' page which redirects the user if the login was valid
@app.route('/oauth')
def oauth():
    code = request.args.get("code")

    data = getAccessToken(code)
    session['access_token'] = data['access_token']

    return render_template("authorise.html")

# Redirect to authorisation URL (Cisco Spark login & Authorisation) using a 'GET' request
@app.route('/authorise', methods=['GET'])
def authorise():
    url = (
        "https://api.ciscospark.com/v1/authorize?"+
        "client_id=%s" %client_id+
        "&response_type=code"+
        "&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foauth"+
        "&scope=spark%3Aall%20spark-admin%3Aroles_read%20spark%3Akms%20spark-admin%3Aorganizations_read%20spark-admin%3Apeople_read"
    )
    return redirect(url, code=302)

@app.route('/')
def index():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)