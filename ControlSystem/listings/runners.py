import sim
import lyb.connector as connector
import lyb.address as address
from listings.point import Point
import lyb.commandList as commList
import listings.propeller_controller as pr


class RECEIVE_REQ_COUNT_PROPELLER_CONTROL_SIGNAL(commList.REQ_COUNT_PROPELLER_CONTROL_SIGNAL):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        pr.propeller_controller.count_signals()

        r = pr.propeller_controller.signals[pr.propeller_controller.r]
        l = pr.propeller_controller.signals[pr.propeller_controller.l]
        t = pr.propeller_controller.signals[pr.propeller_controller.t]
        b = pr.propeller_controller.signals[pr.propeller_controller.b]
        h = (pr.propeller_controller.height_f + pr.propeller_controller.height_b) / 2

        ID = pr.propeller_controller.clientID
        oneShot = sim.simx_opmode_oneshot

        sim.simxSetFloatSignal(ID, 'prop_sig_r', r, oneShot)
        sim.simxSetFloatSignal(ID, 'prop_sig_l', l, oneShot)
        sim.simxSetFloatSignal(ID, 'prop_sig_t', t, oneShot)
        sim.simxSetFloatSignal(ID, 'prop_sig_b', b, oneShot)

        socket.send_com(commList.MSG_PROPELLER_CONTROL_SIGNAL(r, l, t, b, h), address.addr_M)


class RECEIVE_MSG_NAVIG(commList.MSG_NAVIG):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        pr.propeller_controller.setLinearVelocity(*self.linear_velocity)
        pr.propeller_controller.setPos(*self.coordinates)
        pr.propeller_controller.setOrientation(*self.euler_angles)


class RECEIVE_SRV_ADD_POINT(commList.SRV_ADD_POINT):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        print(self.pos[Point.pos.x], self.pos[Point.pos.y], self.h, self.v, self.mods[0],
              self.mods[1], self.number)

        p = Point(self.pos[Point.pos.x], self.pos[Point.pos.y], self.h, self.v, self.mods[0],
                  self.mods[1], self.number)

        if self.number > 0:
            pr.propeller_controller.path.addPoint(p)


class RECEIVE_SRV_GENERATE_PATH(commList.SRV_GENERATE_PATH):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        pr.propeller_controller.path.generatePath()
        pr.propeller_controller.path.printPath()

        # отправить на менеджер подтверждение получения всех точек
        if self.number == len(pr.propeller_controller.path.list_point):
            pr.propeller_controller.socket.send_com(
                commList.SRV_GENERATE_PATH(len(pr.propeller_controller.path.list_point)), address.addr_M)


class RECEIVE_CMD_CONNECT(commList.CMD_CONNECT):
    add_commands = True

    def run(self, senders: address.Address, socket: connector.MySocket):
        if pr.propeller_controller.clientID is not None:
            sim.simxFinish(0)
        pr.propeller_controller = pr.ControlSystem()
        pr.propeller_controller.clientID = sim.simxStart('127.0.0.1', address.sim_port_CS, True, True, 2000, 5)

        if pr.propeller_controller.clientID == -1:
            print("connect fail")
            socket.send_com(commList.EVENT_CONNECT(False), senders)
        else:
            ID = pr.propeller_controller.clientID
            stream = sim.simx_opmode_streaming
            wait = sim.simx_opmode_oneshot_wait
            socket.send_com(commList.EVENT_CONNECT(True), senders)

            sim.simxSetFloatSignal(ID, 'prop_sig_r', 0, stream)
            sim.simxSetFloatSignal(ID, 'prop_sig_l', 0, stream)
            sim.simxSetFloatSignal(ID, 'prop_sig_t', 0, stream)
            sim.simxSetFloatSignal(ID, 'prop_sig_b', 0, stream)

            _, target_x = sim.simxGetFloatSignal(ID, 'target_x', stream)
            _, target_y = sim.simxGetFloatSignal(ID, 'target_y', stream)
            _, target_z = sim.simxGetFloatSignal(ID, 'target_z', stream)

            _, pr.propeller_controller.sensor_height_f = sim.simxGetObjectHandle(ID, 'PS_height_f', wait)
            _, pr.propeller_controller.sensor_height_b = sim.simxGetObjectHandle(ID, 'PS_height_b', wait)
            sim.simxReadProximitySensor(ID, pr.propeller_controller.sensor_height_f, stream)
            sim.simxReadProximitySensor(ID, pr.propeller_controller.sensor_height_b, stream)

            _, pr.propeller_controller.sensor_mid = sim.simxGetObjectHandle(ID, "PS_mid", wait)
            _, pr.propeller_controller.sensor_left = sim.simxGetObjectHandle(ID, "PS_left", wait)
            _, pr.propeller_controller.sensor_right = sim.simxGetObjectHandle(ID, "PS_right", wait)
            _, _, _, _, _ = sim.simxReadProximitySensor(ID, pr.propeller_controller.sensor_right, stream)
            _, _, _, _, _ = sim.simxReadProximitySensor(ID, pr.propeller_controller.sensor_left, stream)
            _, _, _, _, _ = sim.simxReadProximitySensor(ID, pr.propeller_controller.sensor_mid, stream)

            print("connect ok")


########################### COMMAND RECEIVE #######################
def receive():
    RECEIVE_REQ_COUNT_PROPELLER_CONTROL_SIGNAL()
    RECEIVE_MSG_NAVIG()
    RECEIVE_CMD_CONNECT()
    RECEIVE_SRV_ADD_POINT()
    RECEIVE_SRV_GENERATE_PATH()
