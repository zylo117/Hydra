#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from pyvisage import ReadNoise
from pyvisage import PlotTools

if __name__ == '__main__':
    
    bNoise = True
    bfullnoise = True
    bdVscan = False

    num_skip_files = 0
    num_files_ref = 1
    num_files = 1

    columns,rows = 4000,3000
    #columns,rows = 4144,3072
    #columns,rows = 3968,2224
    #columns,rows = 4064,3065
    #columns,rows = 4000,500
    #columns,rows = 4000,3065 # FPN ON
    #columns,rows = 4064,3065 # RTN/FPN alg. ON
    #columns,rows = 1000,3000 # Readout skipping + sub-sampling
    #columns,rows = 256,3000 # Readout skipping + sub-sampling
    #columns,rows = 1280,720
    #columns,rows = 1920,1080
    #columns,rows = 2000,1500
    channel_groups = (1,4) # vertical split
    #channel_groups = (4,1) # horizontal split
    #channel_groups = (2,2)
    num_channel_groups = channel_groups[0] * channel_groups[1]

    show_channels = None
    #show_channels = 0
    #show_channels = [0,2]
    nbins = 100
    #nbins = 'fullresolution'
    linewidth = 2.5
    #linewidth = 0.0
    rotation_xlabel=90

    bparam_cal = False
    bparam_cal2 = False

    directory_suffix = 'v0'

    PlotTools.set_figure_font(xlabelsize=12)
    '''
    # V_sub scan
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150210\\RTO#3_35B_Latch_GPIB_baseline_scan_20150210_133127"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150210\\"
    #param_label = 'V_lownoise'
    param_label = 'Vstart'
    param_unit = 'V'
    #par = numpy.arange(1.8,2.81,0.1)
    #par = numpy.arange(2.2,2.41,0.02)
    #par = numpy.arange(2.24,2.441,0.02)
    #par = numpy.arange(2.24,2.281,0.02)
    #par = numpy.arange(2.02,2.221,0.02)
    #par = numpy.arange(2.14,2.541,0.04)
    #par = numpy.arange(2.02,2.041,0.02)
    par = [2.234,2.255,2.277,2.298,2.319,2.340,2.361,2.382,2.403,2.425]
    #param = ["%i"%v for v in par]
    param = ["%.3f"%v for v in par]
    #param = ['2.100','2.800']
    #par2 = numpy.arange(0.0,1.01,0.1)
    #par2 = numpy.arange(2.0,2.21,0.02)
    #par2 = numpy.arange(1.92,2.321,0.04)
    #par2 = [2.280,4.560,9.120,18.240,36.480,72.960,102.600]
    #par2 = [2.280,4.560,9.120,18.240,36.480,72.960]
    #par2 = [0.010,0.500,1.000,3.000,10.000,30.000,60.000]
    #par2 = [0.010,0.500,1.000,3.000,10.000,30.000,60.000]
    #param_label2 = 'dV_taper'
    #param_label2 = 'Vstop'
    param_label2 = 'dT'
    #param_label2 = 'tau'
    #param_unit2 = ''
    #param_unit2 = 'V'
    param_unit2 = 'hex'
    #param2 = ["%.3f"%v for v in par2]
    param2 = ['0x20','0x24','0x28','0x2c','0x30','0x34','0x38','0x3c','0x40','0x44']
    slope = (2.34-2.12)/52
    bparam_cal2 = True
    #param_cal2 = ['%.3f'%(int(t,16)*0.57) for t in param2]
    param_cal2 = ['%.3f'%(int(t,16)*slope) for t in param2]
    #param_cal_label2 = 'dT'
    #param_cal_unit2 = 'us'
    param_cal_label2 = 'dV'
    param_cal_unit2 = 'V'
    '''

    # LN 2D scans
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_LN12us_2D_Vstart_slope_scan_20150611_140127"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_LN_3D_dTLN_Vstart_slope_scan_20150612_112937"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_LN_3D_scan_20150612_155328"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\752w03#48A1_2DNoise_scan_20150810_164418"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\Q8A752W01#52-A2_Lnscan_20150908_154119"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\"
    param_label = 'Vstart'
    param_unit = 'hex'
    param = [hex(v)[2:] for v in range(0x40,0x71,4)]
    param2 = ['00','02','04','08','0F','4F','5F','6F']
    #param2 = ['00','02']
    param_label2 = 'Slope'
    param_unit2 = 'hex'
    #slope = (2.34-2.12)/52
    #bparam_cal2 = True
    #param_cal2 = ['%.3f'%(int(t,16)*0.57) for t in param2]
    #param_cal2 = ['%.3f'%(int(t,16)*slope) for t in param2]
    #param_cal_label2 = 'dT'
    #param_cal_unit2 = 'us'
    #param_cal_label2 = 'dV'
    #param_cal_unit2 = 'V'

    #file_wildcard = 'RawImages\\image_%s*.raw'
    #file_wildcard = '%sMHz\\RawImages\\image_*.raw'
    #file_wildcard = 'RawImages\\image_%s_*.raw'
    #file_wildcard = 'RawImages\\image_par1_%s*.raw'
    #file_wildcard = 'RawImages\\image_par%s_%s*.raw'
    #file_wildcard = 'RawImages\\image_Vln%s_dVln%s*.raw'
    file_wildcard = 'RawImages\\image_%s_%s*.raw'
    #file_wildcard = 'RawImages\\image_7E_%s_%s*.raw'
    #file_wildcard = 'RawImages\\image_12us_%s_%s*.raw'
    #file_wildcard = 'RawImages\\image_0us_%s_%s*.raw'
    #file_wildcard = 'RawImages\\image_%s_%s_1a*.raw'
    
    file_wildcard_offset = None
    num_files_offset = 0
    #file_wildcard_offset = 'RawImages_AZoff\\image_%s*.raw'
    #num_files_offset = 1

    #roi = None
    roi = (999,999)
    #roi = (0,2999,294,797) # CDS 3-4
    #roi = (499,499)

    if roi!=None:
        roi_suffix = '_roi'
        for r in roi:
            roi_suffix += '_%i'%r
        directory_suffix += roi_suffix

    bfullresolution = False
    if bfullresolution:
        directory_suffix += '_fullres'

    bFPN = False
    if bFPN: directory_suffix += '_FPNcorrected'
    bRTN = False
    if bRTN: directory_suffix += '_RTNcorrected'
    rtn_colstart = 4
    rtn_colstop = 67
    assert((rtn_colstop-rtn_colstart+1)%4==0)

    if bparam_cal:
        directory_suffix += '_calib'
    else:
        param_cal = param
        param_cal_label = param_label
        param_cal_unit = param_unit

    if bparam_cal2:
        directory_suffix += '_calib2'
    else:
        param_cal2 = param2
        param_cal_label2 = param_label2
        param_cal_unit2 = param_unit2

    if bNoise:

        rn_noise = ReadNoise.ReadNoise(directory,
                                       file_wildcard = file_wildcard,
                                       rows = rows,
                                       columns = columns,
                                       param = param,
                                       param2 = param2,
                                       num_skip_files = num_skip_files,
                                       num_files = num_files,
                                       num_files_ref = num_files_ref,
                                       bfullnoise = bfullnoise,
                                       param_label = param_label,
                                       param_unit = param_unit,
                                       param_label2 = param_label2,
                                       param_unit2 = param_unit2,
                                       param_cal = param_cal,
                                       param_cal_label = param_cal_label,
                                       param_cal_unit = param_cal_unit,
                                       param_cal2 = param_cal2,
                                       param_cal_label2 = param_cal_label2,
                                       param_cal_unit2 = param_cal_unit2,
                                       channel_groups = channel_groups,
                                       roi = roi,
                                       show_channels = show_channels,
                                       file_wildcard_offset = file_wildcard_offset,
                                       num_files_offset = num_files_offset,
                                       nbins = nbins)
        
        rn_noise.info()
        rn_noise.analyze_readnoise(bFPN=bFPN,bRTN=bRTN,bsave=False,blog=True,directory_suffix=directory_suffix,linewidth=linewidth,bfullresolution=bfullresolution,rotation_xlabel=rotation_xlabel)
        #rn_noise.analyze_rownoise(bFPN=bFPN,bRTN=bRTN,bsave=True,blog=False,directory_suffix=directory_suffix)
