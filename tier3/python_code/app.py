from flask import *
import os
from dotenv import load_dotenv
import logging
import logging.config
import threading #TODO: remove once imported in other file
import sqlalchemy

load_dotenv()
try:
    stations = os.environ["STATIONS"].split(" ")
    numStations = len(stations)
    topics = os.envrion["TOPICS"].split(" ")
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    db_username = os.environ["DB_USER"]
    db_password = os.environ["DB_PASS"]
except KeyError:
    print("Missing environment variables, check .env before running")
    exit()


app = Flask(__name__.split('.')[0])
lock = threading.Lock()
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")
engine = sqlalchemy.create_engine(f"mariadb+mariadbconnector://{db_username}:{db_password}!@127.0.0.1:3306/company") #TODO: change database name

@app.route("/")
def home():
    return render_template("index.html") # note: can pass data by adding args data=data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
else:
    gunicorn_app = app
    #gunicorn -b 0.0.0.0:8080 app:gunicorn_app
