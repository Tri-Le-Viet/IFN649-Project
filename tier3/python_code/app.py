from flask import *
import os
from dotenv import load_dotenv
import logging
import logging.config
import sqlalchemy

from data import *

load_dotenv()
try:
    stations = os.environ["STATIONS"].split(" ")
    numStations = len(stations)
    topics = os.environ["TOPICS"].split(" ")
    mqtt_port = os.environ["MQTT_PORT"]
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
#TODO: figure out how logging for gunicorn works

update = threading.Event()
engine = sqlalchemy.create_engine(f"mysql+pymysql://{db_username}:{db_password}@localhost:3306/weather") #TODO: change database name
conn = engine.connect()

latest_data = {}
for station in stations:
    latest_data[station] = {}
    mqtt_thread = threading.Thread(target=collect_data, args=(latest_data, update, engine, topics, mqtt_port, lock, logger, username, password, station))
    mqtt_thread.start()


#TODO: check to see if we can move these to a separate file
@app.route("/")
def home():
    return render_template("index.html") # note: can pass data by adding args data=data

@app.route("/view")
def view():
    station = request.args.get("station")
    if not station or station not in stations:
        return abort(404)

    return render_template("view.html", data=latest_data[station])

@app.route("/history")
def history():
    station = request.args.get("station")
    if not station or station not in stations:
        return abort(404)

    query = text("SELECT * FROM stations WHERE station_name=:x")
    historical_data = conn.execute(query, x=station).fetchall()
    return render_template("history.html", data=historical_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
else:
    gunicorn_app = app
    #gunicorn -b 127.0.0.1:5000 app:gunicorn_app
