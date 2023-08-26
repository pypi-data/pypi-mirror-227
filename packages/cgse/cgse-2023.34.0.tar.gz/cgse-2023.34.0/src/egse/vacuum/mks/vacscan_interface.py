from egse.device import DeviceInterface
from egse.decorators import dynamic_interface


class VacscanError(Exception):
    """ Vacscan protocol errors. """


class VacscanInterface(DeviceInterface):

    @dynamic_interface
    def get_status(self):
        return NotImplemented

    @dynamic_interface
    def reset(self):
        return NotImplemented

    @dynamic_interface
    def get_barchart(self):
        return NotImplemented
