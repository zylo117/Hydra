#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
from . import Image
from . import Measurement

class ReadNoise(Measurement.Measurement):


    def __init__(self,directory, file_wildcard='image_%s_*.raw', rows=3000, columns=4000, datatype='uint16', param=[''], param2=None, num_skip_files=0, num_files='all', num_files_ref=0, bfullnoise=False, b_load_all=False, param_label='default', param_unit=None, param_cal=None, param_cal_label=None, param_cal_unit=None, param_label2=None, param_unit2=None, param_cal2=None, param_cal_label2=None, param_cal_unit2=None, channel_groups=(1,8), show_channels=None, roi=None, nbins=100, file_wildcard_offset=None,num_files_offset='all',bswap=False, conditions='default'):

        #if bfullnoise:
        self.bfullnoise = bfullnoise
        Measurement.Measurement.__init__(self,
                                         directory, 
                                         file_wildcard=file_wildcard, 
                                         rows=rows, columns=columns, 
                                         datatype=datatype, 
                                         param=param,
                                         param2 = param2,
                                         num_skip_files=num_skip_files, 
                                         num_files=num_files, 
                                         num_files_ref=num_files_ref, 
                                         b_load_all=b_load_all,
                                         param_label=param_label, 
                                         param_unit=param_unit, 
                                         param_label2=param_label2, 
                                         param_unit2=param_unit2, 
                                         param_cal=param_cal, 
                                         param_cal_label=param_cal_label, 
                                         param_cal_unit=param_cal_unit, 
                                         param_cal2=param_cal2, 
                                         param_cal_label2=param_cal_label2, 
                                         param_cal_unit2=param_cal_unit2,
                                         channel_groups=channel_groups, 
                                         show_channels=show_channels, 
                                         roi=roi, 
                                         nbins=nbins, 
                                         file_wildcard_offset=file_wildcard_offset,
                                         num_files_offset=num_files_offset,
                                         bswap=bswap,
                                         conditions=conditions)
        '''
        else:
            Measurement.Measurement.__init__(self,
                                             directory, 
                                             file_wildcard=file_wildcard, 
                                             rows=rows, columns=columns, 
                                             datatype=datatype, 
                                             param=param, 
                                             param2=param2, 
                                             num_skip_files=num_skip_files, 
                                             num_files=num_files, 
                                             num_files_ref=num_files_ref, 
                                             b_load_all=b_load_all, 
                                             param_label=param_label, 
                                             param_unit=param_unit, 
                                             param_cal=param_cal, 
                                             param_label2=param_label2, 
                                             param_unit2=param_unit2, 
                                             param_cal_label=param_cal_label, 
                                             param_cal_unit=param_cal_unit, 
                                             param_cal2=param_cal2, 
                                             param_cal_label2=param_cal_label2, 
                                             param_cal_unit2=param_cal_unit2,
                                             channel_groups=channel_groups, 
                                             show_channels=show_channels, 
                                             roi=roi, 
                                             nbins=nbins, 
                                             file_wildcard_offset=file_wildcard_offset,
                                             num_files_offset=num_files_offset,
                                             bswap=bswap,
                                             conditions=conditions)
        '''

    def analyze_readnoise(self, bFPN=False, bRTN=False, bsave=True, blog=False, directory_suffix='',linewidth=2.5,bfit=False,fitrange=None,bfullresolution=False,rotation_xlabel=0):

        self.analyze(bFPN=bFPN,bRTN=bRTN,bsave=bsave,blog=blog,bfullresolution=bfullresolution,directory_suffix=directory_suffix,bfullnoise=self.bfullnoise)

        if self.param2 is None:
            self.plot_vs_param(bfit=bfit,fitrange=fitrange,linewidth=linewidth,bfullnoise=self.bfullnoise,rotation_xlabel=rotation_xlabel)
        else:
            self.plot_vs_param_2D(rotation_xlabel=rotation_xlabel,colorscale='jet')


        if self.bfullnoise:

            fname_results = os.path.join(self.directory_analysis,'noise_results.txt')

            if self.param2 is None:
                self.create_txt_output(fname_results)
            else:
                self.create_txt_output_2D(fname_results)

            fname_results_csv = os.path.join(self.directory_analysis,'noise_results_%s.csv'%self.conditions)
            self.create_csv_output(fname_results_csv)
            if self.b_load_all:
                fname_results_csv2 = os.path.join(self.directory_analysis,'analysis2','noise_results2_%s.csv'%self.conditions)
                self.create_csv_output(fname_results_csv2,bmethod=2)

            if bsave:

                for i in range(len(self.param)):
                    param_dir = os.path.join(self.directory_analysis,str(self.param[i]))
                    arr_stack = self.Image[i].get_array(bstack=True)
                    Im_stack = Image.Image(arr_stack)
                    
                    #Im_stack.plot_image(bfullresolution=False,bsave=True,filename=os.path.join(param_dir,'image_RTNcorrected_AfterReferenceSubtraction_stacked_%s.png'%str(self.param[i])))
                    Im_stack.plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'im_AfterRefSub_stacked_%s.png'%str(self.param[i])))
                    #Im_stack.plot_image(bfullresolution=False,bsave=True,minval=-40,maxval=40,filename=os.path.join(param_dir,'im_AfterRefSub_stacked_%s.png'%str(self.param[i])))


    def analyze_rownoise(self,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=67,bsave=False,blog=False,bfullresolution=False,directory_suffix=None):

        self.create_analysis_directory(directory_suffix)

        for i in range(len(self.param)):
            self.Image[i].subtract(self.Image_ref[i])

        self.postprocessing(bsave=bsave,directory=self.directory_analysis,bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop,bfullresolution=bfullresolution,blog=blog)
