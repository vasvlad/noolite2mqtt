#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import argparse
from NooLite_F.MTRF64.MTRF64Adapter import MTRF64Adapter, IncomingData, Command

clientId = "Noolite2MqttClient"
topic = "/devices/"
counter = 0


# The callback for when a PUBLISH message is received from the server.
def on_mqtt_message(client, userdata, msg):
    print(msg.topic)


# The callback for when the client receives a CONNACK response from the server.
def on_mqtt_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("hello/world")
    client.subscribe(topic + "#")


def on_mqtt_publish(mosq, obj, mid):
    global counter
    counter = mid
    print("mid: " + str(counter))


def on_receive_data(incoming_data: IncomingData):
    print("data: {0}".format(incoming_data))
    print("counter: {0}".format(counter))
    if incoming_data.command == Command.LOAD_PRESET:
        client.publish(topic + "channel" + str(incoming_data.channel) + "/" +
                       str(Command(int(incoming_data.command))).split(".")[1].lower(),
                       str(counter), 1)
    else:
        client.publish(topic + "channel" + str(incoming_data.channel) + "/" +
                       str(Command(int(incoming_data.command))).split(".")[1].lower(),
                       str(counter), 1)


parser = argparse.ArgumentParser(description='NooLite to MQTT bridge')
parser.add_argument('--serialport',
                    help='path to serial port (default /dev/noolite)',
                    default="/dev/noolite")
parser.add_argument('--topic',
                    help='subscribe topic (default /devices/noolite/)',
                    default="/devices/noolite/")

args = parser.parse_args()


serial_port = args.serialport
topic = args.topic

adapter = MTRF64Adapter(serial_port, on_receive_data)
client = mqtt.Client(clientId)
client.on_connect = on_mqtt_connect
client.on_message = on_mqtt_message
client.on_publish = on_mqtt_publish
client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
