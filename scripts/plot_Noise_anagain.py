import pylab
import numpy
import PlotTools

PlotTools.set_figure_font(size=17)

analog_gain = [-6,0,6,12,18]
#corr_fact = 10**(numpy.array(analog_gain)/20.)
corr_fact = numpy.array([0.52,1,1.88,3.17,5.01])
print(corr_fact)

# Hard/Soft
TTN = [5.77,9.23,15.89,25.92,39.38]
RTN = [0.68,1.02,1.74,2.86,4.56]
CFPN = [0.46,0.66,1.44,2.98,15.15]
TFPN = [1.31,2.44,5.00,8.05,19.97]

# Low Noise
TTN_ln = [5.12,7.80,13.12,21.30,32.65]
RTN_ln = [0.62,0.93,1.56,2.60,4.15]
CFPN_ln = [0.56,0.88,1.74,3.40,11.51]
TFPN_ln = [1.49,2.99,5.72,9.65,20.84]

elec_noise = [4.36,5.81,8.88,13.93,21.14]
AFE_noise = [2.57,2.62,2.64,2.65,2.63]

TTN = numpy.array(TTN)
elec_noise = numpy.array(elec_noise)

pylab.grid(True)

#pylab.xlim([0,300])
#pylab.ylim([3,6])

#pylab.title('Hard/Soft')
#pylab.title('Low Noise')
pylab.xlabel('Analog Gain [dB]')
#pylab.ylabel('Total temporal Noise [DN]')
#pylab.ylabel('Row temporal Noise [DN]')
#pylab.ylabel('Column FPN [DN]')
#pylab.ylabel('Total FPN [DN]')
#pylab.ylabel('Electronic Temporal Noise [DN]')
#pylab.ylabel('AFE Temporal Noise [DN]')

pylab.ylabel('Total temporal Noise [DN] - gain corrected')
#pylab.ylabel('Row temporal Noise [DN] - gain corrected')
#pylab.ylabel('Column FPN [DN] - gain corrected')
#pylab.ylabel('Total FPN [DN] - gain corrected')
#pylab.ylabel('Electronic Temporal Noise [DN] - gain corrected')
#pylab.ylabel('Pixel only Temporal Noise [DN] - gain corrected')

#pylab.ylim([0,45])
#pylab.plot(analog_gain,TTN,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,TTN_ln,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,5])
#pylab.plot(analog_gain,RTN,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,RTN_ln,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,16])
#pylab.plot(analog_gain,CFPN,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,CFPN_ln,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,25])
#pylab.plot(analog_gain,TFPN,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,TFPN_ln,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,25])
#pylab.plot(analog_gain,elec_noise,'go--',linewidth=4,markersize=10)
#pylab.ylim([0,3])
#pylab.plot(analog_gain,AFE_noise,'go--',linewidth=4,markersize=10)

pylab.ylim([0,15])
pylab.plot(analog_gain,TTN/corr_fact,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,TTN_ln/corr_fact,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,2])
#pylab.plot(analog_gain,RTN/corr_fact,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,RTN_ln/corr_fact,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,4])
#pylab.plot(analog_gain,CFPN/corr_fact,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,CFPN_ln/corr_fact,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,5])
#pylab.plot(analog_gain,TFPN/corr_fact,'mo--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,TFPN_ln/corr_fact,'bo--',linewidth=4,markersize=10)
#pylab.ylim([0,10])
#pylab.plot(analog_gain,elec_noise/corr_fact,'go--',linewidth=4,markersize=10)
#pylab.plot(analog_gain,(TTN**2-elec_noise**2)**0.5/corr_fact,'go--',linewidth=4,markersize=10)

pylab.show()
