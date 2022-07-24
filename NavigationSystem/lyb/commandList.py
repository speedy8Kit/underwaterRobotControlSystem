import struct
from abc import ABC, abstractmethod
from typing import List, Type
from typing import Any
from lyb.address import Address


class Command(ABC):
    """общий класс для всех комманд способный упаковывать и распаковывать
     передаваемые данные в соответствии с типом команды.
     Все прямые наследники должны переопределить:
     key - индивидуальный ключ команды;
     name - имя команды
     format_data - тип передаваемых данных (при отсутствиие, не переопределять);
     def __init__(self, имена тех данных которые передаются)
     Для принятия команды необходимо создать ее класс наследник в котором переопределить метод run
     и изменить флаг add_commands на True.
    """

    key = None
    name = None
    format_data = ''
    struct = None
    add_commands = False

    def run(self, senders: Address, socket):
        """функция вызываемая при получение команды"""
        print(self.name, "don't have runner")

    def __new__(cls, *args):
        if not hasattr(cls, "instance"):
            if cls.add_commands:
                commands.append(cls)
            cls.struct = struct.Struct(cls.format_data)
            cls.instance = super(Command, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def __init__(self, *args):
        self.__params = args

    def pack(self) -> bytes:
        """запоаковвает данне команды с учетом data и ее ключа"""
        if self.__params is None:
            return struct.pack('i', self.key)
        else:
            return struct.pack('i', self.key) + self.struct.pack(*self.__params)
            # return self.struct.pack(*self.params)
            # поменяй эти строки если хочешь проверить как работает __name__==commandList

    @classmethod
    def unPack(cls, data_send: bytes) -> tuple[Any, ...]:
        """распаковывает сообщение состоящее только из параметров,
         предполагается, что ключ команды был принят раньее"""
        if data_send == b'':
            return ()
        return cls.struct.unpack(data_send)

    @staticmethod
    def unPackKey(key_send) -> int:
        """распаковывает ключ любого сообщения
         при отсутствие принятых данных возвращает команду 0"""
        if key_send == b'':
            return 0x88
        return int(struct.unpack('i', key_send)[0])

    def __len__(self) -> int:
        return self.struct.size


commands: List[Type[Command]] = []


################################## REQUESTS #######################################

class REQ_COUNT_NAVIG(Command):
    key = 0x00
    name = 'REQ_COUNT_NAVIG'

    def __init__(self):
        super().__init__()


class REQ_COUNT_PROPELLER_CONTROL_SIGNAL(Command):
    key = 0x02
    name = 'MSG_COUNT_PROPELLER_CONTROL_SIGNAL'

    def __init__(self):
        super().__init__()


class REQ_PROCESS_PICTURE(Command):
    key = 0x03
    name = 'MSG_PROCESS_PICTURE'

    def __init__(self):
        super().__init__()


################################## RESPONSES #######################################

class MSG_NAVIG(Command):
    key = 0x10
    name = 'MSG_NAVIG'
    format_data = '12d'

    def __init__(self,
                 x: float = 0, y: float = 0, z: float = 0,
                 alfa: float = 0, betta: float = 0, gamma: float = 0,
                 linear_velocity_x: float = 0, linear_velocity_y: float = 0, linear_velocity_z: float = 0,
                 angular_velocity_x: float = 0, angular_velocity_y: float = 0, angular_velocity_z: float = 0):
        super().__init__(x, y, z,
                         alfa, betta, gamma,
                         linear_velocity_x, linear_velocity_y, linear_velocity_z,
                         angular_velocity_x, angular_velocity_y, angular_velocity_z)
        self.coordinates = (x, y, z)
        self.euler_angles = (alfa, betta, gamma)
        self.linear_velocity = (linear_velocity_x, linear_velocity_y, linear_velocity_z)
        self.angular_velocity = (angular_velocity_x, angular_velocity_y, angular_velocity_z)


class MSG_PROPELLER_CONTROL_SIGNAL(Command):
    key = 0x12
    name = 'MSG_PROPELLER_CONTROL_SIGNAL'
    format_data = '5d'

    def __init__(self,
                 sig_r: float = 0, sig_l: float = 0,
                 sig_t: float = 0, sig_b: float = 0,
                 h: float = 0):
        super().__init__(sig_r, sig_l, sig_t, sig_b, h)
        self.velocity = [sig_r, sig_l, sig_t, sig_b]
        self.h = h


class MSG_PICTURE_PROCESSED(Command):
    key = 0x13
    name = 'EVENT_PICTURE_PROCESSED'

    def __init__(self):
        super().__init__()


################################## SERVICE #######################################

class SRV_ADD_POINT(Command):
    key = 0x40
    name = 'SRV_ADD_POINT'
    format_data = '4d3i'

    def __init__(self, x: float = 0, y: float = 0, h: float = 0, v: float = 0,
                 move_mode: int = 0, height_mode: int = 0, number: int = 0):
        super().__init__(x, y, h,
                         v,
                         move_mode, height_mode, number)
        self.pos = [x, y]
        self.v = v
        self.h = h
        self.mods = [move_mode, height_mode]
        self.number = number


class SRV_GENERATE_PATH(Command):
    key = 0x41
    name = 'SRV_GENERATE_PATH'
    format_data = 'i'

    def __init__(self, number: int = 1):
        super().__init__(number)
        self.number = number


################################### EVENTS ####################################

class EVENT_END_POS(Command):
    key = 0x50
    name = 'EVENT_END_POS'

    def __init__(self):
        super().__init__()


class EVENT_OBJ(Command):
    key = 0x51
    name = 'EVENT_OBJ'
    format_data = '2d'

    def __init__(self, px_x, px_y):
        super().__init__(px_x, px_y)
        self.holst_pos = [px_x, px_y]


class EVENT_CONNECT(Command):
    def __init__(self, event=True):
        super().__init__(event)
        self.event = event

    key = 0x52
    name = "EVENT_CONNECT"
    format_data = '?'


################################### COMMANDS ####################################

class CMD_CONNECT(Command):
    def __init__(self):
        super().__init__()

    key = 0x60
    name = "CMD_CONNECT"


#################################### SPEC #####################################

class SPEC_UNKNOWN_COMMAND(Command):
    key = 0x92
    name = 'EVENT_UNKNOWN_COMMAND'

    def __init__(self):
        super().__init__()

    @classmethod
    def unPack(cls, data_send: bytes) -> tuple[Any, ...]:
        return ()


# команда которая всегда должна быть в списке,
# без ее объевления невозможно поняять,
# что какой-то комманды не существует
event_unknown_command = SPEC_UNKNOWN_COMMAND()


def findACommand(key_received: int) -> Type[Command]:
    for comClass in commands:
        if key_received == comClass.key:
            return comClass
    print("I don't find key: ", key_received)
    return SPEC_UNKNOWN_COMMAND
