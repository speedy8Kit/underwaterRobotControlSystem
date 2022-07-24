import time

import sim
import listings.detection_system as ds
from lyb import address, connector
import lyb.commandList as comList

fps = 10


class RECEIVE_CMD_CONNECT(comList.CMD_CONNECT):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        if ds.detection_system.clientID is not None:
            sim.simxFinish(0)
        ds.detection_system = ds.DetectionSystem()
        ds.detection_system.socket = socket
        ds.detection_system.clientID = sim.simxStart('127.0.0.1', address.sim_port_DS, True, True, 2000, 5)

        if ds.detection_system.clientID == -1:
            print("connect fail")
            socket.send_com(comList.EVENT_CONNECT(False), address.addr_M)
        else:
            ID = ds.detection_system.clientID
            res, ds.detection_system.camera = sim.simxGetObjectHandle(ID, "CAM", sim.simx_opmode_oneshot_wait)
            print(res)
            sim.simxGetVisionSensorImage(ID, ds.detection_system.camera, ds.detection_system.color,
                                         sim.simx_opmode_streaming)
            socket.send_com(comList.EVENT_CONNECT(True), address.addr_M)

            print("connect ok")


class RECEIVE_REQ_PROCESS_PICTURE(comList.REQ_PROCESS_PICTURE):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        print(self.name)
        time_frame = time.time()
        ds.processThePicture()
        delta_time = time_frame - time.time()

        if delta_time < 1 / fps:
            time.sleep(1 / fps - delta_time)

        ds.detection_system.socket.send_com(comList.MSG_PICTURE_PROCESSED(), address.addr_M)


def receive():
    RECEIVE_CMD_CONNECT()
    RECEIVE_REQ_PROCESS_PICTURE()
