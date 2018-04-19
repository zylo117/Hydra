#! /usr/bin/env python32

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import time
import numpy
import pylab

import Keithley
import HyVision

k = 1.38e-23
e = 1.6e-19

def calc_temperature(I,V):

    Temp = []
    Curr_avg = []

    for i in range(len(I)-1):

        T = e/k * (V[i+1]-V[i]) / numpy.log(I[i+1]/I[i])
        curr_avg = (I[i+1]-I[i])/2.

        Temp.append(T)
        Curr_avg.append(curr_avg)

    return numpy.array(Temp),numpy.array(Curr_avg)


if __name__ == '__main__':

    t0 = time.time()

    channel_GPIB = 5

    voltage_range = 2
    voltage_compliance = voltage_range
    #voltage = 0.2
    
    #current = 1e-7
    current_range = 1e-3
    current_compliance = current_range

    #Current = numpy.arange(10e-7,200e-7,10e-7)
    Current = numpy.arange(-20e-6,10e-6,1e-6)
    #Current = numpy.arange(-5e-6,1e-6,0.1e-6)
    #Current = numpy.arange(0.1e-6,2e-6,0.1e-6)
    #Current = numpy.arange(1e-7,20e-7,1e-7)
    #Current = numpy.array([1e-6,5e-6,10e-6])
    print("Current scan:",Current[0]*10**6,'-',Current[-1]*10**6,'uA')

    Voltage = []

    keithley = Keithley.Keithley(channel_GPIB)

    for current in Current:


        keithley.set_current_source(current,current_range)
        keithley.set_voltage_measurement(voltage_range, voltage_compliance)

        keithley.output_on()

        time.sleep(10)
        print("Time: ",time.time()-t0)

        voltage = keithley.read()
        Voltage.append(voltage)

        keithley.output_off()

        print(current, voltage)
    

Voltage = numpy.array(Voltage)

Resistance = Voltage/Current

#print "Resistance [kohm]:",Resistance/10**3
Temp,Curr_avg = calc_temperature(Current,Voltage)

pylab.grid(True)

pylab.xlabel("Current [uA]")
pylab.ylabel("Voltage [V]")
pylab.plot(Current*10**6,Voltage,'o-')
pylab.show()

pylab.xlabel("Current [uA]")
pylab.ylabel("Temperature [K]")
pylab.plot(Current[1:]*10**6,Temp,'ro')
pylab.grid(True)
pylab.ylim([-600,0])
pylab.show()
