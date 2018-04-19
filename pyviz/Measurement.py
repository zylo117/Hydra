#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy
import glob

from . import Image
from . import ImageArray
from . import PlotTools

class Measurement(object):

    '''
    Class to analyze data set where one parameter has been being scanned
    '''

    def __init__(self,directory, file_wildcard='image_%s_*.raw', rows=3000, columns=4000, datatype='uint16', param=[''], param2=None, num_skip_files=0, num_files='all', num_files_ref=0, b_load_all=False, param_label='default', param_unit=None, param_cal=None, param_cal_label=None, param_cal_unit=None, param_label2=None, param_unit2=None, param_cal2=None, param_cal_label2=None, param_cal_unit2=None, channel_groups=(1,8), show_channels=None, roi=None, nbins=100, file_wildcard_offset=None,num_files_offset='all',bswap=False, conditions='default'):

        self.directory = directory
        self.file_wildcard = os.path.join(self.directory,file_wildcard)
        self.param = param
        self.param2 = param2
        self.num_skip_files = num_skip_files
        self.num_files_ref = num_files_ref
        self.num_files = num_files
        self.param_label = param_label
        self.param_unit = param_unit
        self.param_label2 = param_label2
        self.param_unit2 = param_unit2

        # 1st parameter:
        if param_cal==None:
            self.param_cal = self.param
        else:
            self.param_cal = param_cal

        if param_cal_label==None:
            self.param_cal_label = self.param_label
        else:
            self.param_cal_label = param_cal_label

        if param_cal_unit==None:
            self.param_cal_unit = self.param_unit
        else:
            self.param_cal_unit = param_cal_unit

        # 2nd parameter
        if param_cal2==None:
            self.param_cal2 = self.param2
        else:
            self.param_cal2 = param_cal2


        if param_cal_label2==None:
            self.param_cal_label2 = self.param_label2
        else:
            self.param_cal_label2 = param_cal_label2

        if param_cal_unit2==None:
            self.param_cal_unit2 = self.param_unit2
        else:
            self.param_cal_unit2 = param_cal_unit2

        self.channel_groups = channel_groups
        self.num_channel_groups = self.channel_groups[0]*self.channel_groups[1]
        
        self.show_channels = show_channels
        self.nbins = nbins

        if file_wildcard_offset!=None:
            self.file_wildcard_offset = os.path.join(self.directory,file_wildcard_offset)
            self.num_files_offset = num_files_offset
        else:
            self.file_wildcard_offset = None

        self.b_load_all = b_load_all

        if self.param2 is None:
            self.load_data(rows,columns,datatype,roi=roi)
        else:
            self.load_data_2D(rows,columns,datatype,roi=roi)

        if bswap:
            self.column_swap()

        self.conditions = conditions


    def info(self):
        print("Directory: %s"%self.directory)
        print("Number of reference files: %i"%self.num_files_ref)
        print("Number of files: %i"%self.num_files)
        print("Offset wildcard:",self.file_wildcard_offset)


    def param_names(self,i):

        if self.param2 is None:
            return str(self.param[i])
        else:
            return str(self.param[i%len(self.param)])+'_'+str(self.param2[int(i/len(self.param))])


    def load_data(self,rows,columns,datatype,roi=None):

        ########################
        # Loading offset files #
        ########################

        if self.file_wildcard_offset != None:
            
            print("Loading offset files")
            
            self.Image_offset = []
            
            for i in range(len(self.param)):

                print("Loading %s"%str(self.param[i]))
                if '%s' not in self.file_wildcard_offset:
                    wildcard_offset = self.file_wildcard_offset
                else:
                    wildcard_offset = self.file_wildcard_offset%str(self.param[i])

                if i==0 or ('%s' in self.file_wildcard_offset):

                    print("Wildcard offset: %s"%wildcard_offset)
                    rawfiles_offset = glob.glob(wildcard_offset)
                    print("%i offset files found:"%(len(rawfiles_offset)),rawfiles_offset)
                    
                    # trim down number of offset files used:
                    if self.num_files_offset=='all':
                        num_files_offset = len(rawfiles_offset)
                    else:
                        num_files_offset = self.num_files_offset
                    rawfiles_offset = rawfiles_offset[:num_files_offset]
                    print("%i offset file(s) used:"%(len(rawfiles_offset)),rawfiles_offset)

                    self.Image_offset.append(ImageArray.ImageArray(rawfiles_offset,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

                else:

                    print("using same offset file as for %s"%str(self.param[0]))
                    self.Image_offset.append(self.Image_offset[0])

                self.Image_offset[i].set_ROI(roi)


        #######################
        # Loading data images #
        #######################

        self.Image = []
        self.Image_ref = []
        if self.b_load_all: self.Images = []
        
        for i in range(len(self.param)):

            print("Loading %s"%str(self.param[i]))

            wildcard = self.file_wildcard%str(self.param[i])
            print("Wildcard: %s"%wildcard)
            rawfiles = glob.glob(wildcard)
            print("%i files found:"%(len(rawfiles)),rawfiles)
            if len(rawfiles)==0:
                raise Exception("no files found for parameter: ",self.param[i])

            # Load main and reference files:

            rawfiles_ref = rawfiles[self.num_skip_files:self.num_skip_files+self.num_files_ref]

            if self.num_files=='all':
                self.num_files = len(rawfiles) - self.num_skip_files - self.num_files_ref
            rawfiles_main = rawfiles[self.num_skip_files+self.num_files_ref:self.num_skip_files+self.num_files_ref+self.num_files]

            print("%i reference file(s) used:"%(len(rawfiles_ref)),rawfiles_ref)
            print("%i main file(s) used:"%(len(rawfiles_main)),rawfiles_main)

            self.Image_ref.append(ImageArray.ImageArray(rawfiles_ref,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

            self.Image.append(ImageArray.ImageArray(rawfiles_main,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

            if self.b_load_all:
                self.Images.append(ImageArray.ImageArray(rawfiles,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups))

            if self.Image_ref[i]!=None:
                self.Image_ref[i].set_ROI(roi)
            self.Image[i].set_ROI(roi)
            if self.b_load_all:
                self.Images[i].set_ROI(roi)

            print()


    def load_data_2D(self,rows,columns,datatype,roi=None):

        ########################
        # Loading offset files #
        ########################

        if self.file_wildcard_offset != None:
            
            print("Loading offset files")
            
            self.Image_offset = []
            
            for i2 in range(len(self.param2)):

                for i in range(len(self.param)):

                    print("Loading %s / %s"%(str(self.param[i]),str(self.param2[i2])))
                    if '%s' not in self.file_wildcard_offset:
                        wildcard_offset = self.file_wildcard_offset
                    else:
                        wildcard_offset = self.file_wildcard_offset%(str(self.param[i]),str(self.param2[i2]))

                    if (i2==0 and i==0) or ('%s' in self.file_wildcard_offset):

                        print("Wildcard offset: %s"%wildcard_offset)
                        rawfiles_offset = glob.glob(wildcard_offset)
                        print("%i offset files found:"%(len(rawfiles_offset)),rawfiles_offset)

                        # trim down number of offset files used:
                        if self.num_files_offset=='all':
                            num_files_offset = len(rawfiles_offset)
                        else:
                            num_files_offset = self.num_files_offset
                        rawfiles_offset = rawfiles_offset[:num_files_offset]
                        print("%i offset file(s) used:"%(len(rawfiles_offset)),rawfiles_offset)

                        self.Image_offset.append(ImageArray.ImageArray(rawfiles_offset,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

                    else:

                        print("using same offset file as for i==%s and i2=="%(str(self.param[0]),str(self.param2[0])))
                        self.Image_offset.append(self.Image_offset[0])

                    self.Image_offset[i2*len(self.param)+i].set_ROI(roi)


        #######################
        # Loading data images #
        #######################

        self.Image = []
        self.Image_ref = []
        if self.b_load_all: self.Images = []
        
        for i2 in range(len(self.param2)):

            for i in range(len(self.param)):

                print("Loading %s / %s"%(str(self.param[i]),str(self.param2[i2])))

                wildcard = self.file_wildcard%(str(self.param[i]),str(self.param2[i2]))
                print("Wildcard: %s"%wildcard)
                rawfiles = glob.glob(wildcard)
                print("%i files found:"%(len(rawfiles)),rawfiles)
                if len(rawfiles)==0:
                    raise Exception("no files found for parameters: %s/%s"%(self.param[i],self.param2[i2]))

                # Load main and reference files:

                rawfiles_ref = rawfiles[self.num_skip_files:self.num_skip_files+self.num_files_ref]

                if self.num_files=='all':
                    self.num_files = len(rawfiles) - self.num_skip_files - self.num_files_ref
                rawfiles_main = rawfiles[self.num_skip_files+self.num_files_ref:self.num_skip_files+self.num_files_ref+self.num_files]

                print("%i reference file(s) used:"%(len(rawfiles_ref)),rawfiles_ref)
                print("%i main file(s) used:"%(len(rawfiles_main)),rawfiles_main)

                self.Image_ref.append(ImageArray.ImageArray(rawfiles_ref,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

                self.Image.append(ImageArray.ImageArray(rawfiles_main,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups).average())

                if self.b_load_all:
                    self.Images.append(ImageArray.ImageArray(rawfiles,rows=rows,columns=columns,datatype=datatype,channel_groups=self.channel_groups))

                if self.Image_ref[i2*len(self.param)+i]!=None:
                    self.Image_ref[i2*len(self.param)+i].set_ROI(roi)
                self.Image[i2*len(self.param)+i].set_ROI(roi)
                if self.b_load_all:
                    self.Images[i2*len(self.param)+i].set_ROI(roi)

                print()


    def column_swap(self):
        
        for i in range(len(self.Image)):

            if self.file_wildcard_offset != None:
                self.Image_offset[i].column_swap()
            if self.Image_ref[i]!=None:
                self.Image_ref[i].column_swap()

            self.Image[i].column_swap()

            if self.b_load_all:
                self.Images[i].column_swap()


    def offset_subtraction(self, bsave=False, blog=False, directory=None, bfullresolution=False):

        if self.file_wildcard_offset != None:

            for i in range(len(self.Image)):

                if bsave:
                    # ROI image + histogram of offset image
                    self.Image_offset[i].plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(directory,'image_offset_%s.png'%self.param_names(i)))
                    self.Image_offset[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(directory,'hist_offset_%s.png'%self.param_names(i)))

                if self.num_files_ref>0:
                    self.Image_ref[i].subtract(self.Image_offset[i])

                self.Image[i].subtract(self.Image_offset[i])

                if self.b_load_all:
                    self.Images[i].subtract(self.Image_offset[i])

                if bsave:
                    # ROI image + histogram (dark subtracted)
                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(directory,'image_darksubtracted_%s.png'%self.param_names(i)))
                    if self.num_files_ref>0:
                        self.Image_ref[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(directory,'image_ref_darksubtracted_%s.png'%self.param_names(i)))
                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(directory,'hist_darksubtracted_%s.png'%self.param_names(i)))


            print("Offset subtraction performed")

        else:
            raise Exception("Offset subtraction cannot be performed because no file_wildcard_offset was provided")



    def postprocessing(self,bsave=False,blog=False,bfullresolution=False,directory=None,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=67):

        ##############################################
        # Save image/historam before post-processing #
        ##############################################

        for i in range(len(self.Image)):

            print("\n*** Processing %s ***"%self.param_names(i))

            param_dir = os.path.join(directory,self.param_names(i))
            if bsave:
                
                if not(os.path.exists(param_dir)):
                    os.mkdir(param_dir)

                # ROI image + histogram (nonprocessed)
                self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_raw_%s.png'%self.param_names(i)))
                if self.num_files_ref>0:
                    self.Image_ref[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_ref_raw_%s.png'%self.param_names(i)))

                self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_raw_%s.png'%self.param_names(i)))

                arr_stack = self.Image[i].get_array(bstack=True)
                Im_stack = Image.Image(arr_stack)
                Im_stack.plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_stacked_%s.png'%self.param_names(i)))

        ######################
        # Offset subtraction #
        ######################

        if self.file_wildcard_offset != None:
            self.offset_subtraction(bsave=bsave, blog=blog, directory=param_dir, bfullresolution=bfullresolution)

        #######################
        # RTN/FPN corrections #
        #######################

        for i in range(len(self.Image)):

            # FPN correction (not necessary if dark_subtraction is applied)
            if bFPN:

                self.Image[i].FPN_correction(bswap=False)

                if self.num_files_ref>0:
                    self.Image_ref[i].FPN_correction(bswap=False)

                if self.b_load_all:
                    self.Images[i].FPN_correction(bswap=False)

                if bsave:
                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_FPNcorrected_%s.png'%self.param_names(i)))
                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_FPNcorrected_%s.png'%self.param_names(i)))

            # RTN correction
            if bRTN:

                rtn_correction_factors = self.Image[i].RTN_correction(bswap=False,colstart=rtn_colstart,colstop=rtn_colstop,bsave=bsave,filename=os.path.join(param_dir,'RTN_profiles.png'))
                print('RTN noise:',self.Image[i].rtn_noise)

                if self.num_files_ref>0:
                    rtn_correction_factors = self.Image_ref[i].RTN_correction(bswap=False,colstart=rtn_colstart,colstop=rtn_colstop,bsave=bsave,filename=os.path.join(param_dir,'RTN_profiles_ref.png'))
                    print('RTN noise ref:',self.Image[i].rtn_noise)

                if self.b_load_all:
                    rtn_correction_factors = self.Images[i].RTN_correction(bswap=False,colstart=rtn_colstart,colstop=rtn_colstop,bsave=bsave,filename=os.path.join(param_dir,'RTN_profiles_ref.png'))


                if bsave:

                    self.Image[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_RTNcorrected_%s.png'%self.param_names(i)))

                    arr_stack = self.Image[i].get_array(bstack=True)
                    Im_stack = Image.Image(arr_stack)
                    Im_stack.plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_RTNcorrected_stacked_%s.png'%self.param_names(i)))

                    if self.num_files_ref>0:
                        self.Image_ref[i].plot_image(bsigma=True,minval=2,maxval=2,bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_ref_RTNcorrected_%s.png'%self.param_names(i)))
                        arr_stack = self.Image_ref[i].get_array(bstack=True)
                        Im_stack = Image.Image(arr_stack)
                        Im_stack.plot_image(bfullresolution=bfullresolution,bsave=True,filename=os.path.join(param_dir,'image_ref_RTNcorrected_stacked_%s.png'%self.param_names(i)))

                    self.Image[i].plot_histogram(blog=blog,bsave=True,filename=os.path.join(param_dir,'hist_RTNcorrected_%s.png'%self.param_names(i)))


            #if bsave:
            #    self.Image[i].save2raw(filename=os.path.join(param_dir,'image_postprocessed_%s.raw'%self.param_names(i)))


    def create_analysis_directory(self,directory_suffix=None):

        if directory_suffix==None:
            dir_ana = "Analysis"
        else:
            dir_ana = "Analysis_%s"%directory_suffix

        self.directory_analysis = os.path.join(self.directory,dir_ana)
        if not(os.path.exists(self.directory_analysis)):
            os.mkdir(self.directory_analysis)


    def create_txt_output(self,filename):

        fresults = open(filename,'w')

        for i in range(len(self.param)):

            fresults.write('**************************\n')
            fresults.write('Param #%i: %s\n'%(i,str(self.param[i])))
            fresults.write('**************************\n\n')

            for i_channel_group in range(self.num_channel_groups):

                fresults.write('--------------------------\n')
                fresults.write('Channel %i\n'%i_channel_group)
                fresults.write('--------------------------\n')
                
                fresults.write('total noise = %.2f DN\n'%(self.Total_noise[i_channel_group][i]))
                fresults.write('row noise = %.2f DN\n'%(self.Row_noise[i_channel_group][i]))
                fresults.write('column noise = %.2f DN\n'%(self.Column_noise[i_channel_group][i]))
                fresults.write('pixel noise = %.2f DN\n'%(self.Pixel_noise[i_channel_group][i]))
                
                fresults.write('------------\n')
                
                fresults.write('total temporal noise = %.2f DN\n'%(self.Total_temporal_noise[i_channel_group][i]))
                fresults.write('row temporal noise = %.2f DN\n'%(self.Row_temporal_noise[i_channel_group][i]))
                fresults.write('column temporal noise = %.2f DN\n'%(self.Column_temporal_noise[i_channel_group][i]))
                fresults.write('pixel temporal noise = %.2f DN\n'%(self.Pixel_temporal_noise[i_channel_group][i]))
                
                fresults.write('------------\n')
                
                fresults.write('total fixed pattern noise = %.2f DN\n'%(self.Total_fixed_pattern_noise[i_channel_group][i]))
                fresults.write('row fixed pattern noise = %.2f DN\n'%(self.Row_fixed_pattern_noise[i_channel_group][i]))
                fresults.write('column fixed pattern noise = %.2f DN\n'%(self.Column_fixed_pattern_noise[i_channel_group][i]))
                fresults.write('pixel fixed pattern noise = %.2f DN\n'%(self.Pixel_fixed_pattern_noise[i_channel_group][i]))

                fresults.write('--------------------------\n\n')

            fresults.write('\n')

        fresults.close()


    def create_txt_output_2D(self,filename):

        fresults = open(filename,'w')

        for i in range(len(self.param)):

            for j in range(len(self.param2)):

                fresults.write('**************************\n')
                fresults.write('Param #%i: %s/%s\n'%(i,str(self.param[i]),str(self.param2[j])))
                fresults.write('**************************\n\n')

                for i_channel_group in range(self.num_channel_groups):

                    fresults.write('--------------------------\n')
                    fresults.write('Channel %i\n'%i_channel_group)
                    fresults.write('--------------------------\n')
                    
                    fresults.write('total noise = %.2f DN\n'%(self.Total_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('row noise = %.2f DN\n'%(self.Row_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('column noise = %.2f DN\n'%(self.Column_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('pixel noise = %.2f DN\n'%(self.Pixel_noise[i_channel_group][j*len(self.param)+i]))

                    fresults.write('------------\n')

                    fresults.write('total temporal noise = %.2f DN\n'%(self.Total_temporal_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('row temporal noise = %.2f DN\n'%(self.Row_temporal_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('column temporal noise = %.2f DN\n'%(self.Column_temporal_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('pixel temporal noise = %.2f DN\n'%(self.Pixel_temporal_noise[i_channel_group][j*len(self.param)+i]))

                    fresults.write('------------\n')

                    fresults.write('total fixed pattern noise = %.2f DN\n'%(self.Total_fixed_pattern_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('row fixed pattern noise = %.2f DN\n'%(self.Row_fixed_pattern_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('column fixed pattern noise = %.2f DN\n'%(self.Column_fixed_pattern_noise[i_channel_group][j*len(self.param)+i]))
                    fresults.write('pixel fixed pattern noise = %.2f DN\n'%(self.Pixel_fixed_pattern_noise[i_channel_group][j*len(self.param)+i]))

                    fresults.write('--------------------------\n\n')

                fresults.write('\n')

        fresults.close()


    def create_csv_output(self,filename,bmethod=1):

        fresults = open(filename,'w')

        fresults.write('Conditions, %s, Channel, Response, TN, RN, CN, PN, TTN, RTN, CTN, PTN, TFPN, RFPN, CFPN, PFPN\n'%(self.param_label))

        for i in range(len(self.param)):
            for i_channel_group in range(self.num_channel_groups):

                if bmethod==1:
                    fresults.write('%s, '%self.conditions +
                                   '%s, '%str(self.param[i]) +
                                   '%i ,'%i_channel_group +
                                   '%s ,'%('' if numpy.isnan(self.Average[i_channel_group][i]) else '%.2f'%self.Average[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_noise[i_channel_group][i]) else '%.2f'%self.Total_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_noise[i_channel_group][i]) else '%.2f'%self.Row_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_noise[i_channel_group][i]) else '%.2f'%self.Column_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Pixel_noise[i_channel_group][i]) else '%.2f'%self.Pixel_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_temporal_noise[i_channel_group][i]) else '%.2f'%self.Total_temporal_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_temporal_noise[i_channel_group][i]) else '%.2f'%self.Row_temporal_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_temporal_noise[i_channel_group][i]) else '%.2f'%self.Column_temporal_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Pixel_temporal_noise[i_channel_group][i]) else '%.2f'%self.Pixel_temporal_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_fixed_pattern_noise[i_channel_group][i]) else '%.2f'%self.Total_fixed_pattern_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_fixed_pattern_noise[i_channel_group][i]) else '%.2f'%self.Row_fixed_pattern_noise[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_fixed_pattern_noise[i_channel_group][i]) else '%.2f'%self.Column_fixed_pattern_noise[i_channel_group][i]) +
                                   '%s'%('' if numpy.isnan(self.Pixel_fixed_pattern_noise[i_channel_group][i]) else '%.2f'%self.Pixel_fixed_pattern_noise[i_channel_group][i]) +
                                   '\n')
                elif bmethod==2:
                    fresults.write('%s, '%self.conditions +
                                   '%s, '%str(self.param[i]) +
                                   '%i ,'%i_channel_group +
                                   '%s ,'%('' if numpy.isnan(self.Average[i_channel_group][i]) else '%.2f'%self.Average[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_noise2[i_channel_group][i]) else '%.2f'%self.Total_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_noise2[i_channel_group][i]) else '%.2f'%self.Row_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_noise2[i_channel_group][i]) else '%.2f'%self.Column_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Pixel_noise2[i_channel_group][i]) else '%.2f'%self.Pixel_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_temporal_noise2[i_channel_group][i]) else '%.2f'%self.Total_temporal_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_temporal_noise2[i_channel_group][i]) else '%.2f'%self.Row_temporal_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_temporal_noise2[i_channel_group][i]) else '%.2f'%self.Column_temporal_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Pixel_temporal_noise2[i_channel_group][i]) else '%.2f'%self.Pixel_temporal_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Total_fixed_pattern_noise2[i_channel_group][i]) else '%.2f'%self.Total_fixed_pattern_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Row_fixed_pattern_noise2[i_channel_group][i]) else '%.2f'%self.Row_fixed_pattern_noise2[i_channel_group][i]) +
                                   '%s ,'%('' if numpy.isnan(self.Column_fixed_pattern_noise2[i_channel_group][i]) else '%.2f'%self.Column_fixed_pattern_noise2[i_channel_group][i]) +
                                   '%s'%('' if numpy.isnan(self.Pixel_fixed_pattern_noise2[i_channel_group][i]) else '%.2f'%self.Pixel_fixed_pattern_noise2[i_channel_group][i]) +
                                   '\n')


        fresults.close()


    def analyze(self,bFPN=False,bRTN=False,rtn_colstart=4,rtn_colstop=67,bsave=False,blog=False,bfullresolution=False,directory_suffix=None,bnoise=True,bfullnoise=False):

        # Average, Noise, and Offset will be computed from data measurement as a function of parameter scanned
        # results are stored in numpy arrays: self.Average, self.Noise, self.Offset

        print("\nStarting ANALYSIS")

        self.create_analysis_directory(directory_suffix)

        self.postprocessing(bsave=bsave,directory=self.directory_analysis,bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop,bfullresolution=bfullresolution,blog=blog)

        Average = []
        Total_Noise = []
        Temporal_Noise = []
        Offset = []

        if bfullnoise:

            Total_noise = []
            Row_noise = []
            Column_noise = []
            Column_noise_minmax = []
            Pixel_noise = []

            Total_temporal_noise = []
            Row_temporal_noise = []
            Column_temporal_noise = []
            Pixel_temporal_noise = []

            Total_fixed_pattern_noise = []
            Row_fixed_pattern_noise = []
            Column_fixed_pattern_noise = []
            Pixel_fixed_pattern_noise = []

            Total_noise2 = []
            Row_noise2 = []
            Column_noise2 = []
            Pixel_noise2 = []

            Total_temporal_noise2 = []
            Row_temporal_noise2 = []
            Column_temporal_noise2 = []
            Pixel_temporal_noise2 = []

            Total_fixed_pattern_noise2 = []
            Row_fixed_pattern_noise2 = []
            Column_fixed_pattern_noise2 = []
            Pixel_fixed_pattern_noise2 = []

        for i_channel_group in range(self.num_channel_groups):

            Average.append([])
            Total_Noise.append([])
            Temporal_Noise.append([])
            Offset.append([])

            if bfullnoise:

                Total_noise.append([])
                Row_noise.append([])
                Column_noise.append([])
                Column_noise_minmax.append([])
                Pixel_noise.append([])
                
                Total_temporal_noise.append([])
                Row_temporal_noise.append([])
                Column_temporal_noise.append([])
                Pixel_temporal_noise.append([])
                
                Total_fixed_pattern_noise.append([])
                Row_fixed_pattern_noise.append([])
                Column_fixed_pattern_noise.append([])
                Pixel_fixed_pattern_noise.append([])

                Total_noise2.append([])
                Row_noise2.append([])
                Column_noise2.append([])
                Pixel_noise2.append([])
                
                Total_temporal_noise2.append([])
                Row_temporal_noise2.append([])
                Column_temporal_noise2.append([])
                Pixel_temporal_noise2.append([])
                
                Total_fixed_pattern_noise2.append([])
                Row_fixed_pattern_noise2.append([])
                Column_fixed_pattern_noise2.append([])
                Pixel_fixed_pattern_noise2.append([])

        for i in range(len(self.Image)):

            print("Analyzing %s"%self.param_names(i))

            if bsave:

                param_dir = os.path.join(self.directory_analysis,self.param_names(i))
                if not(os.path.exists(param_dir)):
                    os.mkdir(param_dir)

                if bnoise:
                    # Creating histogram/image for average reference image
                    filename = os.path.join(param_dir,"hist_%s_ref.png"%self.param_names(i))
                    self.Image_ref[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins=self.nbins,bsave=True,filename=filename)
                    #self.Image_ref[i].plot_image()

                # Create histogram/image for main image
                filename = os.path.join(param_dir,"hist_%s_main.png"%self.param_names(i))
                self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins=self.nbins,bsave=True,filename=filename)
                #self.Image[i].plot_histogram(show_channels=self.show_channels,xmin=1200,xmax=1400,blog=blog,nbins=self.nbins,bsave=True,filename=filename)
                #self.Image[i].plot_image(bsave=True,filename=filename,dpi=500)

            # comment one of these two lines if you want to do a mean or median analysis
            averages = self.Image[i].get_mean_channel_groups()
            #averages = self.Image[i].get_median_channel_groups()
            if bnoise: total_noise = self.Image[i].get_rms_channel_groups()
            for i_channel_group in range(self.num_channel_groups):
                Average[i_channel_group].append(averages[i_channel_group])
                if bnoise: Total_Noise[i_channel_group].append(total_noise[i_channel_group])

            if bfullnoise:

                total_noise,row_noise,column_noise,pixel_noise = self.Image[i].get_noise()
                total_noise_minmax,row_noise_minmax,column_noise_minmax,pixel_noise_minmax = self.Image[i].get_noise(bminmax=True)
                for i_channel_group in range(self.num_channel_groups):
                    Total_noise[i_channel_group].append(total_noise[i_channel_group])
                    Row_noise[i_channel_group].append(row_noise[i_channel_group])
                    Column_noise[i_channel_group].append(column_noise[i_channel_group])
                    Column_noise_minmax[i_channel_group].append(column_noise_minmax[i_channel_group])
                    Pixel_noise[i_channel_group].append(pixel_noise[i_channel_group])

                if self.b_load_all:
                    # Compute pixel temporal noise from *all* images
                    if bsave:
                        #total_fixed_pattern_noise2,row_fixed_pattern_noise2,column_fixed_pattern_noise2,pixel_fixed_pattern_noise2 = self.Images[i].get_noise(bsave=bsave,directory=param_dir)
                        total_fixed_pattern_noise2,row_fixed_pattern_noise2,column_fixed_pattern_noise2,pixel_fixed_pattern_noise2,total_temporal_noise2,row_temporal_noise2,column_temporal_noise2,pixel_temporal_noise2 = self.Images[i].get_noise(bsave=bsave,directory=param_dir)
                    else:
                        #total_fixed_pattern_noise2,row_fixed_pattern_noise2,column_fixed_pattern_noise2,pixel_fixed_pattern_noise2 = self.Images[i].get_noise()
                        total_fixed_pattern_noise2,row_fixed_pattern_noise2,column_fixed_pattern_noise2,pixel_fixed_pattern_noise2,total_temporal_noise2,row_temporal_noise2,column_temporal_noise2,pixel_temporal_noise2 = self.Images[i].get_noise()

                    for i_channel_group in range(self.num_channel_groups):

                        Total_temporal_noise2[i_channel_group].append(total_temporal_noise2[i_channel_group])
                        Row_temporal_noise2[i_channel_group].append(row_temporal_noise2[i_channel_group])
                        Column_temporal_noise2[i_channel_group].append(column_temporal_noise2[i_channel_group])
                        Pixel_temporal_noise2[i_channel_group].append(pixel_temporal_noise2[i_channel_group])

                        Total_fixed_pattern_noise2[i_channel_group].append(total_fixed_pattern_noise2[i_channel_group])
                        Row_fixed_pattern_noise2[i_channel_group].append(row_fixed_pattern_noise2[i_channel_group])
                        Column_fixed_pattern_noise2[i_channel_group].append(column_fixed_pattern_noise2[i_channel_group])
                        Pixel_fixed_pattern_noise2[i_channel_group].append(pixel_fixed_pattern_noise2[i_channel_group])


                if bsave:
                    # Create column profile for main image
                    filename = os.path.join(param_dir,"profile_column_%s_main.png"%self.param_names(i))
                    #self.Image[i].plot_profile(axis=0, show_channels=self.show_channels, ylim=(-200,800), bsave=True, filename=filename, ylabel="Col average: AZon - AZoff")
                    #self.Image[i].plot_profile(axis=0, show_channels=self.show_channels, ylim=None, bsave=True, filename=filename, ylabel="Col average: AZon - AZoff")
                    self.Image[i].plot_profile(axis=0, show_channels=self.show_channels, bsave=True, filename=filename)
                    #for i_channel in range(self.num_channel_groups):
                        #im_column_profile = self.Image[i].get_profile_image(axis=0,i_channel_group=i_channel)
                        #im_column_profile.save2raw(filename=os.path.join(param_dir,'image_column_profile_%s_channel%i.raw'%(self.param_names(i),i_channel)))
                        #im_column_profile.save2csv(filename=os.path.join(param_dir,'image_column_profile_%s_channel%i.csv'%(self.param_names(i),i_channel)))
                    # Create row profile for main image
                    filename = os.path.join(param_dir,"profile_row_%s_main.png"%self.param_names(i))
                    self.Image[i].plot_profile(axis=1, show_channels=self.show_channels, bsave=True, filename=filename)



            if bnoise:
                # Subtract average reference image to the main image and create corresponding histogram/image
                self.Image[i].subtract(self.Image_ref[i])

            if bsave and bnoise:
                filename = os.path.join(param_dir,"hist_%s_sub.png"%self.param_names(i))
                self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins=self.nbins,bsave=True,filename=filename,color='magenta')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,xmin=-250,xmax=250,blog=blog,nbins=self.nbins,ylim=(0,200000),bsave=True,filename=filename,color='magenta')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,xmin=-100,xmax=100,blog=blog,nbins=self.nbins,bsave=True,filename=filename,color='magenta')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins=self.nbins,bsave=True,filename=filename,color='yellow')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins=self.nbins,bsave=True,filename=filename,color='yellow',bfit=True)
                #self.Image[i].plot_histogram(show_channels=self.show_channels,xmin=-50,xmax=50,blog=blog,nbins='fullresolution',bsave=True,filename=filename,color='magenta')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins='fullresolution',bsave=True,filename=filename,color='yellow')
                #self.Image[i].plot_histogram(show_channels=self.show_channels,blog=blog,nbins='fullresolution',bsave=True,filename=filename,color='magenta')
                #self.Image[i].plot_image(bsave=True,filename=filename,dpi=500)

            # optional analysis of 'stuck-on' pixels
            bstuckon = False
            if bstuckon:
                arr_zeros = self.Image_ref[i].array
                arr_zeros[self.Image[i].array!=0] = -999
                print(arr_zeros)
                Im_zeros = Image.Image(arr_zeros,rows=self.Image[i].get_rows(),columns=self.Image[i].get_columns(),datatype=self.Image[i].get_datatype(),channel_groups=self.channel_groups)
                filename = os.path.join(param_dir,"hist_%s_zeros.png"%self.param_names(i))
                Im_zeros.plot_histogram(histrange=(0,4100),blog=blog,nbins=self.nbins,bsave=True,filename=filename,color='green')

            if bnoise:

                offset = self.Image[i].get_mean_channel_groups()
                #offset = self.Image[i].get_median_channel_groups()
                temporal_noise = self.Image[i].get_rms_channel_groups()
                #temporal_noise = self.Image[i].get_rms_channel_groups(bfit=True)

                if bfullnoise:
                    total_temporal_noise,row_temporal_noise,column_temporal_noise,pixel_temporal_noise = self.Image[i].get_noise()
                    for i_channel_group in range(self.num_channel_groups):
                        Total_temporal_noise[i_channel_group].append(total_temporal_noise[i_channel_group])
                        Row_temporal_noise[i_channel_group].append(row_temporal_noise[i_channel_group])
                        Column_temporal_noise[i_channel_group].append(column_temporal_noise[i_channel_group])
                        Pixel_temporal_noise[i_channel_group].append(pixel_temporal_noise[i_channel_group])

                for i_channel_group in range(self.num_channel_groups):
                    Offset[i_channel_group].append(offset[i_channel_group])
                    Temporal_Noise[i_channel_group].append(temporal_noise[i_channel_group])

        self.Average = numpy.array(Average)

        if bnoise:
            # Correction factor since ref image still has typical fluctuations around the true FPN value (sqrt(2) if num_files_ref=1 and num_files=1)
            stat_corr = numpy.sqrt(1/float(self.num_files_ref)+1/float(self.num_files))
            print('Statistical correction factor: %f (reference files: %i; main files: %i)'%(stat_corr,self.num_files_ref,self.num_files))
            self.Total_Noise = numpy.array(Total_Noise)
            self.Temporal_Noise = numpy.array(Temporal_Noise)/stat_corr
            self.Offset = numpy.array(Offset)

            if bfullnoise:

                self.Total_noise = numpy.array(Total_noise)
                self.Row_noise = numpy.array(Row_noise)
                self.Column_noise = numpy.array(Column_noise)
                self.Column_noise_minmax = numpy.array(Column_noise_minmax)
                self.Pixel_noise = numpy.array(Pixel_noise)

                self.Total_temporal_noise = numpy.array(Total_temporal_noise) / stat_corr
                self.Row_temporal_noise = numpy.array(Row_temporal_noise) / stat_corr
                self.Column_temporal_noise = numpy.array(Column_temporal_noise) / stat_corr
                self.Pixel_temporal_noise = numpy.array(Pixel_temporal_noise) / stat_corr
                
                self.Total_fixed_pattern_noise  = (self.Total_noise**2-self.Total_temporal_noise**2)**0.5
                self.Row_fixed_pattern_noise = (self.Row_noise**2-self.Row_temporal_noise**2)**0.5
                self.Column_fixed_pattern_noise = (self.Column_noise**2-self.Column_temporal_noise**2)**0.5
                self.Pixel_fixed_pattern_noise = (self.Pixel_noise**2-self.Pixel_temporal_noise**2)**0.5
                
                # Noise2
                if self.b_load_all:

                    self.Total_fixed_pattern_noise2 = numpy.array(Total_fixed_pattern_noise2)
                    self.Row_fixed_pattern_noise2 = numpy.array(Row_fixed_pattern_noise2)
                    self.Column_fixed_pattern_noise2 = numpy.array(Column_fixed_pattern_noise2)
                    self.Pixel_fixed_pattern_noise2 = numpy.array(Pixel_fixed_pattern_noise2)

                    self.Total_temporal_noise2 = numpy.array(Total_temporal_noise2)
                    self.Row_temporal_noise2 = numpy.array(Row_temporal_noise2)
                    self.Column_temporal_noise2 = numpy.array(Column_temporal_noise2)
                    self.Pixel_temporal_noise2 = numpy.array(Pixel_temporal_noise2)

                    self.Total_noise2  = (self.Total_fixed_pattern_noise2**2+self.Total_temporal_noise2**2)**0.5
                    self.Row_noise2 = (self.Row_fixed_pattern_noise2**2+self.Row_temporal_noise2**2)**0.5
                    self.Column_noise2 = (self.Column_fixed_pattern_noise2**2+self.Column_temporal_noise2**2)**0.5
                    self.Pixel_noise2 = (self.Pixel_fixed_pattern_noise2**2+self.Pixel_temporal_noise2**2)**0.5
                

    def plot_vs_param(self,bfit=False,fitrange='all',linewidth=2.0, bfullnoise=False, rotation_xlabel=0):

        (offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',bsave=False,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',ylim=[0,4096],bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',ylim=[1900,3700],bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',ylim=[1200,3300],bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)
        #(offset,slope) = PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Average",yunit='DN',ylim=[1250,1750],bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,bfit=bfit,fitrange=fitrange,rotation_xlabel=rotation_xlabel)

        if bfit:
            # modify this as it belongs to ReadNoise class only (still to be created)
            gain = 1/numpy.array(slope)*1000000.
            print(offset)
            print(slope)
            print(gain)
            PlotTools.plot_scatter(list(range(self.num_channel_groups)),gain,xlabel='Column group',ylabel='Gain', yunit='uV/DN',bsave=True,directory_save=self.directory_analysis)

        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Offset,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Offset",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
        
        #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Temporal_Noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Temporal Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

        #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Temporal_Noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Temporal Noise",yunit='DN',ylim=[0,15],bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
        PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_Noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
        #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,ylim=(0,15))

        if bfullnoise:
            #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_noise_minmax,show_channels=self.show_channels,xlabel=self.param_cal_label,xlim=[-0.3,1.1],ylim=[-5,150],xunit=self.param_cal_unit,ylabel="Column Noise min-max",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_noise_minmax,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Column Noise min-max",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_fixed_pattern_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Column FPN",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Row_fixed_pattern_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Row FPN",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_fixed_pattern_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel FPN",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_fixed_pattern_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total FPN",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

            #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_fixed_pattern_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xlim=[-0.3,1.1],ylim=[-1,23],xunit=self.param_cal_unit,ylabel="Column FPN",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)
            #Ratio_CFPN_temporal = self.Column_fixed_pattern_noise / self.Total_temporal_noise
            #PlotTools.plot([self.param_cal]*self.num_channel_groups,Ratio_CFPN_temporal,show_channels=self.show_channels,xlabel=self.param_cal_label,ylim=[0,2.3],xunit=self.param_cal_unit,ylabel="Ratio CFPN vs Temporal",yunit='',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)
            #CG = 3.0
            #TemporalImaging = (self.Average*CG)**0.5/CG
            #Ratio_CFPN_temporalimaging = self.Column_fixed_pattern_noise / TemporalImaging
            #PlotTools.plot([self.param_cal]*self.num_channel_groups,TemporalImaging,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Temporal Imaging",yunit='',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)
            #PlotTools.plot([self.param_cal]*self.num_channel_groups,Ratio_CFPN_temporalimaging,show_channels=self.show_channels,xlabel=self.param_cal_label,xlim=[-0.3,1.1],ylim=[0,0.6],xunit=self.param_cal_unit,ylabel="Ratio CFPN vs Temporal (imaging)",yunit='',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth)

            # Remove electronic noise
            #self.Pixel_temporal_noise = (self.Pixel_temporal_noise**2-4.2**2)**0.5
            #self.Pixel_temporal_noise2 = (self.Pixel_temporal_noise2**2-4.2**2)**0.5

            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_temporal_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Temporal Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Row_temporal_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Row Temporal Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_temporal_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Column Temporal Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_temporal_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel Temporal Noise",yunit='DN',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
            #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_temporal_noise,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel Temporal Noise",yunit='DN',ylim=(0,15),bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

            # SNR
            PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Average/self.Total_temporal_noise,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="SNR",yunit='',bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

            
            if self.b_load_all:

                directory_analysis2 = os.path.join(self.directory_analysis,'analysis2')
                print(directory_analysis2)
                print(not(directory_analysis2))
                if not(os.path.exists(directory_analysis2)):
                    os.mkdir(directory_analysis2)

                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Temporal Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Temporal Noise2",yunit='DN',ylim=(7,15),bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel Temporal Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                #PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel Temporal Noise2",yunit='DN',ylim=(7,15),bsave=True,directory_save=self.directory_analysis,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Row_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Row Temporal Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_temporal_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Column Temporal Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)

                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Total_fixed_pattern_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Total Fixed Pattern Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Pixel_fixed_pattern_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Pixel Fixed Pattern Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Column_fixed_pattern_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Column Fixed Pattern Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)
                PlotTools.plot([self.param_cal]*self.num_channel_groups,self.Row_fixed_pattern_noise2,show_channels=self.show_channels,xlabel=self.param_cal_label,xunit=self.param_cal_unit,ylabel="Row Fixed Pattern Noise2",yunit='DN',bsave=True,directory_save=directory_analysis2,linewidth=linewidth,rotation_xlabel=rotation_xlabel)


    def plot_vs_param_2D(self,rotation_xlabel=0,colorscale='jet'):

        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Average,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Average",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)

        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Offset,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Offset",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Total_Noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Total Noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)

        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Total_fixed_pattern_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Total fixed pattern noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Row_fixed_pattern_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Row fixed pattern noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Column_fixed_pattern_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Column fixed pattern noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Pixel_fixed_pattern_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Pixel fixed pattern noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)

        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Total_temporal_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Total temporal noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Row_temporal_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Row temporal noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Column_temporal_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Column temporal noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
        PlotTools.plot2D(self.param_cal,self.param_cal2,self.Pixel_temporal_noise,x1label=self.param_cal_label,x2label=self.param_cal_label2,x1unit=self.param_cal_unit,x2unit=self.param_cal_unit2,ylabel="Pixel temporal noise",yunit='DN',ylim=None,bsave=True,directory_save=self.directory_analysis,rotation_xlabel=rotation_xlabel,colorscale=colorscale)
