#!/usr/bin/python3

import argparse
import time
import NooLite_F
from NooLite_F.MTRF64.MTRF64Adapter import MTRF64Adapter, IncomingData, OutgoingData, Command, Mode, Action, ResponseCode, IncomingDataException
from NooLite_F.MTRF64.MTRF64Controller import MTRF64Controller


def on_receive_data(incoming_data: IncomingData):
    print("data: {0}".format(incoming_data))







parser = argparse.ArgumentParser(description='NooLite to MQTT bridge')
parser.add_argument('--serialport',
                    help='path to serial port (default /dev/noolite)',
                    default="/dev/noolite")
args = parser.parse_args()


serial_port = args.serialport

adapter = MTRF64Adapter(serial_port, on_receive_data)

while True:
    time.sleep(60)