#! /usr/bin/env python32

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import Keithley
import HyVision

if __name__ == '__main__':

    channel_GPIB = 5

    voltage_range = 20
    voltage = 10.

    current_compliance = 1e-3
    current_range = 1e-3
    
    keithley = Keithley.Keithley(channel_GPIB)

    keithley.set_voltage_source(voltage,voltage_range)

    keithley.set_current_measurement(current_range, current_compliance)

    keithley.output_on()

    current = keithley.read()
    print("current = ", current, "A")

    current_avg = keithley.average_read()
    print("average current = ", current_avg, "A")

    keithley.output_on()
    
