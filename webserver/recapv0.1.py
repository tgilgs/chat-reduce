from flask import Flask, render_template, request, session, url_for, redirect, abort, json

import requests
import os
import wordcloud as wc
import re
from PIL import Image, ImageDraw
from io import BytesIO

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
# Output: - A dictionary containing the room names and their corresponding id
def listRooms():
    url = "https://api.ciscospark.com/v1/rooms"
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + session['access_token']
    }
    roomData = (requests.get(url, headers=headers)).json()

    #roomDict = {}
    roomArr = []
    for item in roomData["items"]:
        #roomDict[item["title"]] = item["id"]
        roomArr.append(item["title"])
    #print(roomArr[0])

    #only take the first 8 rooms to save space on nav bar
    roomArr=roomArr[:8]
    return roomArr

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



#Generate wordcloud
#@app.route('/<outputImgPath>')
#@app.route('/<imgDimensions>')
#@app.route('/<inputTextPath>')
def generate_wordcloud(outputImgPath, imgDimensions, inputTextPath):
    filepath = open(inputTextPath).read()
    
    wordcloud = wc.WordCloud(font_path = '/System/Library/Fonts/HelveticaNeue.dfont', 
        height = 400, width = 600, margin=2, background_color='white', 
        ranks_only=None, prefer_horizontal=.9, mask=None, scale=1, color_func=None,
        max_font_size=180, min_font_size=4, font_step=2, max_words=40, relative_scaling=0.3,
        regexp=None, collocations=True, random_state=None, mode="RGB",
        colormap=None, normalize_plurals=True)
    wordcloud.generate(filepath)
    image = wordcloud.to_image()

    image.save(outputImgPath, format='png')
    #with args.imagefile:
    #    out = args.imagefile if sys.version < '3' else args.imagefile.buffer
    #    image.save(outputImgPath, format='png')
    filepath = re.sub(r'app/', '', outputImgPath)
    return(filepath)



# 'Main' page with a list of all the rooms the user is part of
@app.route('/main')
def main():


    # rooms = roomDict.keys()
    # roomDict.get(<room name>, <default value>)

    # with open('roomList.txt', 'w') as f:
    #     for room in rooms:
    #         f.write("%s\n" %room)

    # with open('rooms.txt', 'w') as f:
    #         json.dump(rooms,f, ensure_ascii = False)

    displayName = session.get("displayName", False)
    if not displayName:
        return redirect(url_for('index'), code=302)

    rooms = listRooms()

    #generate wordclouds
    path = generate_wordcloud('static/wordcloudimage.png', 'test', '../app/static/files/a_new_hope.txt')
    path2 = generate_wordcloud('static/wordcloudimage2.png', 'test', '../app/static/files/constitution.txt')
    path3 = generate_wordcloud('static/wordcloudimage3.png', 'test', '../app/static/files/constitution.txt')
    path4 = generate_wordcloud('static/wordcloudimage4.png', 'test', '../app/static/files/a_new_hope.txt')
    #####

    return render_template("main.html", key = displayName, rooms=rooms,
        imga=path,
        imgb=path2,
        imgc=path3,
        imgd=path4)



# 'Authorised' page which redirects the user if the login was valid
@app.route('/oauth')
def oauth():
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

@app.route('/')
def index():
    session.clear()
    print("hello 2")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
