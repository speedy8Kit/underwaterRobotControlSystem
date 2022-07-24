import socket
from typing import Tuple

import lyb.commandList as commandList
from lyb.commandList import Command
from lyb.address import Address


class MySocket(object):
    def __init__(self, address: Address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((address.ip, address.port))
        self.sock = sock

    def recv_com(self) -> Tuple[Command, Address]:
        data, addr = self.sock.recvfrom(128)
        address_senders = Address(*addr)
        byte_arr = bytearray(data)
        key = Command.unPackKey(byte_arr[0:4])
        command_typ = commandList.findACommand(key)
        com = command_typ(*command_typ.unPack(byte_arr[4:]))
        return com, address_senders

    def send_com(self, command: Command, address_recipient: Address):
        self.sock.sendto(command.pack(), (address_recipient.ip, address_recipient.port))

    def send(self, data: str, ip, port):
        self.sock.sendto(data.encode(), (ip, port))

    def recv(self, buf_size: int):
        return self.sock.recv(buf_size)

    def recvfrom(self, buf_size: int):
        return self.sock.recvfrom(buf_size)
