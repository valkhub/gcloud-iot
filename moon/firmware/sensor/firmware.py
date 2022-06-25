#!/usr/bin/env python3

import os
import datetime
import ssl
import jwt
import paho.mqtt.client as mqtt


def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.now(tz=datetime.timezone.utc),
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=20),
        'aud': project_id,
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    return jwt.encode(token, private_key, algorithm=algorithm)


def on_connect(client, userdata, flags, rc):
    print("on_connect", mqtt.connack_string(rc))


def on_publish(client, userdata, mid):
    print("on_publish")


def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print(
        "Received message '{}' on topic '{}' with Qos {}".format(
            payload, message.topic, str(message.qos)
        )
    )


def main():
    print("creating client " + os.environ['IOT_DEVICE_PATH'])
    client = mqtt.Client(client_id=os.environ['IOT_DEVICE_PATH'])
    client.username_pw_set(
        username='unused', password=create_jwt(os.environ['IOT_PROJECT_ID'], os.environ['IOT_DEVICE_KEY'], 'RS256')
    )
    client.tls_set(ca_certs=os.environ['IOT_DEVICE_CA'], tls_version=ssl.PROTOCOL_TLSv1_2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    broker_host, broker_port = os.environ['IOT_DEVICE_BROKER'].split(':')
    client.connect(broker_host, int(broker_port))

    mqtt_config_topic = "/devices/{}/config".format(os.environ['IOT_DEVICE_ID'])
    print("subscribing to " + mqtt_config_topic)
    client.subscribe(mqtt_config_topic, qos=1)

    mqtt_command_topic = "/devices/{}/commands/#".format(os.environ['IOT_DEVICE_ID'])
    print("subscribing to " + mqtt_command_topic)
    client.subscribe(mqtt_command_topic, qos=0)

    client.loop_forever()


if __name__ == "__main__":
    main()
