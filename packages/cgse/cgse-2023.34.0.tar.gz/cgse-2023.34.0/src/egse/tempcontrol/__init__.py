"""
This package provides services for different kinds of temperature controllers.

The current on-going work is for support of the following devices:

* Keithley DAQ6510
* LakeShore Model 336
* National Instruments
* SRS PTC10 temperature regulator

"""
class TempError(Exception):
    pass