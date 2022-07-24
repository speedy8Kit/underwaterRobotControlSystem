from socket import timeout

from listings.detection_system import detection_system
from listings.runner import receive

if __name__ == '__main__':
    ########################### COMMAND RECEIVE #######################
    receive()

    ######################### run read msg ################################
    while True:
        try:
            com, addr = detection_system.socket.recv_com()
            com.run(addr, detection_system.socket)
        except timeout:
            continue