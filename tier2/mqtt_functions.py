mqtt_connect_codes = {0: "Connection successful",
1: "Connection refused - incorrect protocol version",
2: "Connection refused - invalid client identifier",
3: "Connection refused - server unavailable",
4: "Connection refused - bad username or password",
5: "Connection refused - not authorised"}

def log(lock, func, message):
    with lock:
        func(message)

def on_connect(client, userdata, flags, rc):
    print(f"rc is {rc}")
    logger = userdata["logger"]
    lock = userdata["lock"]
    name = userdata["name"]
    log_type = logger.info if rc == 0 else logger.critical
    log_message = f"Sensor {name} - {mqtt_connect_codes[rc]}"
    log(lock, log_type, log_message)

def on_disconnect(client, userdata, rc):
    logger = userdata["logger"]
    lock = userdata["lock"]
    name = userdata["name"]

    if (rc == 0):
        log(lock, logger.info, f"Sensor {name} disconnected normally")
    else:
        log(lock, logger.info, f"Sensor {name} disconnected abnormally with code {rc}")
