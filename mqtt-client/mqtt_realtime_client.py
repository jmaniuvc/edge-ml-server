#!/usr/bin/env python3

"""
This is a module that Edge Data.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

import os
import json
import requests
import paho.mqtt.client as mqtt
from utils.resources_handler import download_resources, validate_resources
import config
from dotenv import load_dotenv


load_dotenv()

# mqtt functions
def publish_message(topic, context):
    """ publish message """
    client = connect_mqtt(config.TASK_ID)
    client.publish(topic, context)
    print(f"{topic}: published")


def connect_mqtt(task_id) -> mqtt:
    """ connect mqtt """
    client_id = task_id
    client = mqtt.Client(client_id)
    client.connect(host=config.ADDRESS, port=config.PORT)
    return client


def on_connect(client, userdata, flags, rc):
    """
    Callback for server connection.
    """
    client.subscribe("edge/data")
    client.subscribe("ai/model")


def on_message(client, userdata, msg):
    """
    Callback function for message receipt.
    """
    msg.payload = json.loads(msg.payload.decode("utf-8").strip('"'))
    if msg.topic == 'edge/data':
        if validate_resources():
            url = os.getenv('GET_ANOMALY_DATA_URL')
            requests.post(url, json=msg.payload)
    if msg.topic == 'ai/model':
        print("???????????????")
        dev_id = msg.payload['DEVICE_ID']
        download_resources(dev_id)


def main():
    """
    Main function to create the MQTT client and start the loop.
    """
    while True:
        try:
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(config.ADDRESS, config.PORT, 60)
            client.loop_forever()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
