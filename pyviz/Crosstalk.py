#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from . import Image
from . import ImageArray
from . import Measurement
from . import PlotTools

class Crosstalk(Measurement.Measurement):

    def set_channels(self,i_main_channel):
        # define dictionary for proper pixel positions given the main channel position (main channel position could be automatically determined from brightest channel - to be added)

        self.i_main_channel = i_main_channel

        if self.channel_groups!=(2,2):

            dict = {}

            for i_channel_group in range(self.num_channel_groups):
                dict[i_channel_group] = str(i_channel_group)

            self.i_horizontal_channel = 1
            self.i_vertical_channel = 4
            self.i_diagonal_channel = 5

            return dict

            #strout = "Crosstalk analysis can only be performed on 2x2 group channels for now. It is wrongly set at "+self.channel_groups+" in current analysis. Change it!"
            #raise Exception(strout)

        if self.i_main_channel==0:
            self.i_horizontal_channel = 1
            self.i_vertical_channel = 2
            self.i_diagonal_channel = 3
        elif self.i_main_channel==1:
            self.i_horizontal_channel = 0
            self.i_vertical_channel = 3
            self.i_diagonal_channel = 2
        elif self.i_main_channel==2:
            self.i_horizontal_channel = 3
            self.i_vertical_channel = 0
            self.i_diagonal_channel = 1
        elif self.i_main_channel==3:
            self.i_horizontal_channel = 2
            self.i_vertical_channel = 1
            self.i_diagonal_channel = 0
        else:
            raise Exception("wrong i_main_channel. Only 0,1,2 or 3 currently accepted")

        return {self.i_main_channel:"main",self.i_horizontal_channel:"horizontal",self.i_vertical_channel:"vertical",self.i_diagonal_channel:"diagonal"}

    def analyze_crosstalk(self,i_main_channel=0,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=68,directory_suffix=None,bsave=True,bfullresolution=False,blog=False):

        print("\nStarting CrossTalk analysis")

        self.create_analysis_directory(directory_suffix)

        channel_names = self.set_channels(i_main_channel)

        Average = [[] for i in range(self.num_channel_groups)]
        RMS = [[] for i in range(self.num_channel_groups)]
        xtalk_ratio = []
        xtalk_ratio_rms = []

        Xtalk={}
        Xtalk_rms={}
        for i_channel_group in range(self.num_channel_groups):            
            Xtalk[channel_names[i_channel_group]] = []
            Xtalk_rms[channel_names[i_channel_group]] = []
        

        fname_results = os.path.join(self.directory_analysis,'xtalk_results.txt')
        fresults = open(fname_results,'w')

        for i in range(len(self.param)):

            param_dir = os.path.join(self.directory_analysis,str(self.param[i]))

            if bsave and not(os.path.exists(param_dir)):
                os.mkdir(param_dir)
                
            fresults.write('%s\n'%str(self.param[i]))

            # ROI image + histogram (raw)
            if bsave:
                self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_raw_%s.png'%str(self.param[i])))
                self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_raw_%s.png'%str(self.param[i])))

            # Offset subtraction:
            if self.file_wildcard_offset!=None:

                # ROI image + histogram of offset image
                if bsave:
                    self.Image_offset[i].plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_offset_%s.png'%str(self.param[i])))
                    self.Image_offset[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_offset_%s.png'%str(self.param[i])))

                self.Image[i].subtract(self.Image_offset[i])

                if bsave:
                    # ROI image + histogram (dark subtracted)
                    #self.Image[i].plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(self.directory_analysis,'image.png'))
                    #self.Image[i].plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_%s.png'%str(self.param[i])))
                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_darksubtracted_%s.png'%str(self.param[i])))
                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_darksubtracted_%s.png'%str(self.param[i])))

            # FPN correction (not necessary if dark_subtraction is applied)
            if bFPN:

                fpn_correction_factors = self.Image_offset[i].calculate_FPN_correction()
                self.Image[i].apply_FPN_correction(fpn_correction_factors,bswap=False)

                if bsave:
                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_FPN_%s.png'%str(self.param[i])))
                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_FPN_%s.png'%str(self.param[i])))

            # RTN correction
            if bRTN:

                rtn_correction_factors = self.Image[i].calculate_RTN_correction(bswap=True,colstart=rtn_colstart,colstop=rtn_colstop)
                self.Image[i].apply_RTN_correction(rtn_correction_factors,bswap=True)

                if bsave:
                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_RTN_%s.png'%str(self.param[i])))
                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_RTN_%s.png'%str(self.param[i])))


            if bsave:
                self.Image[i].save2raw(filename=os.path.join(param_dir,'image_processed_%s.raw'%str(self.param[i])))

            Im_channels = []

            averages = self.Image[i].get_median_channel_groups()
            rms = self.Image[i].get_rms_channel_groups()

            for i_channel_group in range(self.num_channel_groups):

                Average[i_channel_group].append(averages[i_channel_group])
                RMS[i_channel_group].append(rms[i_channel_group])
                
                # Channel histogram with average + stddev
                if bsave:
                    self.Image[i].plot_histogram(channel=i_channel_group,bsigma=True,xmin=4,xmax=4,blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_%s_channel%i.png'%(str(self.param[i]),i_channel_group)),title='average = %.1f +/- %.1f'%(Average[i_channel_group][-1],RMS[i_channel_group][-1]))

                Im_channels.append(Image.Image(self.Image[i].get_array(i_channel_group=i_channel_group)))
                #Im_channels[i_channel_group].info()
                if bsave:
                    Im_channels[i_channel_group].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_channel%i_%s.png'%(i_channel_group,str(self.param[i]))))
                #Im_channels[i_channel_group].plot_image(minval=950,maxval=1050,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_channel%i_%s.png'%(i_channel_group,str(self.param[i]))))

                if bsave:
                    Im_channels[i_channel_group].save2raw(filename=os.path.join(param_dir,'image_channel%i_processed_%s.raw'%(i_channel_group,str(self.param[i]))))

                # offset images
                #im_offset = Image.Image(self.Image_offset[i].get_array(i_channel_group=i_channel_group))
                #im_offset.plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=bsave,filename=os.path.join(param_dir,'image_offset_channel%i_%s.png'%(i_channel_group,str(self.param[i]))))

            print("Average:",Average)
            print("RMS:",RMS)

            arr_stack = self.Image[i].get_array(bstack=True)
            Im_stack = Image.Image(arr_stack)
            if bsave:
                Im_stack.plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_stacked_%s.png'%str(self.param[i])))
                #Im_stack.plot_image(minval=0,maxval=1200,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_stacked_%s.png'%str(self.param[i])))

            # Xtalk computation

            for i_channel_group in range(self.num_channel_groups):

                if i_channel_group!=self.i_main_channel:

                    print("Computing Xtalk channel %i"%i_channel_group)

                    Im_channels[i_channel_group].divide(Im_channels[self.i_main_channel])
                    Im_channels[i_channel_group].multiply(100) # to have xtalk in percent

                    Xtalk[channel_names[i_channel_group]].append(Im_channels[i_channel_group].get_median())
                    Xtalk_rms[channel_names[i_channel_group]].append(Im_channels[i_channel_group].get_rms(minval=0,maxval=100))
                    
                    xtalk_str = '%s crosstalk = %.1f +/- %.1f%%'%(channel_names[i_channel_group],Xtalk[channel_names[i_channel_group]][i],Xtalk_rms[channel_names[i_channel_group]][i])
                    fresults.write('%s\n'%xtalk_str)

                    if bsave:
                        Im_channels[i_channel_group].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'heatmap_xtalk_%s_%s.png'%(channel_names[i_channel_group],str(self.param[i]))),title='%s crosstalk'%channel_names[i_channel_group])
                        #Im_channels[i_channel_group].plot_profile(axis=0,xlabel='column',ylabel='average crosstalk',bsave=True,filename=os.path.join(param_dir,'xprofile_xtalk_%s_%s.png'%(channel_names[i_channel_group],str(self.param[i]))),title='%s channel'%channel_names[i_channel_group])
                        #Im_channels[i_channel_group].plot_profile(axis=1,xlabel='row',ylabel='average crosstalk',bsave=True,filename=os.path.join(param_dir,'yprofile_xtalk_%s_%s.png'%(channel_names[i_channel_group],str(self.param[i]))),title='%s channel'%channel_names[i_channel_group])

                        Im_channels[i_channel_group].plot_histogram(bsigma=True,xmin=4,xmax=4,bsave=True,filename=os.path.join(param_dir,'hist_xtalk_%s_%s.png'%(channel_names[i_channel_group],str(self.param[i]))),xlabel='Crosstalk',title=xtalk_str)
                        #Im_channels[i_channel_group].plot_histogram(xmin=0,xmax=100,bsave=True,filename=os.path.join(param_dir,'hist_xtalk_%s_%s.png'%(channel_names[i_channel_group],str(self.param[i]))),xlabel='Crosstalk',title=xtalk_str)
                    
            # Plot stacked xtalk image:
            Im_channels[self.i_main_channel].divide(Im_channels[self.i_main_channel])
            Im_channels[self.i_main_channel].multiply(100)
            Im_xtalk = ImageArray.ImageArray(Im_channels)
            Im_xtalk_stacked = Im_xtalk.combine(shape=self.channel_groups)

            if bsave:
                Im_xtalk_stacked.plot_image(minval=0,maxval=100,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_xtalk_stacked_%s.png'%str(self.param[i])))

            #######################################
            # horizontal/vertical crosstalk ratio #
            #######################################

            i0 = self.i_horizontal_channel
            i1 = self.i_vertical_channel
            label_i0_i1 = '%s/%s xtalk'%(channel_names[i0],channel_names[i1])
            suffix_i0_i1 = '%s_vs_%s'%(channel_names[i0],channel_names[i1])
            
            Im_channels[i0].divide(Im_channels[i1])

            xtalk_ratio.append(Im_channels[i0].get_median())
            xtalk_ratio_rms.append(Im_channels[i0].get_rms())

            minval = xtalk_ratio[i] - 2 * xtalk_ratio_rms[i]
            maxval = xtalk_ratio[i] + 2 * xtalk_ratio_rms[i]
            if bsave:
                Im_channels[i0].plot_image(minval=minval,maxval=maxval,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'heatmap_xtalk_%s_%s.png'%(suffix_i0_i1,str(self.param[i]))),title=label_i0_i1)
                #Im_channels[i0].plot_profile(axis=0,xlabel='column',ylabel=label_i0_i1,bsave=True,filename=os.path.join(param_dir,'xprofile_xtalk_%s_%s.png'%(suffix_i0_i1,str(self.param[i]))))
                #Im_channels[i0].plot_profile(axis=1,xlabel='row',ylabel=label_i0_i1,bsave=True,filename=os.path.join(param_dir,'yprofile_xtalk_%s_%s.png'%(suffix_i0_i1,str(self.param[i]))))

            xmin = xtalk_ratio[i] - 4 * xtalk_ratio_rms[i]
            xmax = xtalk_ratio[i] + 4 * xtalk_ratio_rms[i]
            if bsave:
                Im_channels[i0].plot_histogram(xmin=xmin,xmax=xmax,bsave=True,filename=os.path.join(param_dir,'hist_xtalk_%s_%s.png'%(suffix_i0_i1,str(self.param[i]))),xlabel=label_i0_i1,title='Median = %.1f +/- %.1f'%(xtalk_ratio[i],xtalk_ratio_rms[i]))

            fresults.write('\n')

        fresults.close()

        #########################
        # Plot results vs param #
        #########################

        PlotTools.plot([self.param]*self.num_channel_groups,Average,error=RMS,xlabel=self.param_label,xunit=self.param_unit,ylabel='Average',yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=2)

        for i_channel_group in range(self.num_channel_groups):
            if i_channel_group!=self.i_main_channel:
                PlotTools.plot([self.param],[Xtalk[channel_names[i_channel_group]]],error=[Xtalk_rms[channel_names[i_channel_group]]],xlabel=self.param_label,xunit=self.param_unit,ylabel='%s crosstalk'%channel_names[i_channel_group],yunit='%',bsave=True,directory_save=self.directory_analysis,linewidth=2)
                #PlotTools.plot([self.param],[Xtalk[channel_names[i_channel_group]]],error=[Xtalk_rms[channel_names[i_channel_group]]],xlabel=self.param_label,xunit=self.param_unit,ylabel='%s crosstalk'%channel_names[i_channel_group],yunit='%',bsave=True,directory_save=self.directory_analysis,yrange=(0,100),linewidth=2)

        PlotTools.plot([self.param],[xtalk_ratio],error=[xtalk_ratio_rms],xlabel=self.param_label,xunit=self.param_unit,ylabel='crosstalk ratio',yunit='horizontal/vertical',bsave=True,directory_save=self.directory_analysis,linewidth=2)
