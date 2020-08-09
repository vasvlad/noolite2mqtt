#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import time
import paho.mqtt.client as mqtt
import argparse
from NooLite_F.MTRF64.MTRF64Adapter import MTRF64Adapter, \
                                           IncomingData, OutgoingData, \
                                           Command, Action, Mode

clientId = "Noolite2MqttClient"
topic = "/devices/noolite/"
counter = 0
nooliteFdevices = []


# Search NooliteF devices
def search_nooliteFdevices(adapter, array):
    array.clear()
    request = OutgoingData()
    request.action = Action.SEND_BROADCAST_COMMAND
    request.mode = Mode.TX_F
    request.command = Command.READ_STATE

    for i in range(0, 64):
        request.channel = i
        response = adapter.send(request)
        if (response[0].command == 130):
            nooliteFdevices.append(i)


# Read states of all NooliteF devices
def read_nooliteFdevices_states():
    request = OutgoingData()
    request.action = Action.SEND_BROADCAST_COMMAND
    request.mode = Mode.TX_F
    request.command = Command.READ_STATE
    while True:
        for channel in nooliteFdevices:
            request.channel = channel
            response = adapter.send(request)
            # TODO Make parse for Bright
            if response[0].data[2] & 0b0000001 == 1:
                client.publish(topic + "channel" +
                               str(channel) + "/state", "1")
            else:
                client.publish(topic + "channel" +
                               str(channel) + "/state", "0")
        time.sleep(60)


# The callback for when a PUBLISH message is received from the server.
def on_mqtt_message(client, userdata, msg):
    print(msg.topic)
    if topic + "channel" in msg.topic:
        if msg.topic.split("/")[4] == "on":
            channelId = int(msg.topic.split("/")[3][7:])
            request = OutgoingData()
            request.action = Action.SEND_COMMAND
            request.mode = Mode.TX_F
            request.channel = channelId
            if (int(msg.payload) == 1):
                request.command = Command.ON
            else:
                request.command = Command.OFF

            response = adapter.send(request)
            if channelId in nooliteFdevices:
                # TODO Make parse for Bright
                if response[0].data[2] & 0b0000001 == 1:
                    client.publish(topic + "channel" +
                                   str(channelId) + "/state", "1")
                else:
                    client.publish(topic + "channel" +
                                   str(channelId) + "/state", "0")


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


def on_receive_noolite_data(incoming_data: IncomingData):
    print("data: {0}".format(incoming_data))
    print("counter: {0}".format(counter))
    if incoming_data.command == Command.LOAD_PRESET:
        client.publish(topic + "channel" + str(incoming_data.channel) + "/" +
                       str(Command(int(incoming_data.command))).split(".")[1].lower(),  # noqa: E501
                       str(counter), 1)
    else:
        client.publish(topic + "channel" + str(incoming_data.channel) + "/" +
                       str(Command(int(incoming_data.command))).split(".")[1].lower(),  # noqa: E501
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

adapter = MTRF64Adapter(serial_port, on_receive_noolite_data)
client = mqtt.Client(clientId)
client.on_connect = on_mqtt_connect
client.on_message = on_mqtt_message
client.on_publish = on_mqtt_publish
client.connect("127.0.0.1", 1883, 60)

search_nooliteFdevices(adapter, nooliteFdevices)
# Run threading for read nooliteF devices_states every 60 secounds
t = threading.Thread(target=read_nooliteFdevices_states)
t.start()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
