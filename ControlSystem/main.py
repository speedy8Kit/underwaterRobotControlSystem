# import time
from listings.runners import *

"""контроллер пропеллерами знает о положении цели относительно аппарата,
которое выдал TSS и на основании этих данных генерирует сигналы управления
с помощью пид регулятора.
Для ограничения изменения и значения максимального выходного сигнала
добавлен ограничитель."""

if __name__ == '__main__':
    ########################### COMMAND RECEIVE #######################
    receive()

    ######################### run read msg ################################
    while True:
        com, addr = pr.propeller_controller.socket.recv_com()
        com.run(addr, pr.propeller_controller.socket)
