from listings.runners import *

if __name__ == '__main__':
    ########################### COMMAND RECEIVE #######################
    receive()

    ######################### run read msg ################################
    while True:
        com, addr = ns.navigation_system.socket.recv_com()
        com.run(addr, ns.navigation_system.socket)
