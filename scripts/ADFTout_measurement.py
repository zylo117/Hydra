#! /usr/bin/env python32

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import time
import numpy
#import pylab

from pyvisage import Keithley
from pyvisage import HyVision

def measure_adft_out(adft_channel=0x00):

    slave_address = 0x10
    length_register_address = 2 # byte(s)
    register_address = 0x364B
    data_length = 1 # byte(s)
    data_value = adft_channel

    hyviz.I2C_write(slave_address, length_register_address, register_address, data_length, data_value)

    keithley.set_voltage_measurement(voltage_range, voltage_compliance)

    keithley.output_on()

    time.sleep(0.2)
    #time.sleep(1.0)
    #print "Time: ",time.time()-t0

    voltage = keithley.read()
    
    keithley.output_off()

    return voltage


if __name__ == '__main__':

    #filename = "Z:\\PC5\\ADFT_out_measurements\\ADFT_out_DAC_Bandgap_measurements.txt"
    #filename = "ADFT_out_DAC_Bandgap_measurements.txt"
    filename = 'blacksun_bottom_full.csv'
    b_dir_from_config = False
    #directory = 'Z:\\PC5\\ADFT_out_measurements\\test001'
    directory = 'Z:\\PC5\\DACs\\Q8A685w02#26A_blacksun'

    b_bandgap = False
    b_blacksun = True
    b_filmbias = False
    b_resetnoise = False

    GPIO_pin = 0

    hyviz = HyVision.HyVision()
    hyviz.set_HVS_PS()
    hyviz.set_GPIO_pin(GPIO_pin)

    t0 = time.time()

    channel_GPIB = 5

    voltage_range = 5
    voltage_compliance = voltage_range
    
    current = 0.
    current_range = 1e-6
    #current_compliance = current_range

    keithley = Keithley.Keithley(channel_GPIB)

    keithley.set_current_source(current,current_range)

    # Voltage measurements:
    #DAC_registers = [0x00, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x7F]
    DAC_registers = list(range(128))
    
    # Bandgap Voltage
    if b_bandgap:
        adft_channel = 0x00
        voltage_bandgap = measure_adft_out(adft_channel)

    # Blacksun DAC
    if b_blacksun:
        adft_channel = 0x0A
        voltage_blacksun = []
        for dac_register in DAC_registers:
            hyviz.I2C_write(0x10,2,0x3632,1,dac_register)        
            hyviz.I2C_write(0x10,2,0x3633,1,dac_register)        
            voltage_blacksun.append(measure_adft_out(adft_channel))
            print(dac_register,voltage_blacksun[-1])

    # Filmbias DAC
    if b_filmbias:
        adft_channel = 0x0B
        voltage_filmbias = []
        for dac_register in DAC_registers:
            hyviz.I2C_write(0x10,2,0x3601,1,dac_register)        
            voltage_filmbias.append(measure_adft_out(adft_channel))
            
    # Reset Noise DAC
    if b_resetnoise:
        adft_channel = 0x0E
        voltage_RSTnoise = []
        for dac_register in DAC_registers:
            hyviz.I2C_write(0x10,2,0x3605,1,dac_register)        
            voltage_RSTnoise.append(measure_adft_out(adft_channel))

    hyviz.close_USB_comm()

    if b_bandgap: print("Bandgap Voltage =", voltage_bandgap)
    if b_blacksun: print("Blacksun Voltage =", voltage_blacksun)
    if b_filmbias: print("Filmbias Voltage =", voltage_filmbias)
    if b_resetnoise: print("RSTnoise Voltage =", voltage_RSTnoise)

    if b_dir_from_config:
        #f_config = open("Z:\\PROGRAMS\\PyVision_488\\config.txt")
        f_config = open("Z:\\PC5\\ADFT_out_measurements\\config.txt")
        directory = f_config.readlines()[0]
        f_config.close()
    print("directory",directory)

    if not(os.path.exists(directory)):
        os.mkdir(directory)

    filename = os.path.join(directory,filename)

    f = open(filename,'w')

    if b_bandgap:
        f.write("Bandgap Voltage [Volt]: %f\n\n"%voltage_bandgap)

    if b_blacksun:
        #f.write("Blacksun DAC:\n")
        #f.write('Register values (0x3632/0x3633): '+', '.join([str(hex(v)) for v in DAC_registers])+'\n')
        #f.write('Voltages [Volt]: '+', '.join([str(v) for v in voltage_blacksun])+'\n\n')
        f.write('Register value,DAC output\n')
        for i in range(len(DAC_registers)):
            f.write('%s,%s\n'%(DAC_registers[i],voltage_blacksun[i]))

    if b_filmbias:
        f.write("Filmbias DAC:\n")
        f.write('Register values (0x3601): '+', '.join([str(hex(v)) for v in DAC_registers])+'\n')
        f.write('Voltages [Volt]: '+', '.join([str(v) for v in voltage_filmbias])+'\n\n')

    if b_resetnoise:
        f.write("Reset Noise DAC:\n")
        f.write('Register values (0x3605): '+', '.join([str(hex(v)) for v in DAC_registers])+'\n')
        f.write('Voltages [Volt]: '+', '.join([str(v) for v in voltage_RSTnoise])+'\n\n')

    f.close()
