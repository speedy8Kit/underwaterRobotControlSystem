import numpy as np

import lyb.address as address
import lyb.commandList as comList
import lyb.connector as connector
from listings.manager import manager, RedObject
from listings.ui.ssUi_btclickevents import SSUI_BtClickEvent


class RECEIVE_MSG_PROPELLER_CONTROL_SIGNAL(comList.MSG_PROPELLER_CONTROL_SIGNAL):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        socket.send_com(comList.MSG_NAVIG(*manager.pos,
                                          *manager.orientation,
                                          *manager.linear_velocity,
                                          *manager.angular_velocity),
                        address.addr_CS)
        manager.height = self.h
        if manager.worked:
            socket.send_com(comList.REQ_COUNT_PROPELLER_CONTROL_SIGNAL(), address.addr_CS)


class RECEIVE_MSG_NAVIG(comList.MSG_NAVIG):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        manager.setPos(*self.coordinates)
        manager.setOrientation(*self.euler_angles)
        manager.setAngularVelocity(*self.angular_velocity)
        manager.setLinearVelocity(*self.linear_velocity)
        if manager.worked:
            socket.send_com(comList.REQ_COUNT_NAVIG(), address.addr_NS)


class RECEIVE_MSG_PICTURE_PROCESSED(comList.MSG_PICTURE_PROCESSED):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        if manager.cam_worked:
            manager.sock.send_com(comList.REQ_PROCESS_PICTURE(), address.addr_DS)


class RECEIVE_EVENT_CONNECT(comList.EVENT_CONNECT):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        if senders.port == address.addr_M.port:
            manager.list_connection[0] = self.event
        elif senders.port == address.addr_CS.port:
            manager.list_connection[1] = self.event
        elif senders.port == address.addr_DS.port:
            manager.list_connection[2] = self.event
        elif senders.port == address.addr_NS.port:
            manager.list_connection[3] = self.event


class RECEIVE_SRV_GENERATE_PATH(comList.SRV_GENERATE_PATH):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        print("OK")


class RECEIVE_EVENT_OBJ(comList.EVENT_OBJ):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        is_new = True
        obj_new = RedObject(self.holst_pos[0], self.holst_pos[1], manager)
        for i in range(len(manager.list_red_objects)):
            obj = manager.list_red_objects[i]
            rad2 = (obj.pos[0] - obj_new.pos[0]) ** 2 + (obj.pos[1] - obj_new.pos[1]) ** 2
            if rad2 < 20:
                is_new = False
                if obj_new.norm < obj.norm:
                    manager.list_red_objects[i] = obj_new
                    for obj in manager.list_red_objects:
                        print(obj, " ", *obj.pos)
                break
        if is_new:
            manager.list_red_objects.append(obj_new)
            print("new point: ", obj_new.pos)


class RECEIVE_EVENT_END_POS(comList.EVENT_END_POS):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        SSUI_BtClickEvent.save()


def receive():
    RECEIVE_MSG_PROPELLER_CONTROL_SIGNAL()
    RECEIVE_MSG_NAVIG()
    RECEIVE_MSG_PICTURE_PROCESSED()
    RECEIVE_SRV_GENERATE_PATH()
    RECEIVE_EVENT_CONNECT()
    RECEIVE_EVENT_OBJ(0, 0)
