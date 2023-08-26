import logging
import time
from functools import partial

import yaml

from egse.serialdevice import SerialDevice
from egse.command import Command
from egse.settings import Settings
from egse.vacuum.mks.vacscan_interface import VacscanInterface, VacscanError

logger = logging.getLogger(__name__)

# Load the device settings from the global common-egse config file
DEVICE_SETTINGS = Settings.load("MKS Vacscan Controller")

# Load the device protocol
DEVICE_PROTOCOL = Settings.load(filename='vacscan.yaml')['Commands']


class VacscanController(SerialDevice, VacscanInterface):

    def __init__(self, port=None, baudrate=9600):

        # Load device configuration from the common-egse global config file
        self._port     = DEVICE_SETTINGS.PORT if port is None else port
        self._baudrate = DEVICE_SETTINGS.BAUDRATE if baudrate is None else baudrate

        # Create a dict of Command objects for each function
        self._commands = {}
        for name, items in DEVICE_PROTOCOL.items():
            if 'cmd' in items:
                self._commands[name] = Command(name, items['cmd'])

        # Initialize the parent class with the port and baudrate
        super().__init__(port=self._port, baudrate=self._baudrate, terminator='\r\n')
        self.connect()

    def reset(self):
        return self.query(self._commands['reset'].get_cmd_string(), check_response=False)

    def enable_acknowledge(self):
        return self.query(self._commands['enable_acknowledge'].get_cmd_string())

    def get_status(self):
        return self.query(self._commands['get_status'].get_cmd_string())

    def read_data(self):
        return self.query(self._commands['read_data'].get_cmd_string())

    def set_barchart(self):
        return self.query(self._commands['set_barchart'].get_cmd_string())

    def enable_filament(self, index, enable):
        return self.query(self._commands['enable_filament'].get_cmd_string(index, enable))

    def press_key(self, index, count):
        return self.query(self._commands['press_key'].get_cmd_string(index, count))

    def set_scan_speed(self, value):
        return self.query(self._commands['set_scan_speed'].get_cmd_string(value))

    def set_first_mass(self, value):
        return self.query(self._commands['set_first_mass'].get_cmd_string(value))

    def set_mass_zoom(self, value):
        return self.query(self._commands['set_mass_zoom'].get_cmd_string(value))

    def set_gain(self, value):
        return self.query(self._commands['set_gain'].get_cmd_string(value))

    def set_time_interval(self, value):
        return self.query(self._commands['set_time_interval'].get_cmd_string(value))

    def query(self, command, check_response=True):
        """ Override the parent class to do some error checking on the response. """

        if not check_response:
            self.send_command(command)

        else:
            response = super().query(command)

            if len(response) == 0:
                raise VacscanError('No response received for command: {}'.format(command))
            elif response[-2:] != '\r\n':
                raise VacscanError('Invalid response terminators received: {}'.format(response))
            elif response[0] == 'N':
                raise VacscanError('NACK response received for command: {}'.format(command))
            elif response[0] != 'A':
                raise VacscanError('Invalid response received: {}'.format(response))

            if len(response) > 3:
                return response[1:-2]

        return None

def main():
    dev = VacscanController(port='/dev/vacscan')

    print(dev.get_status())
    # dev.set_gain(8)
    dev.set_mass_zoom(100)
    print(dev.get_status())

    # dev.reset()
    # dev.enable_acknowledge()
    # dev.set_gain(7)
    # dev.set_time_interval(100)
    dev.set_barchart()
    # dev.enable_filament(1, 1)

    while True:
        time.sleep(10)
        print(dev.read_data())


if __name__ == '__main__':
    main()
