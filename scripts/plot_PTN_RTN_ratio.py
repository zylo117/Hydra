import pylab
import numpy
import PlotTools

PlotTools.set_figure_font(size=17)

elec_noise = 4.65

num_ref_cols = [64,128,256]
# 4 chan splitting
PTN = [9.2]*3
RTN = [2.8,2.0,1.6]
PTN = [7.9]*3
RTN = [2.4,1.7,1.4]
# no chan sep
PTN = [7.8]*3
RTN = [1.3,0.95,0.7]
PTN = [9.1]*3
RTN = [1.5,1.0,0.8]

ratio = numpy.array(PTN)/numpy.array(RTN)

pylab.grid(True)

pylab.xlim([0,300])
#pylab.ylim([3,6])
pylab.ylim([5.5,12])

#pylab.title('Hard/Soft')
#pylab.title('Low Noise')
pylab.xlabel('# ref cols')
pylab.ylabel('PTN/RTN')

pylab.plot(num_ref_cols,ratio,'mo--',linewidth=4,markersize=15)
pylab.show()
