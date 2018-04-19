#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from . import Image
from . import ImageArray
from . import Measurement
from . import PlotTools

class PhotonTransfert(Measurement.Measurement):

    def analyze_response(self,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=67,bsave=False,directory_suffix=None,bfullresolution=False,blog=False,bfit=True,fitrange='all',linewidth=1.0):

        print("\nStarting Response analysis")

        self.analyze(bsave=bsave,directory_suffix=directory_suffix,bfullresolution=bfullresolution,blog=blog,bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop,bnoise=False)

        self.create_analysis_directory(directory_suffix)

        fname_results = os.path.join(self.directory_analysis,'Response_results.txt')
        fresults = open(fname_results,'w')
        fresults.write('Parameter: '+self.param_label+'\n')
        fresults.write('Values scanned: '+', '.join(str(v) for v in self.param)+'\n')
        fresults.write('Unit: '+self.param_unit+'\n\n')
        fresults.write('Parameter [calibrated]: '+self.param_cal_label+'\n')
        fresults.write('Values scanned [calibrated]: '+', '.join(str(v) for v in self.param_cal)+'\n')
        fresults.write('Unit [calibrated]: '+self.param_cal_unit+'\n\n')


        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Response",yunit='DN',bsave=True,directory_save=self.directory_analysis)

        fresults.write('Response:\n')
        for i in range(self.num_channel_groups):
            fresults.write('Channel %i: '%i+', '.join(str(v) for v in self.Average[i])+'\n')

        fresults.close()

        return self.Average



    def analyze_photontransfert(self,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=67,bsave=False,directory_suffix=None,bfullresolution=False,blog=False,bfit=True,fitrange='all',linewidth=1.0):

        print("\nStarting Photon Transfert analysis")

        self.analyze(bsave=bsave,directory_suffix=directory_suffix,bfullresolution=bfullresolution,blog=blog,bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop)

        self.create_analysis_directory(directory_suffix)

        fname_results = os.path.join(self.directory_analysis,'PTC_results.txt')
        fresults = open(fname_results,'w')

        #fresults.write('RTN noise: '+', '.join(str(v) for v in self.Image[0].rtn_noise)+'\n\n')        

        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Response",yunit='DN',bsave=True,directory_save=self.directory_analysis)
        #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Response",yunit='DN',ylim=[0,2800],bsave=True,directory_save=self.directory_analysis)
        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Offset,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Offset",yunit='DN',bsave=True,directory_save=self.directory_analysis)
        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Temporal_Noise,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis)

        PlotTools.plot(self.Average,self.Temporal_Noise,xlabel="Response",xunit='DN',ylabel="Noise",yunit='DN',bfit=False,bsave=True,directory_save=self.directory_analysis)

        # SNR
        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average/self.Temporal_Noise,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="SNR",yunit='',bsave=True,directory_save=self.directory_analysis)

        # Compute shot noise (remove read noise in quadrature):
        Read_noise = []
        Noise_shot = []
        for i in range(self.num_channel_groups):
            Read_noise.append(self.Temporal_Noise[i][0])
            #Read_noise.append(0.9999*self.Temporal_Noise[i][0])
            print(self.Temporal_Noise[i])
            print(Read_noise[i])
            print(self.Temporal_Noise[i]**2-Read_noise[i]**2)
            Noise_shot.append(numpy.sqrt(self.Temporal_Noise[i]**2-Read_noise[i]**2))
        fresults.write('Read Noise: '+', '.join(str(v) for v in Read_noise)+'\n\n')
        PlotTools.plot_scatter(list(range(self.num_channel_groups)),Read_noise,xlabel='Group',ylabel='Read Noise', yunit='DN',bsave=True,directory_save=self.directory_analysis)
        Noise_shot = numpy.array(Noise_shot)


        # remove first element of numpy arrays (which should correspond to dark)
        self.Temporal_Noise = numpy.delete(self.Temporal_Noise,0,1)
        Noise_shot = numpy.delete(Noise_shot,0,1)
        self.Average = numpy.delete(self.Average,0,1)


        PlotTools.plot(numpy.log10(self.Average),numpy.log10(self.Temporal_Noise),xlabel="Log(Response)",xunit='Log(DN)',ylabel="Log(Noise)",yunit='Log(DN)',bfit=False,bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)

        PlotTools.plot(self.Average,self.Temporal_Noise**2,xlabel="Response",xunit='DN',ylabel="Noise^2",yunit='DN^2',bfit=False,bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)


        PlotTools.plot(self.Average,Noise_shot,xlabel="Response",xunit='DN',ylabel="Noise_shot",yunit='DN',bfit=False,bsave=True,directory_save=self.directory_analysis)

        if type(fitrange)==str:
            (offset_shot_loglog,slope_shot_loglog) = PlotTools.plot(numpy.log10(self.Average),numpy.log10(Noise_shot),xlabel="Log(Response)",xunit='Log(DN)',ylabel="Log(Noise_shot)",yunit='Log(DN)',bfit=bfit,fitrange=fitrange,bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)
        else:
            (offset_shot_loglog,slope_shot_loglog) = PlotTools.plot(numpy.log10(self.Average),numpy.log10(Noise_shot),xlabel="Log(Response)",xunit='Log(DN)',ylabel="Log(Noise_shot)",yunit='Log(DN)',bfit=bfit,fitrange=numpy.log10(fitrange),bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)

        (offset_shot,slope_shot) = PlotTools.plot(self.Average,Noise_shot**2,xlabel="Response",xunit='DN',ylabel="Noise_shot^2",yunit='DN^2',bfit=bfit,fitrange=fitrange,bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)

        print("slope_shot",slope_shot)
        print("slope_shot_loglog",slope_shot_loglog)

        if (None not in slope_shot) or (None not in slope_shot_loglog):

            fresults.write('Shot Noise LogLog slope: '+', '.join(str(v) for v in slope_shot_loglog)+'\n\n')
            PlotTools.plot_scatter(list(range(self.num_channel_groups)),slope_shot_loglog,xlabel='Group',ylabel='Slope shot LogLog', yunit=None,bsave=True,directory_save=self.directory_analysis)

            #conversion_gain = 1/numpy.array(slope)
            conversion_gain = 1/numpy.array(slope_shot)

            fresults.write('Conversion Gain: '+', '.join(str(v) for v in conversion_gain)+'\n\n')
            PlotTools.plot_scatter(list(range(self.num_channel_groups)),conversion_gain,xlabel='Group',ylabel='Conversion Gain', yunit='e/DN',bsave=True,directory_save=self.directory_analysis)

        fresults.close()
