class Address(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


addr_DS = Address('localhost', 9091)
addr_NS = Address('localhost', 9092)
addr_CS = Address('localhost', 9093)
addr_M = Address('localhost', 9094)

sim_port_DS = 20001
sim_port_NS = 20002
sim_port_M = 19997
sim_port_CS = 20003

