from flask import Flask

app = Flask(__name__)
from app import views


app.config["CACHE_TYPE"] = "null"