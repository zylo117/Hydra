#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from pyvisage import ReadNoise
from pyvisage import PlotTools

if __name__ == '__main__':
    
    analysis_suffix = 'test_v3'    

    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141019\\Q8A672w15#52B_imaging_LN_Taper0.2uA_20141019_175355"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141021\\Q8A672w15#52B_LN_Taper0.2uA_20141021_124042"
    param_label = 'RST_sampling end'
    param_unit = 'Hex Clock Cycles'
    param = ['01', '05', '09', '0d', '11', '15', '19', '1d', '21', '25', '29', '2d', '31', '35', '39', '3d', '41', '45', '49', '4d', '51', '55', '59', '5d', '61', '65', '69', '6d', '71', '75', '79', '7d', '81', '85', '89', '8d', '91', '95', '99', '9d', 'a1', 'a5', 'a9', 'ad', 'b1', 'b5', 'b9', 'bd', 'c1', 'c5', 'c9', 'cd', 'd1', 'd5', 'd9', 'dd', 'e1', 'e5', 'e9', 'ed', 'f1', 'f5', 'f9', 'fd']
    #param = ['21', '25', '29']

    columns,rows = 4000,3000
    channel_groups = (1,4)

    roi = None
    #roi = (999,999)
    #roi = (0,2999,0,255)

    file_wildcard = 'RawImages\\image_%s*.raw'
    num_skip_files = 0
    num_files_ref = 1
    num_files = 1

    file_wildcard_offset = None
    num_files_offset = 0

    bFPN = False
    bRTN = False

    bfullnoise = True

    # Plotting attributes
    bfullresolution = False
    nbins = 100
    linewidth = 2.5
    rotation_xlabel=90
    xlabelsize = 12

    ###############################################
    # No input from user needed beyond this point #
    ###############################################

    PlotTools.set_figure_font(xlabelsize=xlabelsize)

    if roi!=None:
        roi_suffix = '_roi'
        for r in roi:
            roi_suffix += '_%i'%r
        analysis_suffix += roi_suffix

    if bfullresolution:
        analysis_suffix += '_fullres'
    if bFPN: 
        analysis_suffix += '_FPNcorrected'
    if bRTN: 
        analysis_suffix += '_RTNcorrected'

    assert(not(bRTN) or (rtn_colstop-rtn_colstart+1)%4==0)

    rn_noise = ReadNoise.ReadNoise(directory,
                                   file_wildcard = file_wildcard,
                                   rows = rows,
                                   columns = columns,
                                   param = param,
                                   num_skip_files = num_skip_files,
                                   num_files = num_files,
                                   num_files_ref = num_files_ref,
                                   bfullnoise = bfullnoise,
                                   param_label = param_label,
                                   param_unit = param_unit,
                                   channel_groups = channel_groups,
                                   roi = roi,
                                   show_channels = None,
                                   file_wildcard_offset = file_wildcard_offset,
                                   num_files_offset = num_files_offset,
                                   nbins = nbins)
    
    rn_noise.info()
    rn_noise.analyze_readnoise(bFPN=bFPN,bRTN=bRTN,bsave=False,blog=False,directory_suffix=analysis_suffix,linewidth=linewidth,bfullresolution=bfullresolution,rotation_xlabel=rotation_xlabel)
    #rn_noise.analyze_rownoise(bFPN=bFPN,bRTN=bRTN,bsave=True,blog=False,directory_suffix=analysis_suffix)

