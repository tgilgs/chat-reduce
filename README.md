# Recap: Cisco Spark Web Application

Summarise your Spark chatroom conversations into visual wordclouds separated into key topics: 

![wordcloud](webserver/static/wordclouds.jpg)


## Instructions to get started:

Install python package for virtual environments

```
pip install virtualenv
```

Start a virtual environment

```
virtualenv -p python3 venv
```

activate virtual environment:

```
source venv/bin/activate
```

- you are now working within the virtual environment

Install packages to the virtual environment:

```
pip install flask Pillow wordcloud nltk numpy scipy sklearn
```

For nltk, you also need to run dependencies.py to download the models.

Once everything is installed, cd into webserver and:

```
source credentials.sh
```
Then just run ```python recap_v1.2.py``` from terminal and access the page through ```localhost:8080``` in your browser. Sign in to your Spark account and get started!

Extra notes:
- to fix an error with python not installed as a backend on OS X go ```cd ./venv/lib/python3.5/site-packages/matplotlib/mpl-data/``` inside the virtual environment and add ```backend: TkAgg``` to the "matplotlib.rc" file

- the browser caches the old images so use incognito mode and you may need to reopen to refresh new images. This will be fixed once I figure out how to deliver images directly to flask


## Contributors:
Adrian C.
Aydan G.
Thomas G.
