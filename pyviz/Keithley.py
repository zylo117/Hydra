#! /usr/bin/env python32

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import visa
import time

class Keithley(object):

    def __init__(self, channel_GPIB):
        
        rm = visa.ResourceManager()
        
        # VISA instruments found:
        print('\nVISA instruments found:\n',rm.list_resources(),'\n')
        
        # connect to Keithley:
        self.inst = rm.get_instrument("GPIB0::%i::INSTR"%channel_GPIB)
        
        # query instrument info:
        print(self.inst)
        print(self.inst.ask("*IDN?")) # ask = write + read sequence
        
        # reset keithley
        self.inst.write("*RST")
        #self.inst.write("*RST; STATUS:PRESET; *CLS")

        #print self.inst.write(":SYST:BEEP:STAT?")
        self.inst.write(":SYST:BEEP:STAT off")
        #print self.inst.write(":SYST:BEEP:STAT?")


    def set_voltage_source(self,voltage=0, voltage_range=20):

        self.inst.write(":SOUR:FUNC VOLT")
        self.inst.write(":SOUR:VOLT:MODE FIXED")
        self.inst.write(":SOUR:VOLT:RANG %f"%voltage_range)
        self.inst.write(":SOUR:VOLT:LEV %f"%voltage)

    def set_current_source(self,current=0, current_range=1e-2):

        self.inst.write(":SOUR:FUNC CURR")
        self.inst.write(":SOUR:CURR:MODE FIXED")
        self.inst.write(":SOUR:CURR:RANG %f"%current_range)
        self.inst.write(":SOUR:CURR:LEV %f"%current)
        
    def output_on(self):
        self.inst.write(":OUTP ON")

    def output_off(self):
        self.inst.write(":OUTP OFF")
    
    def set_voltage_measurement(self, voltage_range=20, voltage_compliance=30):

        self.inst.write(":SENS:VOLT:PROT %f"%voltage_compliance)
        self.inst.write(":SENS:FUNC \"VOLT\"")
        self.inst.write(":SENS:VOLT:RANG %f"%voltage_range)
        self.inst.write(":FORM:ELEM VOLT")

    def set_current_measurement(self, current_range=1e-3, current_compliance=1e-3):

        self.inst.write(":SENS:CURR:PROT %f"%current_compliance)
        self.inst.write(":SENS:FUNC \"CURR\"")
        self.inst.write(":SENS:CURR:RANG %f"%current_range)
        self.inst.write(":FORM:ELEM CURR")

    def read(self):

        val = float(self.inst.ask("READ?"))
        return val

    def average_read(self,Nmeas=10):

        val = 0
        for i in range(Nmeas):
            val += float(self.inst.ask("READ?"))
        avg = val/Nmeas

        return avg



if __name__ == '__main__':
    
    channel_GPIB = 5

    voltage_range = 20
    voltage = 10.

    current_compliance = 1e-3
    current_range = 1e-3
    
    keithley = Keithley(channel_GPIB)

    keithley.set_voltage_source(voltage,voltage_range)

    keithley.set_current_measurement(current_range, current_compliance)

    keithley.output_on()

    current = keithley.read()
    print("current = ", current, "A")

    current_avg = keithley.average_read()
    print("average current = ", current_avg, "A")

    keithley.output_on()
