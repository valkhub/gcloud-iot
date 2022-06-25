#!/usr/bin/env python3

import os
import datetime
import ssl
import time
import jwt
#import json
import paho.mqtt.client as mqtt

payload = int(60)
connected = False
mqtt_bridge_hostname = "mqtt.googleapis.com"
mqtt_bridge_port = 443

def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=20),
        'aud': project_id,
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )
    return jwt.encode(token, private_key, algorithm=algorithm)


def on_connect(client, userdata, flags, rc):
    print("on_connect", mqtt.connack_string(rc))
    global connected
    connected = True


def on_publish(client, userdata, mid):
    print("on_publish")


def main():
    print("creating client " + os.environ['IOT_DEVICE_PATH'])
    client = mqtt.Client(client_id=os.environ['IOT_DEVICE_PATH'])
    client.username_pw_set(
        username='unused', password=create_jwt(os.environ['IOT_PROJECT_ID'], os.environ['IOT_DEVICE_KEY'], 'RS256')
    )
    client.tls_set(ca_certs=os.environ['IOT_DEVICE_CA'], tls_version=ssl.PROTOCOL_TLSv1_2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    broker_host, broker_port = os.environ['IOT_DEVICE_BROKER'].split(':')
    client.connect(broker_host, int(broker_port))

    mqtt_config_topic = "/devices/{}/config".format(os.environ['IOT_DEVICE_ID'])
    print("subscribing to " + mqtt_config_topic)
    client.subscribe(mqtt_config_topic, qos=1)

    mqtt_command_topic = "/devices/{}/commands/#".format(os.environ['IOT_DEVICE_ID'])
    print("subscribing to " + mqtt_command_topic)
    client.subscribe(mqtt_command_topic, qos=0)

    mqtt_topic = "/devices/{}/{}".format(os.environ['IOT_DEVICE_ID'])

    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)
    client.loop_start()
    print("loop start")
    while connected != True:
        time.sleep(0.3)
    client.publish(mqtt_topic, payload)
    client.loop_stop()


if __name__ == "__main__":
    main()
