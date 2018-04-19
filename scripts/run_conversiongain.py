#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from pyvisage import PhotonTransfert
from pyvisage import PlotTools
from pyvisage import Calibration



if __name__ == '__main__':
    
    #directory = "C:\\Users\\Aurel\\PTC\\Data\\20140530\\response_Q8A625w04#62S_Green_Vfilm-0.5V_LED_scan_v0_053014_145140"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\NormalVT_20141212_182903"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\LowVT_20141212_183118"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\NormalVT_FWclear_20141212_185000"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\LowVT_FWclear_20141212_185253"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\LowVT_FWclear_highres_20141212_185640"
    #directory = "C:\\Users\\Aurel\\PC3\\LowVTdevice\\Data\\20141212\\NormalVT_FWclear_highres_20141212_190528"
    directory = "C:\\Users\\Aurel\\PC5\\Pipeline\\Data\\20141223\\33A_normal_20141223_102325"
    #directory = "C:\\Users\\Aurel\\PC5\\Pipeline\\Data\\20141223\\33A_normal_20141223_103311"
    directory = "C:\\Users\\Aurel\\PC5\\Pipeline\\Data\\20141223\\33A_pipeline_20141223_104022"
    directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_Hard_noLN_LEDscan_20150204_105720"
    directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_Hard_LEDscan_20150204_110522"
    directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_Hard_Vref1.6V_LEDscan_20150204_111420"
    #directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_Hard_noLN_Vpix2.5V_LEDscan_20150204_112116"
    directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_Hard_Vref1.9V_LEDscan_20150204_113309"
    directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20150204\\35B_staircase_Vref1.3V_LEDscan_20150204_114008"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_light_sweep_20150430_164432"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_PIXPWR_3.0V_light_sweep_20150430_173640"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_PIXPWR_2.0V_light_sweep_20150430_174435"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_PIXPWR_3.0V_light_sweep_20150430_175151"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_PIXPWR_3.0V_maxI20mA_light_sweep_20150430_175627"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-1.5V_PIXPWR_2.0V_maxI20mA_light_sweep_20150430_184805"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-0.5V_PIXPWR_3.0V_maxI20mA_light_sweep_20150430_185031"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-1.5V_PIXPWR_2.0V_maxI20mA_light_sweep_20150430_185353"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-0.5V_PIXPWR_3.0V_maxI20mA_light_sweep_20150430_185702"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-0.5V_PIXPWR_3.0V_light_sweep_20150501_131409"
    directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\52A_Vfilm_-1.5V_PIXPWR_2.0V_light_sweep_20150501_133017"
    #directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\"
    #directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\"
    #directory = "C:\\Users\\Aurel\\PC5\\Soft_only_reset\\Data\\"

    #file_wildcard = '%smA\\*.raw'
    #file_wildcard = 'RawImages\\Bright_%s\\*.raw'
    file_wildcard = 'RawImages\\image_%s_*.raw'
    #file_wildcard = 'BrightImage_%s_*.raw'
    #file_wildcard = '%s\\*.raw'
    
    #file_wildcard_offset = 'Dark\\*.raw'
    file_wildcard_offset = 'Dark\\*.raw'
    #file_wildcard_offset = 'RawImages\\dark_*.raw'
    #file_wildcard_offset = 'BrightImage_0_*.raw'
    #file_wildcard_offset = None
    
    rows = 3000
    columns = 4000
    datatype = 'uint16'
    
    #channel_groups = (2,2)
    #channel_groups = (2,8)
    #channel_groups = (1,8)
    channel_groups = (2,4)
    
    #fitrange = (1000,2300)
    #fitrange = (500,1500)
    #fitrange = (500,2000)
    fitrange = (250,750)
    #fitrange = 'all'

    directory_suffix = 'v3_upto30'

    bfit = True

    bswap = False
    if bswap: directory_suffix += '_swapped'
    bFPN = False
    if bFPN: directory_suffix += '_FPNcorrected'
    bRTN = False
    if bRTN: directory_suffix += '_RTNcorrected'
    rtn_colstart = 4
    rtn_colstop = 67
    #rtn_colstart = 50
    #rtn_colstop = 150
    assert((rtn_colstop-rtn_colstart+1)%4==0)

    num_skip_files = 0
    num_files = 1
    num_files_ref = 1

    #roi = None
    #roi = (400,400)
    #roi = (600,800)
    roi = (999,999)
    #roi = (399,399)
    #roi = (500,1499,500,1499) # CFA + uLens
    #roi = (2700,2999,3100,3399) # B&W region

    if roi!=None:
        roi_suffix = '_roi'
        for r in roi:
            roi_suffix += '_%i'%r
        directory_suffix += roi_suffix

    bfullresolution = False
    if bfullresolution:
        directory_suffix += '_fullres'
    
    blog = False

    nbins = 200

    PlotTools.set_figure_font()
    
    param_label = 'LED Current'
    #param_label = 'LED Register setting'
    param_unit = 'mA'
    #param_unit = 'Hex'
    #param = [2,3,4,5,6,7,8,9,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,60,62,65,68,70,72,75,78,80]
    #param = [2,3,4,5,6,7,8,9,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,55,60,65,70,75,80,82,85,88,90]
    #param = [2,10,20,40,70,90]
    #param = range(10,91,10)
    #param = [2050,2100,2150,2200,2250,2300,2350,2400]
    #param = [2050,2100,2150,2200,2250,2300]
    #param = range(2050,2410,10)
    #param = range(2050,2300,10)
    #param = range(2050,2300,50)
    #param = range(2050,2300,100)
    #param = [2030,2040]
    #param.remove(2300)
    #param.remove(2360)
    #param = range(0,42,2)
    #param = range(10,701,100)
    #param = range(10,501,50)
    param = list(range(10,501,10))
    #param = range(10,101,10)
    #param = range(10,911,100)
    #param = range(1,10,1)+range(10,401,10)
    #param = range(1,10,1)+range(10,31,10)
    #param = range(1,20,1)
    #param = range(10,401,10)
    #param = range(0,38,3)
    #param = range(0,13,1)
    #param = range(0,20,6)
    #param = [2100,2200,2300,2400]
    #param = [3,4,5,6,7,8,9,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,55,60,65,70,75,80,82,85,88,90]
    #param = [5,6,7,8,9,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,60,62,65,68,70,72,75,78,80]
    #param = [1,2,3,4,5,7,8,10,12,15,18,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150]
    #param = [1,2,3,4,5,7,8,10,12,15,18,20,25,30,35,40,45,50,55,60,65,70,75,80]
    #param = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
    #param = [3,10,20]
    #param = range(61)
    #param = range(101)
    #param = [0,15,25,45,60,80]
    bparam_cal = False
    dT = 0.215 # sec
    #dT = 0.404 # sec
    calib = Calibration.Calibration()
    param_cal = [calib.mA2Luxsec(v,dT) for v in param]
    param_cal_label = 'Intensity'
    param_cal_unit = 'Lux.sec'


    if bparam_cal:
        directory_suffix += '_calib'
    else:
        param_cal = param
        param_cal_label = param_label
        param_cal_unit = param_unit


    cg = PhotonTransfert.PhotonTransfert(directory,
                                         rows=rows,
                                         columns=columns, 
                                         datatype=datatype, 
                                         file_wildcard=file_wildcard, 
                                         param=param, 
                                         num_skip_files=num_skip_files, 
                                         num_files_ref=num_files_ref, 
                                         param_label=param_label, 
                                         param_unit=param_unit, 
                                         param_cal = param_cal,
                                         param_cal_label = param_cal_label,
                                         param_cal_unit = param_cal_unit,
                                         channel_groups=channel_groups, 
                                         roi=roi, 
                                         nbins=nbins,
                                         file_wildcard_offset=file_wildcard_offset)

    cg.info()

    cg.analyze_photontransfert(bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop,bsave=False,directory_suffix=directory_suffix,bfullresolution=bfullresolution,blog=blog,bfit=bfit,fitrange=fitrange)
