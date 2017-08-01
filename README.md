# Recap: Cisco Spark Web Application

Summarise your Spark chatroom conversations into visual wordclouds separated into key topics: 

![wordcloud](webserver/static/wordclouds.jpg)


## Instructions to get started:

1. Install python package for virtual environments

```
pip install virtualenv
```

2. Start a virtual environment:

```
virtualenv -p python3 venv
```

3. Activate virtual environment:

```
source venv/bin/activate
```

You are now working within the virtual environment

4. Install packages to the virtual environment:

```
pip install flask Pillow wordcloud nltk numpy scipy sklearn requests
```

For nltk, you also need to run ```dependencies.py``` to download the models.

5. Once everything is installed, **cd** into ```webserver``` and:

```
source credentials.sh
```
6. Then just run ```python recap_v1.2.py``` from terminal and access the page through ```localhost:8080``` in your browser. Sign in to your Spark account and get started!

###### Extra notes:
- to fix an error with python not installed as a backend on OS X go ```cd ./venv/lib/python3.5/site-packages/matplotlib/mpl-data/``` inside the virtual environment and add ```backend: TkAgg``` to the "matplotlib.rc" file


## Contributors:
Adrian C.
Aydan G.
Thomas G.
