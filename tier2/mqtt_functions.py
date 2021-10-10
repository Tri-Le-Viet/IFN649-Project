def mqtt_connect(client, username, password, ip, port):
    client.username_pw_set(username=username, password=password)
    client.connect(ip, port)
    # TODO: add on_connect handler
