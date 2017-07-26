from flask import Flask, render_template, request, session, url_for, redirect, json

import requests
import os
import wordcloud as wc
import re
from PIL import Image, ImageDraw
from io import BytesIO
from extract_topics import cluster_topics

app = Flask(__name__)
app.secret_key = os.environ['secret_key']

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']


#######################################################################################

################################       Methods         ################################

#######################################################################################

def getAccessToken(code):
# POST request to get Access Token for Cisco Spark Integration:
#   Required Parameters: - Access Code  - Client ID  - Client secret
#   Output: - A JSON object containing a valid access token
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


def getUserProfile():
# GET request to get current user details on Cisco Spark:
#   Required Parameters: - Access Token
#   Output: - A JSON object containing the user's Cisco Spark details
    url = "https://api.ciscospark.com/v1/people/me"
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    userDetails = requests.get(url, headers=headers)
    return userDetails.json()


def listRooms():
# GET request to get all rooms that the user is a member of:
#   Required Data: - Access Token
#   Output: - A dictionary containing the room names and their corresponding id
    url = "https://api.ciscospark.com/v1/rooms"
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    roomData = (requests.get(url, headers=headers)).json()

    roomDict = {}
    for item in roomData["items"]:
        roomDict[item["title"]] = item["id"]
    return roomDict


def getMembers(roomId):
# GET request to get first 5 members in a specific room:
#   Required Data: - Room ID  - Access Token
#   Output: - A list containing 5 display names of its group members
    url = (
        "https://api.ciscospark.com/v1/memberships?roomId=%s" %roomId
    )
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    roomMembers = (requests.get(url, headers=headers)).json()

    members = []
    noOfMembers = len(roomMembers["items"])
    # Get the names of the first 5 members:
    for i in range(5):
        if i > (noOfMembers-1):
            break
        else:
            members.append(roomMembers["items"][i]["personDisplayName"])
    if noOfMembers > 5:
        members.append('+ %d member(s)' %(noOfMembers-5))
    return members


def getMessages(roomId):
# GET request to get all messages from a specific room:
#   Required Data: - Room ID  - Access Token
#   Output: - A JSON containing the messages of the corresponding room
    url = (
        "https://api.ciscospark.com/v1/messages?roomId=%s" %roomId+
        "&max=1000"
    )
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    roomMessages = requests.get(url, headers=headers)
    return roomMessages.json()


def generate_wordcloud(outputImgPath, inputText):
# Method to generate a wordcloud from a text file containing extracted messages about a specific topic:
#   Required Data: - Text file
#   Output: - Filepath to the generated word cloud
    wordcloud = wc.WordCloud(font_path = '/System/Library/Fonts/HelveticaNeue.dfont',
        height = 400, width = 600, margin=2, background_color='white',
        ranks_only=None, prefer_horizontal=.9, mask=None, scale=1, color_func=None,
        max_font_size=180, min_font_size=4, font_step=2, max_words=40, relative_scaling=0.3,
        regexp=None, collocations=True, random_state=None, mode="RGB",
        colormap=None, normalize_plurals=True)
    wordcloud.generate(inputText)
    image = wordcloud.to_image()
    image.save(outputImgPath, format="PNG")

    # Regular Expression method - search and replace pattern in output image path:
    filepath = re.sub(r'static/', '', outputImgPath)
    return(filepath)



#######################################################################################

##############################       URL Routing         ##############################

#######################################################################################


# Log-out route:
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Topic summary route:
@app.route('/chat/<roomName>/<topic>')
def topicMessages(roomName, topic):
    topicNumber = 'topic'+str(topic)
    topiclist = json.loads(open('clustered_topics.json').read())
    topicMessage = topiclist[topicNumber]["messages"]
    # Reverse the message list:
    topicMessage = topicMessage[::-1]

    return render_template("messages.html", name = session['displayName'], room = roomName, topic = ('Topic ' + str(topic)), topicMessage = topicMessage)


# List of Rooms route
@app.route('/chat/<roomName>')
def wordCloud(roomName):
    roomId = session['rooms_dict'].get(roomName)
    roomMessages = getMessages(roomId)

    with open ("room_messages.json", "w") as file1:
        json.dump(roomMessages, file1)

    processed_data = cluster_topics("room_messages.json")

    with open ("clustered_topics.json", "w") as file2:
        json.dump(processed_data, file2)

    #process JSON, extract topics
    jsonTopics = json.loads(open('clustered_topics.json').read())

    jsonTopicsStr = str(jsonTopics)

    #count number of topics
    matches = re.findall("('topic)\d+(':)", jsonTopicsStr)

    numTopics = len(matches)
    topics = [None] * numTopics
    msgs = [None] * numTopics

    #get messages from topics
    for i in range(0, numTopics):
        print(str(i))
        topicKey = 'topic' + str(i)
        topics[i] = jsonTopics[topicKey]
        msgs[i] = str(topics[i]['messages'])

    filenames = []
    #generate wordclouds
    for i in range(0, numTopics):
        filename = 'static/wordcloudimage' + str(i) + '.png'
        path = generate_wordcloud(filename, msgs[i])
        filenames.append(path)

    return render_template("wordClouds.html", room = roomName, name = session['displayName'], imageArr=filenames)


# User page with a list of all the rooms and its users:
@app.route('/main')
def main():
    displayName = session.get("displayName", False)
    if not displayName:
        return redirect(url_for('index'), code=302)

    roomSession = session.get("rooms_dict", False)
    if not roomSession:
        roomDict = listRooms()
        session['rooms_dict'] = roomDict

    roomDict = session['rooms_dict']
    rooms = list(roomDict.keys())

    participants = []
    for room in rooms[:6]:
        room_id = roomDict.get(room)
        participants.append(getMembers(room_id))

    return render_template("main.html", name = displayName, rooms = rooms[:6], members = participants)


# 'Authorised' page which redirects the user (if the login is valid):
@app.route('/oauth')
def oauth():
    # Get access code from URL:
    code = request.args.get("code")

    data = getAccessToken(code)
    session['access_token'] = data['access_token']

    userDetails = getUserProfile()
    session['displayName'] = userDetails['displayName']

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


# Front Page route:
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)