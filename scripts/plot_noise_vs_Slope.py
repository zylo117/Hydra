import pylab
import numpy
import PlotTools

PlotTools.set_figure_font(size=17)

elec_noise = 4.65

#[04,08,0F,4F,5F,6F] 
#Slope = [30.,15.,8.,4.,3.,2.,0.]# us/200mV
#Noise = [7.8,7.9,8.15,8.4,8.6,9.0,10.6]
#Noise_pix= (numpy.array(Noise)**2 - elec_noise**2)**0.5

#[00,02,04,08,0F,4F,5F,6F] 
#Slope = [30.,15.,8.,4.,3.,2.,0.]# us/200mV
#Slope = {'00':99999,'02':60.,'04':30.,'08':15.,'0F':8.,'4F':4.,'5F':2.,'6F':60.}
dT = [0,2,4,6,8,10,12,16,20] #us
Noise = [10.7,9.3,8.5,8.25,8.1,8.0,7.9,7.9,7.85]
best_slope = ['xx',0x0F,0x0F,0x0F,0x0F,0x08,0x08,0x04,0x04]
best_vstart = ['xx',0x50,0x50,0x54,0x58,0x54,0x54,0x50,0x50]
Noise_pix= (numpy.array(Noise)**2 - elec_noise**2)**0.5
red_factor = Noise_pix[0]/Noise_pix

pylab.grid(True)

#pylab.xlim([-2,32])
pylab.xlim([-1,21])
#pylab.ylim([7,11])
#pylab.ylim([7.5,11])
#pylab.ylim([3,16])
#pylab.ylim([78,90])
pylab.ylim([0.9,1.6])

#pylab.xlabel('Slope [us/200mV]')
pylab.xlabel('Low Noise Reset time [us]')
#pylab.ylabel('Pixel Temporal Noise [DN]')
pylab.ylabel('Pixel Noise Reduction Factor')
#pylab.ylabel('Slope [Hex]')
#pylab.ylabel('Vstart [Hex]')

#pylab.plot(Slope,Noise_pix,'o-',linewidth=3)
#pylab.plot(dT,Noise_pix,'o-',linewidth=4,markersize=15)
pylab.plot(dT,red_factor,'o-',linewidth=4,markersize=15)
#pylab.plot(dT,Noise,'o-',linewidth=4,markersize=15)
#pylab.plot(dT[1:],best_slope[1:],'d-',linewidth=4,markersize=15)
#pylab.plot(dT[1:],best_vstart[1:],'d-',linewidth=4,markersize=15)
pylab.show()
