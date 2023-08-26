import logging

from egse.control import ControlServer
from egse.command import ClientServerCommand
from egse.protocol import CommandProtocol
from egse.proxy import Proxy
from egse.settings import Settings
from egse.zmq_ser import bind_address
from egse.system import format_datetime
from egse.vacuum.mks.vacscan_interface import VacscanInterface
from egse.vacuum.mks.vacscan_controller import VacscanController
from egse.vacuum.mks.vacscan_simulator import VacscanSimulator
from egse.zmq_ser import connect_address


LOGGER = logging.getLogger(__name__)

DEVICE_SETTINGS = Settings.load(filename="vacscan.yaml")
CTRL_SETTINGS = Settings.load("MKS Vacscan Control Server")


class VacscanCommand(ClientServerCommand):
    pass


class VacscanProtocol(CommandProtocol):

    def __init__(self, control_server: ControlServer):

        super().__init__()
        self.control_server = control_server

        if Settings.simulation_mode():
            self.dev = VacscanSimulator()
        else:
            self.dev = VacscanController()

        self.load_commands(DEVICE_SETTINGS.Commands, VacscanCommand, VacscanInterface)
        self.build_device_method_lookup_table(self.dev)


    # move to parent class?
    def get_bind_address(self):
        return bind_address(
            self.control_server.get_communication_protocol(),
            self.control_server.get_commanding_port(),
        )


    def get_status(self):
        status_dict = super().get_status()

        return status_dict


    def get_housekeeping(self) -> dict:
        result = dict()
        result["timestamp"] = format_datetime()

        return result


class VacscanProxy(Proxy):

    def __init__(self):
        super().__init__(
            connect_address(
                CTRL_SETTINGS.PROTOCOL, CTRL_SETTINGS.HOSTNAME, CTRL_SETTINGS.COMMANDING_PORT))
