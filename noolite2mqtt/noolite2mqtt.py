import time
import NooLite_F
from NooLite_F.MTRF64.MTRF64Adapter import MTRF64Adapter, IncomingData, OutgoingData, Command, Mode, Action, ResponseCode, IncomingDataException
from NooLite_F.MTRF64.MTRF64Controller import MTRF64Controller


def on_receive_data(incoming_data: IncomingData):
    print("data: {0}".format(incoming_data))

adapter = MTRF64Adapter("/dev/noolite", on_receive_data)

while True:
    time.sleep(60)