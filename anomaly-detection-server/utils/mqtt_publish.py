#!/usr/bin/env python3

"""
This is a module that Edge Data.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

import paho.mqtt.client as mqtt
import config

TOPIC = 'ai/data'


def connect_mqtt(task_id) -> mqtt:
    """ connect mqtt """
    client_id = task_id
    client = mqtt.Client(client_id)
    client.connect(host=config.ADDRESS, port=config.PORT)
    return client


def public_message(context):
    """
    Main function to create the MQTT client and start the loop.
    """
    try:
        client = mqtt.Client()
        client.connect(config.ADDRESS, config.PORT, 60)
        client.loop_start()
        client = connect_mqtt(config.TASK_ID)
        client.publish(TOPIC, context)
        client.loop_stop()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    public_message()
