#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from pyvisage import ReadNoise
from pyvisage import PlotTools

if __name__ == '__main__':
    
    conditions = 'default' # do not use comma to get proper CSV output file

    bNoise = True
    bfullnoise = True
    b_load_all = False
    bdVscan = False

    num_skip_files = 0
    num_files_ref = 1
    num_files = 1

    #columns,rows = 4208,3120 # IMX214
    columns,rows = 4000,3000
    #columns,rows = 4144,3072
    #columns,rows = 504,3000
    #columns,rows = 4288,3072
    #columns,rows = 4064,3065
    #columns,rows = 4000,500
    #columns,rows = 4000,3065 # FPN ON
    #columns,rows = 4064,3065 # RTN/FPN alg. ON
    #columns,rows = 1000,3000 # Readout skipping + sub-sampling
    #columns,rows = 256,3000 # Readout skipping + sub-sampling
    #columns,rows = 1280,720
    #columns,rows = 1920,1080
    #columns,rows = 2000,1500
    #channel_groups = (1,4) # vertical split
    #channel_groups = (1,1)
    #channel_groups = (2,4)
    channel_groups = (1,16)
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
    rotation_xlabel=0

    bparam_cal = False

    directory_suffix = 'v0'

    PlotTools.set_figure_font(xlabelsize=12)

    #########
    # Noise #
    #########
    '''
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150710\\741w01#48A1_baseline1_corr_latch_VANA1.7V_Noise_scan_20150710_134514"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150724\\752w04#66A2_baseline1_corr_latch_VANA1.7V_Noise_scan_20150724_142145"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150724\\752w04#66A2_baseline1_corr_latch_VANA1.7V_Noise_scan_20150724_150357"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150724\\752w04#66A2_baseline1_corr_latch_VANA1.7V_Noise_scan_20150724_151134"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150724\\752w04#75A1_baseline1_corr_latch_VANA1.7V_Noise_scan_20150724_151416"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150807\\752w04#48A1_Noise_scan_20150810_115932"
    directory = "F:\\INVISAGE\\PC6\\Conversion_gain\\Data\\20151023\\752w01#44A4_Noise_scan_20151023_170058"
    directory = "F:\\INVISAGE\\PC6\\Conversion_gain\\Data\\20151023\\752w01#64A4_Noise_scan_20151023_170836"
    directory = "F:\\INVISAGE\\PC6\\Conversion_gain\\Data\\20151023\\752w01#13A3_Noise_scan_20151023_170935"
    directory = "F:\\INVISAGE\\Q13S\\Bringup\\Data\\20151130\\imaging"
    param_label = 'ScriptConfig'
    #param_label = 'Path A and B'
    param_unit = None
    #param = ['default']
    #param = ['']
    param = ['hard','HS']
    #param = ['simplecapture']
    #param = ['enabled','disabled']
    #param = ['pathABenabled','pathABdisabled','colfreeze']
    #param = ['Hard_Bstyle','Hard','HardSoft','Soft_Bstyle','Soft','CrushedCurrent']
    #param = ['HardB','Hard','HardSoft','CrushedCurrent']
    #param = ['HardB','HardSoft','CrushedCurrent']
    #param = ['CrushedCurrent']
    #param = ['Hard','HardSoft','LowNoise','Elec']
    #param = ['Hard','HardSoft','LowNoise','Soft','Elec']
    #param = ['Hard','HardSoft','LowNoise','Soft','Elec','AFE']
    #param = ['Hard','HardSoft','LowNoise','Soft','Elec','ElecLN']
    #param = ['Hard','HardSoft','LowNoise','Soft','Elec','ElecLN','AFE','AFE_LN']
    #param = ['HardSoft','Elec']
    '''

    '''
    # dV scan
    directory = "F:\\INVISAGE\\Q13S\\Bringup\\Data\\20151130\\790w12#27A3_SHout_finescan_20151204_102858"
    directory = "F:\\INVISAGE\\Q13S\\Bringup\\Data\\20160113\\790w07#27_SHinject_scan_20160113_115802"
    directory = "F:\\INVISAGE\\Q13S\\Bringup\\Data\\20160222\\792w12#35R1_blksunDAC_scan_20160222_151829"
    #param_label = 'Vrst - Vsig'
    #param_label = 'Vshout'
    param_label = 'Blacksun DAC'
    param_unit = 'Volt'
    #V = numpy.arange(-0.8,0.8,0.1)
    #V = numpy.arange(-0.4,1.301,0.1)
    #V = numpy.arange(-0.4,1.301,0.05)
    V = numpy.arange(0.4,1.8,0.05)
    #V = numpy.arange(0,1.501,0.1)
    param = ["%.3f"%v for v in V]
    #param =["%.2f"%(v if abs(v)>0.000001 else abs(int(v))) for v in V]
    #param =["%.1f"%(v if abs(v)>0.000001 else abs(int(v))) for v in V]
    #print param
    '''

    '''
    # timing gen scan
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_hard_scan_20160127_140930"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_hard_scan_20160127_143819"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_hard_scan_20160127_144744"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_hard_scan2_20160127_151727"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_CDSsampling_scan_20160127_154804"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_SHsampling_invscan_20160127_160053"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_SHsampling_scan_20160127_155816"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_SHsampling_newscan_20160127_161828"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_CDSsampling_newscan_20160127_162343"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_softRST_scan_20160127_163636"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_dT5lines_softRST_scan2_20160127_165430"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_softRST_scan2_20160128_132323"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_softRST_scan_20160128_132435"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_hardRST_scan2_20160128_132612"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_hardRST_scan_20160128_132712"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_SHsampling_scan_20160128_134053"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_CDSsampling_scan_20160128_134148"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w07#56R1_dT5lines_SHsampling_finescan_20160128_140606"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\"
    #param_label = 'Hard RST time'
    #param_label = 'Soft RST time'
    param_label = 'Sampling time'
    param_unit = 'us'
    #V = numpy.arange(0.06,1.35,0.08) # hard RST
    #V = numpy.arange(0.03,1.8,0.16) # hard RST 2
    #V = numpy.arange(0.130,2.370,0.16) # CDS/SH sampling
    V = numpy.arange(0.130,2.371,0.04) # CDS/SH sampling - fine
    #V = numpy.arange(0.050,1.10,0.08) # soft RST
    param = ["%.3f"%v for v in V]
    #param =["%.2f"%(v if abs(v)>0.000001 else abs(int(v))) for v in V]
    #param =["%.1f"%(v if abs(v)>0.000001 else abs(int(v))) for v in V]
    #print param
    '''

    # LED scan
    #directory = "F:\\INVISAGE\\PC5\\CDS_AFE_gain_linearity\\Data\\20140916\\Q8A670w12#33A_LEDscan_FPNfrozen"
    #param_label = 'LED intensity'
    #param_unit = 'mA'
    #V = range(0,91,10)
    #param = ["%i"%v for v in V]
    '''
    # Integration time scan
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140203\\LowNoiseAurel_pixel_1FPS_dTscan_qTest3.7.15_10val_0-500ms_DFT_v0_020314_144530"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_dT_scan_20150313_162528"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_HardRST_cold_dT_finescan_20150318_143054"
    #conditions = 'Film ON / Cold Temp' # do not use comma to get proper CSV output file
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_HardRST_FilmOFF_dT_finescan_20150318_144803"
    #conditions = 'Film OFF / Room Temp' # do not use comma to get proper CSV output file
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_HardRST_withcorr_FilmOFF_dT_finescan_20150319_124731"
    #conditions = 'Film OFF / Room Temp/ with corr' # do not use comma to get proper CSV output file
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_HardRST_withcorr_FilmOFF_inverse_dT_finescan_20150319_140310"
    #conditions = 'Film OFF / Room Temp/ with corr / Inv' # do not use comma to get proper CSV output file
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_HardRST_withcorr_FilmON_inverse_dT_finescan_20150319_153044"
    #conditions = 'Film ON / Room Temp/ with corr / Inv' # do not use comma to get proper CSV output file
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150406\\85C_baseline0_20150406_154219"
    #conditions = 'default'
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150406\\35B_1fps_20150406_160400"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150406\\35B_1fps_withcorr_20150406_162033"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150406\\35B_baseline0_nocorr_20150406_163454"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\35B_1fps_nocorr_20150409_135858"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nocorr_20150414_115226"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nocorr_100images_20150414_164438"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nolatch_HSreset_nocorr_20150415_112818"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nolatch_Hreset_nocorr_20150415_113327"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nolatch_Hreset_withcorr_20150415_113937"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_latch_Hreset_nocorr_20150415_121702"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\693w18#55C_baseline0_nolatch_HSreset_nocorr_20150415_132050"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\PFPN\\Data\\20150409\\"
    #conditions = 2
    param_label = 'Integration Time'
    param_unit = 'sec'
    #dT = [0.149, 0.298, 0.447, 0.596, 0.745, 0.894, 1.042, 1.191, 1.333]
    #dT = [0.002, 0.005, 0.007, 0.009, 0.012, 0.014, 0.016]
    #dT = [0.019, 0.037, 0.056, 0.074, 0.093, 0.112, 0.130, 0.149]
    #dT = [0.0012, 0.0023, 0.0035, 0.0047, 0.0058, 0.0070, 0.0081, 0.0093, 0.0105, 0.0116, 0.0128, 0.0140, 0.0151, 0.0163, 0.0175]
    #dT = [0.019, 0.037, 0.056, 0.074, 0.093, 0.112, 0.130, 0.149, 0.298, 0.447, 0.596, 0.745, 0.894, 1.042, 1.191, 1.333]
    #dT = [0.0012, 0.0023, 0.0035, 0.0047, 0.0058, 0.0070, 0.0081, 0.0093, 0.0105, 0.0116, 0.0128, 0.0140, 0.0151, 0.0163, 0.0175, 0.019, 0.037, 0.056, 0.074, 0.093, 0.112, 0.130, 0.149]
    #dT = [0.0012, 0.0023, 0.0035, 0.0047, 0.0058, 0.0070, 0.0081, 0.0093, 0.0105, 0.0116, 0.0128, 0.0140, 0.0151, 0.0163, 0.0175, 0.0190, 0.0370, 0.0560, 0.0740, 0.0930, 0.1120, 0.1300, 0.1490, 0.298, 0.447, 0.596, 0.745, 0.894, 1.042, 1.191, 1.333]
    dT = [0.214000, 0.196358, 0.178508, 0.160657, 0.142806, 0.124955, 0.107105, 0.089254, 0.071403, 0.053552, 0.035702, 0.017851, 0.008925, 0.007810, 0.006694, 0.005578, 0.004463, 0.003347, 0.002231, 0.001116, 0.001046, 0.000976, 0.000906, 0.000837, 0.000767, 0.000697, 0.000628, 0.000558, 0.000488, 0.000418, 0.000349, 0.000279, 0.000209, 0.000139, 0.000070]
    #dT = [0.017851, 0.008925, 0.007810, 0.006694, 0.005578, 0.004463, 0.003347, 0.002231, 0.001116, 0.001046, 0.000976, 0.000906, 0.000837, 0.000767, 0.000697, 0.000628, 0.000558, 0.000488, 0.000418, 0.000349, 0.000279, 0.000209, 0.000139, 0.000070]
    #dT = [0.214000, 0.142806, 0.071403, 0.008925]
    #dT = [0.0190, 0.0370, 0.0560, 0.0740, 0.0930, 0.1120, 0.1300, 0.1490, 0.298, 0.447, 0.596, 0.745, 0.894, 1.042, 1.191, 1.333]
    #dT = [0.0190, 0.0370]
    #dT = [0.0012, 0.0023, 0.0035, 0.0047, 0.0058, 0.0070, 0.0081, 0.0093, 0.0105, 0.0116, 0.0128, 0.0140, 0.0151, 0.0163, 0.0175, 0.0190, 0.0370, 0.0560, 0.0740, 0.0930, 0.1120, 0.1300, 0.1490]
    #dT = numpy.linspace(0.0,0.5,10)
    #dT = numpy.linspace(0.0,0.9,18)
    #param = ["%.3f"%dt for dt in dT]
    param = ["%.4f"%dt for dt in dT]
    param = ["%.6f"%dt for dt in dT]
    '''
    # simultaneous vs non-simultaneous
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140324\\LowNoiseAurel_sim_nonsim_Q8A636w14#25-D_CrushedCurrentSource_v0_032414_155729"
    #param_label = 'Timing'
    #param_unit = None
    #param = ['non-simultaneous','simultaneous']

    # grounded/pixel
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140422\\noise_Q8A636w14#25-D_RSTbeforesampling_HardSoftRST_NoiseBreakdown_v0_042214_123430"
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140422\\noise_Q8A636w14#25-D_RSTbeforesampling_HardRST_NoiseBreakdown_v0_042214_123517"
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140422\\noise_Q8A636w14#25-D_RSTbeforesampling_SoftRST_NoiseBreakdown_v0_042214_123605"
    #param_label = 'Connection'
    #param_label = 'Setting'
    #param_unit = None
    #param = ['grounded','pixel']
    #param = ['pixel','RSTalwaysON','CrushedCurrentSource']

    # DeltaT scan
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140402\\noise_Q8A636w14#25-D_HSrst_Vrsthigh_2.5V_dT_scan_ascending_v0_040214_131805"
    #param_label = 'coarse_integration_time'
    #param_unit = ''
    #V = range(0,1001,100)
    #V = range(256,-1,-16)
    #V = range(16,-1,-1)
    #param = ["%i"%v for v in V]


    # V_sub scan
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150218\\RTO#3_13B_afterFIB_GPIB_baseline_scanVPIX2.8V_AUX02_pwlLOW_20150219_162654"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150223\\RTO#3_74B_afterFIB_Vref1.6V_GPIB_baseline_scan_20150223_172034"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_GPIB_baseline_scan_20150225_105134"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_GPIB_baseline_scan_20150225_105836"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_GPIB_baseline_scan_20150225_110201"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_GPIB_baseline_finescan_20150225_110741"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_startcol104_GPIB_baseline_scan_20150225_114821"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150225\\RTO#3_63B_beforeFIB_startcol104_GPIB_baseline_finescan_20150225_115401"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_24L_GPIB_baseline_finescan_20150226_112801"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_afterFIB_startcol104_GPIB_baseline_finescan_20150226_114252"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test0_20150226_150236"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test0_top3_bot2_20150226_150547"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test0_top2_bot3_20150226_150732"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test0_tgcont8A_20150226_151014"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test1_LNoff_20150226_154150"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test1_LNoff_20150226_160651"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_63B_test1_LNoff_20150226_161138"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_GPIB_baseline_scan_20150227_110344"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_withcorr_GPIB_baseline_scan_20150227_112110"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_nocorr_GPIB_baseline_finescan_20150305_105710"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_withcorr_GPIB_baseline_finescan_20150305_105052"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150305\\RTO#3_63B_afterFIB2_startcol104_GPIB_baseline_finescan_20150305_142054"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_nocorr_GPIB_staircase_finescan_20150305_180142"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150305\\RTO#3_63B_afterFIB2_startcol104_GPIB_baseline_finescan_20150309_114042"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150227\\RTO#3_35B_GPIB_constant_slope_scan_20150306_104456"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150310\\RTO#3_63B_afterFIB_oddcol_GPIB_baseline_scan_20150310_183853"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150312\\RTO#3_35B_GPIB_constant_slope_scan_20150313_181746"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_scan_20160222_151829"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_scan_20160222_154801"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_scan_20160222_173027"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_scan_20160222_173602"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_scan2_20160224_115358"
    directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\792w12#35R1_blksunDAC_newSettings_scan2_20160224_145823"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\"
    #directory = "F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160222\\"
    #param_label = 'V_staircase'
    #param_label = 'Vref'
    #param_label = 'Vtaper'
    #param_label = 'Vmean_tapering'
    #param_label = 'V_compensation'
    #param_label = 'hard RST width'
    #param_label = 'hard RST end'
    #param_label = 'dT_LN'
    param_label = 'Blacksun DAC'
    #param_unit = 'V'
    #param_unit = 'us'
    param_unit = 'hex'
    param = ["0x%02x"%v for v in range(0x0,0x7F,8)]
    #V = numpy.arange(0.1,2.701,0.1)
    #V = numpy.arange(1.7,2.701,0.1)
    #V = numpy.arange(2.2,2.701,0.025)
    #V = numpy.arange(1.7,2.701,0.025)
    #V = numpy.arange(2.6,2.701,0.1)
    #V = numpy.arange(1.7,2.801,0.1)
    #V = numpy.arange(1.7,2.701,0.025)
    #V = numpy.arange(1.5,2.801,0.05)
    #V = numpy.append(V,0.0)
    #V = [0,0.5,1.0,1.5,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.8]
    #V = [0,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.8]
    #V = [0,1.9,2.1,2.3,2.5,2.8]
    #V = [0,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8]
    #V = [1.8,1.85,1.9,1.95,2.0,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5]
    #V = [1.9,1.95,2.0,2.05,2.1,2.11,2.12,2.13,2.14,2.15,2.16,2.17,2.18,2.19,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.8]
    #V = [1.9,1.95,2.0,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.8]
    #V = [2.16,2.8]
    #V = [2.0]
    #V = [0.00, 1.14, 2.28, 3.42, 4.56, 5.70, 6.84, 7.98, 9.12, 10.26, 11.40, 12.54, 13.68, 14.82, 15.96]
    #V = [0.000, 0.570, 1.140, 2.280, 4.560, 9.120, 18.240, 36.480, 72.960]
    #V = numpy.arange(2.2,2.501,0.05)
    #V = [3.43,8.00,9.14,12.57,17.14,21.71,23.43]
    #V = [1.71,6.29,10.86,15.43,20.00,23.43]
    #param = ['20','24','28','2c','30','34','38','3c','40','44']
    #param = ["%.1f"%v for v in V]
    #param = ["%.2f"%v for v in V]
    #param = ["%.3f"%v for v in V]
    #param = ["internalRST_LN"]
    #param = ["hard","samplingduringRST","crushed"]
    #param = ["hard","samplingduringRST","crushed","crushed2"]
    #param = [""]
    #param = ['04','09','1A','34','69']
    #param.insert(0,"crushed")
    #param.insert(0,"noRST")
    #param.insert(0,"noRST2")
    #param.remove('1.700')
    #param = ['30','38','40','48','50']
    #param = ['hard_Vrsthi_2.8V','hard_Vrsthi_2.0V','hard_Vrsthi_1.0V','hard_Vrsthi_0.0V','hard_Vrstlo']
    #bparam_cal = True
    #param_cal = [int(v,16)*0.57 for v in param]
    #param_cal_label = 'dT_LN2'
    #param_cal_unit = 'us'
    #slope = (2.34-2.12)/0x34
    #param_cal = [ slope*int(v,16)*1000 for v in param]
    #param_cal_label = 'dV_tapering'
    #param_cal_unit = 'mV'
    '''

    # Taper end scan
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\Q8A670w07#75B_RSTfall_roughscan_20141106_170246"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\74B_RSTfall_roughscan_20141106_170834"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141106\\"
    #param_label = 'Taper end'
    #param_unit = 'Hex Clock Cycles'
    #param = ['35', '39', '3d', '41', '45', '49', '4d', '51', '55', '59', '5d', '61', '65', '69', '6d', '71', '75', '79', '7d', '81', '85', '89', '8d', '91', '95', '99', '9d', 'a1', 'a5', 'a9', 'ad', 'b1', 'b5', 'b9', 'bd', 'c1', 'c5', 'c9', 'cd', 'd1', 'd5', 'd9', 'dd', 'e1', 'e5', 'e9', 'ed']
    #param = ['35', '37', '39', '3b', '3d', '3f', '41', '43', '45', '47', '49', '4b', '4d', '4f', '51', '53', '55', '57', '59', '5b', '5d', '5f', '61', '63', '65', '67', '69', '6b', '6d', '6f', '71', '73', '75', '77', '79', '7b', '7d', '7f', '81', '83','85', '87', '89', '8b', '8d', '8f', '91', '93', '95', '97', '99', '9b', '9d', '9f', 'a1', 'a3', 'a5', 'a7', 'a9', 'ab', 'ad', 'af', 'b1', 'b3', 'b5', 'b7', 'b9', 'bb', 'bd', 'bf', 'c1', 'c3', 'c5', 'c7', 'c9', 'cb', 'cd', 'cf', 'd1', 'd3','d5', 'd7', 'd9', 'db', 'dd', 'df', 'e1', 'e3', 'e5', 'e7', 'e9', 'eb', 'ed',]
    #param = ['35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed',]
    #param = ['9d', 'a1', 'a5', 'a9', 'ad', 'b1', 'b5', 'b9', 'bd', 'c1', 'c5', 'c9', 'cd', 'd1', 'd5', 'd9', 'dd', 'e1', 'e5', 'e9', 'ed']
    #param = ['9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed',]

    # Itaper scan
    #directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20141110\\75B_Itaper_scan_20141110_141745"
    #directory = "C:\\Users\\Aurel\\PC5\\Low_Noise\\Data\\20141110\\75B_LowGain_Itaper_scan_20141110_142108"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141116\\Q8A672w10#13B_Tapering_scan_ExternalRST_2M_longerTapering"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141118\\Q8A672w10#13B_Itaper_scan_internal_20141118_124801"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141118\\Q8A672w10#13B_Itaper_scan_external"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141118\\"
    #param_label = 'I_taper'
    #param_label = 'Taper_time'
    #param_unit = 'uA'
    #param_unit = 'us'
    #param_unit = ''
    #I = numpy.array([8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0,0.7,0.6,0.5,0.4,0.3,0.2,0.1])
    #I = numpy.array([8.0,0.2,0.1])
    #I = numpy.array([8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0,0.3,0.2,0.1])
    #param = ["%.1f"%v for v in I]
    #param = ['0x37','0x39','0x3D','0x45','0x55','0x85','0xD5',]
    #dT_taper = [1.,2.,5.,10.,25.,50.,100.,200.,400.]
    #dT_taper = [2**i for i in range(11)]
    #param = ["%i"%v for v in dT_taper]
    #dT = 1.9e-12*2.8/(I*1e-6)*1e6
    #dT = [(int(p,16)-0x35)*0.57 for p in param]
    #bparam_cal = True
    #param_cal = ["%.1f"%v for v in dT]
    #param_cal_label = 'dT_taper'
    #param_cal_unit = 'us'

    # timing scan
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150616\\31A9_LN_roi_scan_20150616_161121"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150616\\31A9_LN_16images_roi_scan_20150616_163046"
    directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150619\\35A2_preFIB_LN_scan_20150619_120524"
    #directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150619\\"
    #directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150616\\33A5_baseline1_hardsoft_sftognd_longRead_test7_RSTsampling_scan_20150617_174714"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150616\\33A5_baseline1_hardsoft_sftognd_RSTsampling_scan_20150617_165258"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\55A8_postCut_sftognd_RSTsampling_scan_20150619_181436"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\33A5_colbias3_RSTsampling_scan_20150619_185521"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\33A5_colbias3_noRSTsampSEL_RSTsampling_scan_20150619_185828"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\33A8_colbias3L_RSTsampling_scan_20150619_190837"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\33A8_colbias3L_noRSTSEL_RSTsampling_scan_20150619_191248"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150619\\55A8_colbias3_noRSTSEL_cut_RSTsampling_scan_20150619_192811"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_RSTsampling_scan_20150623_103253"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_RSTsampling_scan_20150623_103500"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_nokeep_RSTsampling_scan_20150623_104720"
    #directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_nokeep_adfinject_RSTsampling_scan_20150623_111844"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_nokeep_adfinject_RSTsampling_scan_20150623_112544"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_nokeep_adfinject_RSTsampling_finescan_20150623_113138"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_nokeep_RSTsampling_finescan_20150623_113317"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual_RSTsampling_finescan_20150623_115713"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual_adftinject_RSTsampling_finescan_20150623_115851"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_adftinject_RSTsampling_finescan_20150623_120453"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_RSTsampling_finescan_20150623_120653"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_adfinject_start95_RSTsampling_finescan_20150623_121249"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_start95_RSTsampling_finescan_20150623_121433"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_RSTsampling_finescan_20150623_122338"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_adftinject_RSTsampling_finescan_20150623_122501"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_start8F_adftinject_RSTsampling_finescan_20150623_122725"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_start8F_adftinject_RSTsampling_finescan_20150623_122725"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_start95_RSTsampling_finescan_20150623_123107"
    directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\33A8_baseline1_sftognd_blcmanual1FF_DAC80.7V_start95_adfinject_RSTsampling_finescan_20150623_123217"
    #directory = "F:\\INVISAGE\\PC6\\Pixel_Timing\\Data\\20150622\\"
    #param_label = 'en_hard_end'
    #param_label = 'Vref'
    #param_label = 'reset_LN_start'
    #param_label = 'RST_end'
    #param_label = 'Vstart ramp'
    #param_label = 'LN_time'
    #param_label = 'LN_en end'
    param_label = 'RST_sampling end'
    #param_label = 'RST falling edge'
    #param_unit = 'Clock Cycles'
    param_unit = 'Hex Clock Cycles'
    #param_unit = 'us'
    #T = range(94,129,2)
    #T = range(88,129,2)
    #param = ["%i"%t for t in T]
    #param = ['30','c6']
    #param = [hex(v)[2:] for v in range(0x30,0xc9,10)[:8]]
    #param = [hex(v)[2:] for v in range(0x30,0x66,1)]
    param = [hex(v)[2:] for v in range(0x7f,0x10,-8)]
    param = [hex(v)[2:] for v in range(0x7f,0x10,-5)]
    #param = [hex(v)[2:] for v in range(0x10,0xF1,5)]
    #param = [hex(v)[2:] for v in range(0x83,0xB5,1)]
    #param = [hex(v)[2:] for v in range(0x60,0xBC,3)]
    #param = [hex(v)[2:] for v in range(0x50,0xBC,0x02)]
    #param = [hex(v)[2:] for v in range(0x85,0xFC,0x02)]
    #param = [hex(v)[2:] for v in range(0x85,0xB5,0x01)]
    param = [hex(v)[2:] for v in range(0x85,0x9A,0x01)]
    #param = [hex(v)[2:] for v in range(0x50,0xFC,0x02)]
    #param = [hex(v)[2:] for v in range(0xA2,0xFC,0x04)]
    #param = [hex(v)[2:] for v in range(0x1B,0xE0,8)]
    #param = [hex(v)[2:] for v in range(0x23,0xE0,8)]
    #param = [ hex(s)[2:] for s in range(int('0x64',16),int('0x8e',16)+1,2)]
    #param = ['49','85','c1']
    #param = ['15','40','58','b0']
    #param = ['15','41','b1']
    #param.remove('7a')
    #param.append('crushed')
    #bparam_cal = True
    #param_cal = [(int(v,16)-0x1A)*0.12 for v in param]
    #param_cal_label = 'Reset Ramp time'
    #param_cal_unit = 'us'
    '''
    '''
    # Vrst scan
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\52A_dark_AZoff_pixpwrVfilm_scan_20150430_181910"
    directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\52A_light_AZoff_pixpwrVfilm_scan_20150430_183139"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\52A_dark_AZoff_pixpwrVfilm_scan_20150430_183845"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\"
    #directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150429\\"
    #param_label = 'Vrst'
    #param_label = 'Vrst_high'
    #param_label = 'Vref'
    param_label = 'PIXPWR'
    #param_label = 'Vrsthigh_PWRPIX'
    param_unit = 'Volt'
    #V = numpy.arange(2.0,3.01,0.1)
    #V = numpy.arange(1.5,3.31,0.1)
    #V = numpy.arange(1.5,3.31,0.01)
    #V = numpy.arange(1.5,3.31,0.02)
    V = numpy.arange(2.0,3.31,0.02)
    #V = numpy.arange(1.5,3.31,0.1)
    #param = ["%.1f"%v for v in V]
    #param = ["%.2f"%v for v in V]
    param = ["%.3f"%v for v in V]
    #param.remove('2.10')
    #param.remove('1.89')
    #param.remove('2.80')
    #param.append('crushedcurrent')
    param.append('crushed')
    '''
    # VDD scans
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140129\\LowNoiseAurel_nonsim_AFEDFT_BLC0_AVDD_scan_v0_012914_123950"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\Data\\20140909\\Q8A670w10#54E_AVDD28_scan"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\Data\\20140912\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut_AVDD15_1.8V"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_20140922_122039"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_dV0.5V_PWRAN2scan_20140922_122140"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#55E_afterFIB_specialWB_PWRAN2scan_20140922_140520"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_VANA15_1.5V_PWRAN2scan_20140922_141431"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_170932"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#55E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_175127"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#55E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_175531"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_175715"
    #directory = "F:\\INVISAGE\\PC5\\Read_noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_1to3V_Vcmi300mV_20140922_184212"
    #param_label = 'AVDD28'
    #param_label = 'PWRAN2'
    #param_unit = 'Volt'
    #V = numpy.linspace(2.0,3.01,10)
    #V = numpy.arange(1.0,3.01,0.1)
    #param = ["%.1f"%v for v in V]
    '''
    # Clock Delay scan
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150527\\55A8_10MHz_AFEdelay_finescan_20150527_132722"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150527\\55A5_30MHz_CDS4-7_AFEdelay_finescan_20150528_110915"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150527\\55A5_30MHz_CDS4-7_VANA28_3.5V_AFEdelay_finescan_20150528_111208"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150527\\46A_afterFIB_30MHz_AFEdelay_finescan_20150528_112555"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150527\\46A_afterFIB_10MHz_AFEdelay_finescan_20150528_113150"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_delay_scan_20150603_144806"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_30MHz_4CDS_delay_scan_20150603_150239"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_10MHz_4CDS_delay_scan_20150603_150612"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_30MHz_4CDS_13-16_delay_scan_20150603_151052"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_10MHz_4CDS_13-16_delay_scan_20150603_151412"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_20MHz_4CDS_13-16_delay_scan_20150603_152118"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_40MHz_4CDS_13-16_delay_scan_20150603_153217"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_50MHz_4CDS_delay_scan_20150603_154833"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_50MHz_4CDS_13-16_delay_scan_20150603_155049"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_40MHz_4CDS_delay_scan_20150603_154602"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\31A5_FIBall_20MHz_4CDS_delay_scan_20150603_155519"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_20MHz_CDS1-4_afe_clk_delay_scan_20150604_131501"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    param_label = 'AFE-CDS clock delay'
    #param_unit = 'hex'
    param_unit = 'dec'
    #V = numpy.arange(0,255,8)
    V = numpy.arange(-248,255,8)
    #V = numpy.arange(50,150,1 )
    param = ["%i"%v for v in V]
    #param_unit = 'ns'
    #V = numpy.linspace(0.45,4.0,10)
    #V = numpy.arange(0.45,3.95,0.22)
    #V = numpy.arange(-3.3,3.31,0.22)
    #param = ["%.2f"%v for v in V]
    '''
    '''
    # Clock skew scan
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_skew_scan_20150604_130408"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_30MHz_skew_scan_20150604_130732"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_40MHz_skew_scan_20150604_130907"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_CDS13-16_clkskew_scan_20150604_134759"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_40MHz_CDS13-16_clkskew_scan_20150604_135527"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_30MHz_CDS13-16_clkskew_scan_20150604_140853"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_50MHz_CDS13-16_clkskew_scan_20150604_141510"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_20MHz_CDS13-16_clkskew_scan_20150604_141836"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_10MHz_CDS13-16_clkskew_scan_20150604_142004"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    param_label = 'Clock skew'
    param_unit = 'ns'
    V = numpy.arange(0,7.1,1)
    param = ["%ins"%v for v in V]
    param.append('noskew')
    '''
    '''
    # Analog Clock Frequency scan
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150603\\55A5_4CDS_1-4_anafreq_scan"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_CDS1-4_freq_scan_20150604_133728"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_CDS13-16_freq_scan_20150604_134102"
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_skew2ns_CDS13-16_freq_scan_20150604_150417"
    conditions = 'skew 2ns'
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_noskew_CDS13-16_freq_scan_20150604_150625"
    #conditions = 'no skew'
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_noskew_1.8V_CDS13-16_freq_scan_20150604_154121"
    conditions = 'no skew + VANA15=1.8V'
    directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\31A5_fullFIB_skew2ns_1.8V_CDS13-16_freq_scan_20150604_154320"
    conditions = 'skew 2ns + VANA15=1.8V'
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    #directory = "F:\\INVISAGE\\PC6\\AtSpeed\\Data\\20150604\\"
    param_label = 'Analog Clock Frequency'
    param_unit = 'MHz'
    #V = numpy.arange(10,71,10)
    V = numpy.arange(10,51,10)
    param = ["%i"%v for v in V]
    '''
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140121_LowNoise_baseline_simultaneous_sampling_VDD_ClockDelays_Vrst_scans\\LowNoiseAurel_baseline_Vrst_scan_v0_012114_151523"
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140122\\LowNoiseAurel_baseline_DFTInput_Vrst_scan_v0_012214_090832"
    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140129\\LowNoiseAurel_nonsim_AFEDFT_BLC0_Vrst_scan_v0_012914_121055"
    #param_label = 'V_REF'
    #param_unit = 'Volt'
    #V = numpy.linspace(0.,3.,11)
    #param = ["%.1f"%v for v in V]

    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140128\\LowNoiseAurel_nonsim_VCMI_scan_v0_012814_095849"
    #param_label = 'V_CMI'
    #param_unit = 'hex value'
    #param = ['00','01','02','03']

    #directory = "F:\\INVISAGE\\PC3\\Read_noise\\Data\\20140128\\LowNoiseAurel_nonsim_BLC_scan_v1_012814_112845"
    #param_label = 'BLC'
    #param_unit = 'hex value'
    #param = ['00','0F','1F','2F','3F','4F','5F','6F','7F','8F','9F','AF','BF','CF','DF','EF','FF']

    #file_wildcard = 'image_%s_*.raw'
    #file_wildcard = 'RawImages\\Dark%s_*.raw'
    #file_wildcard = 'RawImages\\image_%s*.raw'
    file_wildcard = 'RawImages\\image_%s_*.raw'
    #file_wildcard = 'RawImages\\image_18_%s_*.raw'
    #file_wildcard = 'RawImages\\image_2.382_%s*.raw'
    #file_wildcard = '%sMHz\\RawImages\\image_*.raw'
    #file_wildcard = 'RawImages\\image_%s_*.raw'
    #file_wildcard = 'RawImages\\image_%s*.raw'
    #file_wildcard = 'RawImages\\image_2.340_2.120_%s*.raw'
    #file_wildcard = 'RawImages\\image_%s_[10,11].raw'
    #file_wildcard = 'RawImages\\image_%s[0,1,2].raw'
    #file_wildcard = 'RawImages\\image_%s[3,4]?.raw'
    #file_wildcard = 'RawImages\\image_%s_[5]?.raw'
    #file_wildcard = 'RawImages\\image_%s_[50,51].raw'
    #file_wildcard = 'RawImages\\image_%s_*.raw'
    #file_wildcard = 'RawImages\\image_%s*.raw'
    #file_wildcard = 'RawImages\\image_%s'+param_unit+'_*.raw'
    #file_wildcard = 'RawImages\\image_%sus_*.raw'
    #file_wildcard = 'RawImages\\image_%sV_*.raw'
    #file_wildcard = 'RawImages\\image_%suA_*.raw'
    
    file_wildcard_offset = None
    num_files_offset = 0
    #file_wildcard_offset = 'RawImages_AZoff\\image_%s*.raw'
    #file_wildcard_offset = 'RawImages\\image_-0.500_0.raw'
    #file_wildcard_offset = 'RawImages_dark\\image_%s_*.raw'
    #num_files_offset = 1

    roi = None
    roi = (999,999)
    #roi = (4,2995,4,3995)
    #roi = (4,2995,0,199)
    #roi = (0,2999,1000,1003)
    #roi = (2900,2999,1500,2499)
    #roi = (0,2999,0,503)
    #roi = (1520,1619,1010,1129)
    #roi = (10,139,1040,1119)
    #roi = (0,2999,0,199)
    #roi = (0,2999,100,103)
    #roi = (0,2999,1840,2331)
    #roi = (0,2999,1840,2079)
    #roi = (0,2999,0,37) # CDS 1
    #roi = (0,2999,44,291) # CDS 2
    #roi = (0,2999,300,547) # CDS 3
    #roi = (0,2999,300,803) # CDS 3-4
    #roi = (0,2999,556,803) # CDS 4
    #roi = (0,2999,812,1059) # CDS 5
    #roi = (0,2999,1068,1315) # CDS 6
    #roi = (0,2999,1324,1571) # CDS 7
    #roi = (0,2999,1580,1827) # CDS 8
    #roi = (0,2999,1836,2083) # CDS 9
    #roi = (0,2999,2092,2339) # CDS 10
    #roi = (0,2999,2348,2595) # CDS 11
    #roi = (0,2999,2604,2851) # CDS 12
    #roi = (0,2999,2860,3107) # CDS 13
    #roi = (0,2999,3116,3363) # CDS 14
    #roi = (0,2999,3372,3619) # CDS 15
    #roi = (0,2999,3628,3875) # CDS 16
    #roi = (0,2999,3884,3993) # CDS 17
    #roi = (0,2987,0,3987)
    #roi = (499,499)
    #roi = (0,2999,0,3999)
    #roi = (65,3064,64,4063)
    #roi = (0,2999,1787,1790) # 1 column analysis #2000 physical
    #roi = (0,2999,1779,1782) # 1 column analysis #1992 physical
    #roi = (0,2999,1795,1798) # 1 column analysis #2008 physical
    #roi = (0,2999,15,18) # 1 column analysis #120 physical (col start: 104)
    #roi = (0,2999,23,26) # 1 column analysis #128 physical (col start: 104)
    #roi = (0,2999,7,10) # 1 column analysis #112 physical (col start: 104) - true FIBed
    #roi = (0,2999,11,14) # 1 column analysis #112 physical (col start: 104) - true FIBed
    #roi = (0,2999,15,18) # 1 column analysis #116 physical (col start: 104) - true FIBed
    #roi = (0,2999,19,22) # 1 column analysis #120 physical (col start: 104) - true FIBed
    #roi = (0,2999,23,26) # 1 column analysis #124 physical (col start: 104) - true FIBed
    #roi = (0,2999,27,30) # 1 column analysis #128 physical (col start: 104) - true FIBed
    #roi = (0,2999,31,34) # 1 column analysis #128 physical (col start: 104) - true FIBed
    #roi = (1000,1003,0,3999) # 1 row analysis
    #roi = (2000,2003,0,3999) # 1 row analysis
    #roi = (2999,2999,0,3499) # last line
    #roi = (2998,2998,0,3999) # last line
    #roi = (1500,1500,0,3999) # middle line
    #roi = (0,0,0,3999) # first line
    #roi = (0,2999,0,240)
    #roi = (0,2999,1000,3999)
    #roi = (66,3064,65,4063) # image array only (i.e. without reference rows/columns)
    #roi = (0,2999,44,299) # 2nd CDS unit
    #roi = (0,2999,44,283) # 2nd CDS unit (minus last 4 columns)
    #roi = (0,2999,1525,1824)
    #roi = (1300,1699,44,299)
    #roi = (0,2999,0,3999)
    #roi = (0,2999,2000,2499)
    #roi = (0,2999,2200,2599)
    #roi = (0,2999,400,799)
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

    if bNoise:

        #directory_noise = os.path.join(directory,"RawImages")
        #directory_noise = os.path.join(directory,"RawImages_noise")
        #directory_noise = os.path.join(directory,"RawImages_dVscan")
        #directory_noise = os.path.join(directory,"RawImages_noise_LSBSwap")

        rn_noise = ReadNoise.ReadNoise(directory,
                                       file_wildcard = file_wildcard,
                                       rows = rows,
                                       columns = columns,
                                       param = param,
                                       num_skip_files = num_skip_files,
                                       num_files = num_files,
                                       num_files_ref = num_files_ref,
                                       bfullnoise = bfullnoise,
                                       b_load_all = b_load_all,
                                       param_label = param_label,
                                       param_unit = param_unit,
                                       param_cal = param_cal,
                                       param_cal_label = param_cal_label,
                                       param_cal_unit = param_cal_unit,
                                       channel_groups = channel_groups,
                                       roi = roi,
                                       show_channels = show_channels,
                                       file_wildcard_offset = file_wildcard_offset,
                                       num_files_offset = num_files_offset,
                                       nbins = nbins,
                                       conditions = conditions)
        
        rn_noise.info()
        rn_noise.analyze_readnoise(bFPN=bFPN,bRTN=bRTN,bsave=False,blog=True,directory_suffix=directory_suffix,linewidth=linewidth,bfullresolution=bfullresolution,rotation_xlabel=rotation_xlabel)
        #rn_noise.analyze_rownoise(bFPN=bFPN,bRTN=bRTN,bsave=True,blog=False,directory_suffix=directory_suffix)

    ###########
    # dV scan #
    ###########

    if bdVscan:
        print("Starting dV scan analysis")
        #directory_dVscan = os.path.join(directory,"RawImages_dVscan")
        #directory_dVscan = os.path.join(directory,"RawImages")
        param_label = 'V_RST - V_SIG'
        param_unit = 'Volt'
        #Vsig = numpy.arange(-0.8,0.9,0.1) # AFE DFT dV scan
        Vsig = numpy.arange(-0.6,1.8,0.1) # AFE CDS dV scan
        #Vsig = numpy.arange(-0.4,1.6,0.1) # CDS dV scan
        #Vsig = numpy.arange(0.6,0.71,0.1) # CDS dV scan
        #Vsig = numpy.arange(0.0,1.1,0.1) # AFE CDS dV scan
        param = ["%.1f"%(v if abs(v)>0.00001 else abs(v)) for v in Vsig]
        #param = ["%.2f"%(v if abs(v)>0.00001 else abs(v)) for v in Vsig]

        #fitrange = (0.0,0.6)
        #fitrange = (-0.7,-0.2)
        fitrange = 'best'

        rn_dVscan = ReadNoise.ReadNoise(directory,
                                        file_wildcard = file_wildcard,
                                        rows = rows,
                                        columns = columns,
                                        param=param,
                                        num_skip_files=num_skip_files,
                                        num_files_ref=num_files_ref,
                                        param_label=param_label,
                                        param_unit=param_unit,
                                        channel_groups=channel_groups,
                                        roi = roi,
                                        nbins=nbins)

        rn_dVscan.info()
        rn_dVscan.analyze_readnoise(bFPN=bFPN,bRTN=bRTN,bsave=False,blog=True,directory_suffix='dVscan_'+directory_suffix,linewidth=linewidth,bfit=True,fitrange=fitrange)
