# chat-reduce

Instructions to get started:

Install python package for virtual environments

pip install virtualenv

Start a virtual environment

virtualenv -p python3 venv

activate virtual environment:
source venv/bin/activate

- you are now working within the virtual environment

Install packages to the virtual environment:
pip install flask Pillow wordcloud nltk pandas numpy scipy sklearn

to fix an error with python not installed as a backend on OS X go cd ./venv/lib/python3.5/site-packages/matplotlib/mpl-data/ inside the virtual environment and add backend: TkAgg to the matplotlib.rc file

access page through localhost:5000/index in browser. NOTE the browser caches the old images so use incognito mode and you may need to reopen to refresh new images. This will be fixed once I figure out how to deliver images directly to flask
