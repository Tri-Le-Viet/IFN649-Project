from flask import *
import os
from dotenv import load_dotenv
import logging
import logging.config
import sqlalchemy

from data import *

load_dotenv()
try:
    station_names = os.environ["STATIONS"].split(" ")
    for name in range(len(station_names)):
        stations[name] = station_names[name].replace('_', ' ')
    numStations = len(station_names)
    topics = os.environ["TOPICS"].split(" ")
    hostname = os.environ["MQTT_HOST"]
    mqtt_port = int(os.environ["MQTT_PORT"])
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

update = threading.Event()
engine = sqlalchemy.create_engine(f"mysql+pymysql://{db_username}:{db_password}@localhost:3306/weather")
conn = engine.connect()

latest_data = {}
for station in stations:
    latest_data[station] = {}
    mqtt_thread = threading.Thread(target=collect_data, args=(latest_data, update, engine, topics, hostname, mqtt_port, lock, logger, username, password, station))
    mqtt_thread.start()


@app.route("/")
def home():
    return render_template("index.html", stations=stations)

@app.route("/view")
def view():
    station = request.args.get("station")
    station = station.replace('_', " ")
    if not station or station not in stations:
        return abort(404)

    convertedData = {}
    for key in data:
        convertedData[key] = str(data[key])

    return render_template("view.html", data=latest_data[station], name=station)

@app.route("/data")

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
