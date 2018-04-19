#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import numpy

class Calibration(object):


    def __init__(self, file_calibration = "J:\\SYSTEMS_CHARACTERIZATION\\LAB\\Hardware\\Power_Meter_Calibration_Mightex_LED.txt"):

        self.file_calibration = file_calibration

        f = open(self.file_calibration)
        
        lines = f.readlines()[1:] # remove first line ()
        
        self.LED_intensity = numpy.array([float(l.split('\t')[0]) for l in lines])
        self.Lux = numpy.array([float(l.split('\t')[-1]) for l in lines])

        f.close()


    def mA2Lux(self, LEDintensity):

        if LEDintensity < self.LED_intensity[0]: raise "LED intensity provided (%f) is smaller than the smallest value (%f) available in the calibration file (%s)"
        if LEDintensity > self.LED_intensity[-1]: raise "LED intensity provided (%f) is larger than the largest value (%f) available in the calibration file (%s)"

        if LEDintensity == self.LED_intensity[-1]: return self.Lux[-1]

        i = numpy.where(self.LED_intensity >= LEDintensity)[0][0] - 1

        Lux = self.Lux[i] + (self.Lux[i+1]-self.Lux[i]) * (LEDintensity - self.LED_intensity[i]) / (self.LED_intensity[i+1] - self.LED_intensity[i])

        return Lux

    
    def mA2Luxsec(self, LEDintensity, dT):

        return self.mA2Lux(LEDintensity) * dT


if __name__ == '__main__':


    print("test")

    calib = Calibration()
    print(calib.LED_intensity)
    print(calib.Lux)
    print(calib.mA2Lux(351))
