#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy

from pyvisage import Image, 
from pyvisage import Crosstalk
from pyvisage import PlotTools

if __name__ == '__main__':

    #rawfile = "F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Ric\\GAIN CORRECTED - Q8A553-19#96-A1_3.0V_100ms_625nm_16FrameAvg_DFS.raw_AC.raw"
    #directory = "F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Ric"
    #directory = "Z:\\PC3\\CrossTalk\\Scripts\\plots"
    #directory = 'F:\\INVISAGE\PC3\\Crosstalk\\Data\\from_Ravi\\column_coupling_debug\\Q8A553-19#96-A1'
    #directory = 'F:\\INVISAGE\PC3\\Crosstalk\\Data\\from_Aurel'
    #directory = 'F:\\INVISAGE\PC3\\Crosstalk\\Data\\from_Aurel\\Q8A624w05#23-F_scriptMourad_LEDscan_v1_021314_144006'
    #directory = '\\\\INVCA-HV-D_PC1\\c$\\Users\\Aurel\\20140218\\xtalk_myScript_LEDscan_v1_021814_102059'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\Data\\from_Aurel\\20140218\\xtalk_myScript_LEDscan_v1_021814_102059'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\Data\\from_Aurel\\20140218\\xtalk_myScript_Vfilm_-0.5V_LEDscan_v0_021814_105716'
    #directory = 'C:\\Users\\Aurel\\20140218\\xtalk_myScript_LED_50_Vfilm_scan_v2_021814_143653'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140219\\xtalk_myScript_LED_50_Vfilm_scan_withDarks_v1_021914_112829'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MouradScript_LED_20_Vfilm_scan_v0_022014_113321'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MyScript_LED_20_Vfilm_scan_v0_022014_114348'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MouradScript_LED_20_Vfilm_scan_debug_LEDOn_v0_022014_132817'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MouradScript_LED_20_Vfilm_scan_debug_LEDOnOff_v0_022014_133130'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MyScript_4FPS_LED_20_Vfilm_scan_v0_022014_150005'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MyScript_1FPS_LED_20_Vfilm_scan_v0_022014_151115'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_MyScript_8FPS_LED_20_Vfilm_scan_v0_022014_150706'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_Q8A624w05#34-G_MyScript_4FPS_LED_20_Vfilm_scan_v0_022014_161843'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140220\\xtalk_Q8A624w05#34-G_MyScript_4FPS_LED_20_Vfilm_scan_v0_022014_161843'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140220\\xtalk_Q8A624w05#34-G_MyScript_4FPS_LED_20_Vfilm_scan_darkframes_v0_022014_162254'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140220\\xtalk_Q8A624w05#34-G_MyScript_4FPS_LED_20_Vfilm_scan_darkframes_v0_022014_162254'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_scan_Vfilm_-0.5V_v0_022414_153739'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_scan_Vfilm_-1.0V_v0_022414_154018'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_scan_Vfilm_-1.5V_v0_022414_160847'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_v0_022414_162230'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_RSoffduringRST_v0_022414_162700'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_readphasetimingdividedby2_v0_022414_162522'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_hardreset_v0_022414_162356'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140224\\xtalk_Q8A624w14#34-A_8FPS_LED_20_Vfilm_-1.0V_v0_022414_162818'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140219\\test'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Ric\\streaks'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Ric\\control_die'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140226\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_v0_022614_110911'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140226\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_hardreset_v0_022614_111045'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140227\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_hardsoftreset_v0_022714_182900'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140227\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_hardreset_v0_022714_183037'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140227\\xtalk_Q8A624w14#34-A_4FPS_LED_20_Vfilm_-1.0V_hardreset_enhardalwaysON_v0_022714_183402'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140228\\xtalk_Q8A624w14#34-A_4FPS_hardsoftreset_v0_022814_150637'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140228\\xtalk_Q8A624w14#34-A_4FPS_hardsoftreset_refrowcol_v0_022814_150828'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140228\\xtalk_Q8A624w14#34-A_4FPS_hardsoftreset_refrowcol_RSoffduringRST_v0_022814_151520'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140228\\xtalk_Q8A624w14#34-A_4FPS_hardreset_refrowcol_v0_022814_151647'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140228\\xtalk_Q8A624w14#34-A_4FPS_hardreset_enhardalwaysON_refrowcol_v0_022814_151830'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140227\\I_part_v0_022714_183801'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140303\\xtalk_Q8A636w14#56-A_4FPS_LED_20_Vfilm_-1.0V_v0_030314_155956'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140204\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_v0_MouradMachine_030414_104428'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140204\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_v3_030414_113207'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140204\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_new_v0_030414_163847'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140204\\xtalk_Q8A624w14#34-A_4FPS_hardsoftreset_refrowcol_v0_022814_150828'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_noDAC3_v0_030514_104324'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_DAC3_v0_030514_104452'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_DAC3_-0.5V_v0_030514_112127'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_DAC3_-0.5V_RSoffduringRST_v1_030514_113520'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A621w10#73-A_5Metal_LED_20_Vfilm_-1.0V_DAC3_-0.5V_v0_030514_113947'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A621w10#73-A_5Metal_LED_20_Vfilm_-1.0V_new_v0_030514_154902'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A621w10#73-A_5Metal_LED_20_Vfilm_scan_new_v0_030514_155621'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_build9_LED_20_Vfilm_scan_v0_030514_120828'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_run0_v0_030514_162012'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_run1_v0_030514_162110'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_run2_v0_030514_162207'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_run3_v0_030514_162305'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A624w14#34-A_LED_20_Vfilm_-1.0V_run4_v0_030514_162400'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#56-A_LED_20_Vfilm_scan_v0_030514_164759'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#56-A_LED_20_Vfilm_scan_withDark_v0_030514_165126'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0V_470nm_v0_030514_171922'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0V_440nm_v0_030514_172028'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_LED_scan_Vfilm_-1.0V_RSoffduringRST_v0_030514_180018'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0V_8FPS_v0_030514_181859'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140205\\xtalk_Q8A636w14#54-A_LED_scan_Vfilm_-1.0V_v0_030514_184217'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#56-A_LED_20_Vfilm_-1.0V_470nm_v0_030614_093527'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#36-I_LED_20_Vfilm_-1.0V_v0_030614_100231'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#46-I_LED_20_Vfilm_-1.0V_v0_030614_101325'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#54-A_LED_scan20_Vfilm_-1.0V_v0_030614_160439'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#54-A_LED_scan20_Vfilm_-1.0V_RSoffduringRST_v0_030614_160904'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#46-I_LED_20_Vfilm_-1.0_RSoffduringRST_v3_030614_164916'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#54-A_LED_8_Vfilm_-1.0_FullFrame_v0_030614_165732'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140206\\xtalk_Q8A636w14#54-A_LED_8_Vfilm_-1.0_FullFrame_RSoffduringRST_v0_030614_165621'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Carey\\Q8A638W22#64-F1_Post-VisEra_T60C_B-0.5V_030514_144351'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140305\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0V_run0_v0_030514_162012'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_DigVdd1.5_v1_031014_151009'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_DigVdd1.65_v0_031014_151107'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vrst_scan_v2_031014_153946'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vrst_scan_v3_031014_154252'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_scan_v0_031014_174154'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#65-G_LED_20_Vfilm_scan_v0_031014_175136'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_scan_Vrst_1.8V_v0_031014_182239'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_harsoftreset_v0_031014_184259'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_hardreset_v0_031014_184426'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140210\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_hardreset_enhardalwayson_v0_031014_184544'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140310\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_harsoftreset_v0_031014_184259'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140310\\xtalk_Q8A636w14#56-A_LED_20_Vfilm_scan_v0_030514_164759'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140212\\xtalk_Q8A636w14#32-A_LED_20_Vfilm_-1.0_v0_031214_133846'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140212\\xtalk_Q8A636w14#33-A_LED_20_Vfilm_-1.0_v0_031214_133615'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140212\\xtalk_Q8A636w14#33-A_LED_20_Vfilm_-1.0_Greenlight_v0_031214_134841'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140212\\xtalk_Q8A636w14#33-A_LED_20_Vfilm_-1.0_Greenlight_v1_031214_135415'
    #directory = 'C:\\Users\\Aurel\\DATA\\20140212\\xtalk_Q8A636w14#33-A_LED_20_Vfilm_-1.0_Bluelight_v0_031214_134957'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140312\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_Optoliner_red_v0_031214_173011'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140312\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_Optoliner_red_new_v0_031214_182116'
    #directory = 'F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Aurel\\20140312\\xtalk_Q8A636w14#54-A_LED_20_Vfilm_-1.0_Optoliner_red_noaperture_v1_031214_182921'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140324\\xtalk_Q8A636w14#54-A_630nm_4FPS_v0_032414_171007'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140324\\xtalk_Q8A636w14#54-A_630nm_8FPS_v0_032414_171256'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140324\\xtalk_Q8A636w14#54-A_630nm_4FPS_8FPSclockspeed_v0_032414_171142'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_8FPSscan_v0_032714_130503'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_12FPSscan_v0_032714_131100'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_4FPS_v0_032714_133925'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_4FPS_verticalflip_v0_032714_134035'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_8FPS_v0_032714_135403'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140327\\xtalk_Q8A636w14#54-A_630nm_8FPS_verticalflip_v1_032714_135538'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A636w14#54A_Red_Vfilm_scan_v0_060314_120606'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#44R_Red_Vfilm_scan_v0_060314_130137'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#55S_Red_Vfilm_scan_v0_060314_131032'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#51P_Red_Vfilm_scan_v1_060314_132445'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#51P_Red_Vgrid0.0V_Vfilm_scan_v0_060314_133011'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#51P_Red_Vgrid0.5V_Vfilm_scan_v0_060314_133700'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#51P_Red_Vgrid1.0V_Vfilm_scan_v0_060314_134719'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#51P_Red_Vgrid2.0V_Vfilm_scan_v0_060314_135341'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#55D_Red_Vfilm_scan_v0_060314_155138'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140603\\response_Q8A643w20#55D_Red_Vfilm_scan_v1_060314_160823'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140618\\xtalk_Q8A643w20#51P_Red_VgridVfilm_Vfilm_scan_v0_061814_190213'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140618\\xtalk_Q8A643w20#51P_Red_Vfilm-0.5_Vgrid_scan_v0_061814_190927'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_R_630nm_4FPS_83ms_Vfilm_scan_v0_070114_115141'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_Vfilm_scan_v0_070114_120001'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED20mA_Vfilm_scan_v0_070114_120356'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED40mA_Vfilm_scan_v0_070114_120713'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED60mA_Vfilm_scan_v0_070114_120928'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED80mA_Vfilm_scan_v0_070114_121155'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED50mA_Vfilm_scan_v0_070114_121503'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED30mA_Vfilm_scan_v0_070114_121719'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED10mA_Vfilm_scan_v0_070114_122001'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_FulFrame_LED7mA_Vfilm_scan_v0_070114_122712'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_200ms_LED8mA_Vfilm_scan_v0_070114_122944'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_100ms_LED17mA_Vfilm_scan_v0_070114_124303'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_50ms_LED33mA_Vfilm_scan_v0_070114_124520'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_20ms_LED83mA_Vfilm_scan_v0_070114_124723'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_10ms_LED166mA_Vfilm_scan_v0_070114_124930'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_5ms_LED332mA_Vfilm_scan_v0_070114_125218'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_2ms_LED830mA_Vfilm_scan_v0_070114_125450'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_630nm_4FPS_83ms_LED20mA_Vfilm_scan_v0_070114_125719'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_570nm_4FPS_83ms_LED20mA_Vfilm_scan_v0_070114_125942'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140701\\xtalk_Q8A643w21#33R_450nm_4FPS_83ms_LED20mA_Vfilm_scan_v0_070114_130150'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_FullFrame_LED7mA_Vfilm_scan_v0_070214_111643'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_FullFrameminus1line_LED7mA_Vfilm_scan_v0_070214_111928'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070214_112248'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_150ms_LED11mA_Vfilm_scan_v0_070214_112652'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_100ms_LED17mA_Vfilm_scan_v0_070214_113004'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_75ms_LED22mA_Vfilm_scan_v0_070214_113355'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_175ms_LED9mA_Vfilm_scan_v0_070214_113603'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_FullFrameminus16lines_LED7mA_Vfilm_scan_v0_070214_114826'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_FullFrameminus2lines_LED7mA_Vfilm_scan_v0_070214_115111'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140702\\xtalk_Q8A643w21#33R_630nm_4FPS_FullFrameminus3lines_LED7mA_Vfilm_scan_v0_070214_115336'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#33R_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_111001'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#35S_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v1_070714_111437'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_111848'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#31P_630nm_4FPS_125ms_LED13mA_VgridVfilm_Vfilm_scan_v0_070714_112908'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#31P_630nm_4FPS_125ms_LED13mA_Vgrid0V_Vfilm_scan_v0_070714_113111'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#31P_630nm_4FPS_125ms_LED13mA_Vgrid0.5V_Vfilm_scan_v0_070714_113319'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#31P_630nm_4FPS_125ms_LED13mA_Vgrid1.0V_Vfilm_scan_v0_070714_113522'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_630nm_4FPS_75ms_LED22mA_Vfilm_scan_v0_070714_114410'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_630nm_4FPS_175ms_LED9mA_Vfilm_scan_v0_070714_114651'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_114909'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_530nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_115120'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_470nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_115701'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A636w14#54A_630nm_4FPS_FullFrame_LED7mA_Vfilm_scan_v0_070714_121324'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#33R_630nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_121947'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#33R_530nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_122237'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#33R_470nm_4FPS_125ms_LED13mA_Vfilm_scan_v0_070714_122528'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#51P_630nm_4FPS_125ms_LED13mA_VgridVfilm_Vfilm_scan_v0_070714_132507'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#51P_630nm_4FPS_125ms_LED13mA_Vgrid0V_Vfilm_scan_v0_070714_132814'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#51P_630nm_4FPS_125ms_LED13mA_Vgrid-0.5V_Vfilm_scan_v2_070714_133227'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w20#51P_630nm_4FPS_125ms_LED13mA_Vgrid-1.0V_Vfilm_scan_v0_070714_133436'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8A643w21#51P_630nm_4FPS_125ms_LED13mA_VgridVfilm_Vfilm_scan_v1_070714_173647'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\xtalk_Q8AGGG_630nm_4FPS_125ms_LED13mA_VgridVfilm_Vfilm_scan_v1_070714_174237'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\'
    #directory = 'C:\\Users\\Aurel\\Crosstalk\\Data\\20140707\\'

    file_wildcard = 'RawImages\\Bright_%s\\*.raw'
    #file_wildcard = 'RawImages\\%s\\*.raw'
    #file_wildcard = 'RawImages\\%smA\\*.raw'
    #file_wildcard = 'BrightImage_%s*.raw'
    file_wildcard_offset = 'RawImages\\Dark_%s\\*.raw'
    #file_wildcard_offset = 'RawImages\\Dark\\*.raw'
    #file_wildcard_offset = 'Dark\\*.raw'
    #file_wildcard_offset = None
    
    #directory_suffix = 'v3_hot_with_without_ulens'
    #directory_suffix = 'v3_hot_Greensea'
    #directory_suffix = 'v3_hot_Greensea_redislands_withuLens'
    directory_suffix = 'v0'
    #directory_suffix = 'v4_withRAW'
    #directory_suffix = 'v5_withRAW'
    #directory_suffix = 'v4_withwithoutuLens'
    #directory_suffix = 'v4_withwithoutuLens_Bayer'
    #directory_suffix = 'v4_Greensea'
    #directory_suffix = 'v4_Greensea_redpix_withoutulens'
    #directory_suffix = 'v0_Greensea_redpix_withulens'
    #directory_suffix = 'v4_Greensea_redpix_withwithoutulens'
    #directory_suffix = 'v4_Bluesea'
    #directory_suffix = 'v4_Bluesea_redpix_withoutulens'
    #directory_suffix = 'v4_Bluesea_redpix_withulens'
    #directory_suffix = 'v4_Bluesea_redpix_withwithoutulens'
    #directory_suffix = 'v4_Bluesea_Greensea'

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

    #analysis_type = 1
    analysis_type = 2

    if analysis_type==1:

        #param = ['']
        #param = [10,20,30,40,50,60,70,80,90]
        param = [20]
        #param = range(1,9)
        #param = range(3,13)
        #param = [8]
        #param = [40]
        #param = range(1,21)
        param_label = "LED current"
        #param_label = "Frame Rate"
        param_unit = 'mA'
        #param_unit = 'FPS'
        #param_label = ""
        #param_unit = ''

    elif analysis_type==2:

        param_label = "Vfilm"
        #param_label = "Vgrid"
        #param_label = "Vrst_high"
        param_unit = 'Volt'
        #v_start = -2.0
        #v_stop = -2.0
        #v_stop = 2.2
        #v_stop = 0.9
        #v_start = -1.0
        #v_stop = -1.0
        #v_stop = -1.8 #1.3
        v_start = -2.0
        v_stop = 0.8
        dv = 0.2
        V = numpy.linspace(v_start,v_stop,round((v_stop-v_start)/dv+1))
        print(V)
        param =["%.1f"%(v if abs(v)>0.000001 else abs(int(v))) for v in V]
        #param=['-1.0']
        print(param)

    num_skip_files = 0
    #num_files = 25
    #num_files = 16
    num_files = 999
    num_files_ref = 0
    #num_files_offset = 25
    #num_files_offset = 64
    num_files_offset = 999

    rows = 3000
    columns = 4000
    datatype = 'uint16'
    #rows = 1200
    #columns = 1600
    #datatype = 'int16'

    #roi = None
    #roi = (999,999)
    #roi = (2000,2999,0,999)
    roi = (500,1499,500,1499) # CFA + uLens
    #roi = (1500,2199,1700,2299) # CFA + with/without uLens
    #roi = (350,649,2000,2499)
    #roi = (500,549,2150,2349)
    #roi = (2200,2999,800,1999) # Green sea
    #roi = (2300,2599,1702,1951) # Green sea redpix without ulens
    #roi = (2700,2999,1702,1951) # Green sea redpix with ulens
    #roi = (2300,2999,1702,1951) # Green sea redpix with and without ulens
    #roi = (2200,2999,1900,3099) # Blue sea
    #roi = (2300,2599,2800,3049) # Blue sea redpix without ulens
    #roi = (2700,2999,2800,3049) # Blue sea redpix with ulens
    #roi = (2300,2999,800,3099) # Blue and Green sea
    #roi = (2300,2899,1700,1949) # red island in green sea with/without ulens
    #roi = (2500,2899,1702,1951) # red island in green sea with ulens
    #roi = (1400,1999,400,1399)# with/without ulens
    #roi = (100,2899,0,255) # first 256 columns (5-Metal part)
    if roi!=None:
        roi_suffix = '_roi'
        for r in roi:
            roi_suffix += '_%i'%r
        directory_suffix += roi_suffix

    bfullresolution = False
    if bfullresolution:
        directory_suffix += '_fullres'
    
    blog = False

    channel_groups = (2,2)
    #channel_groups = (4,4)
    #channel_groups = (5,5)
    i_main_channel = 0
    #i_main_channel = 12

    PlotTools.set_figure_font()

    xt = Crosstalk.Crosstalk(directory,
                             file_wildcard = file_wildcard,
                             rows = rows,
                             columns = columns,
                             datatype = datatype,
                             param = param,
                             num_skip_files = num_skip_files,
                             num_files = num_files,
                             num_files_ref = num_files_ref,
                             param_label = param_label,
                             param_unit = param_unit,
                             channel_groups = channel_groups,
                             roi = roi,
                             file_wildcard_offset = file_wildcard_offset,
                             num_files_offset = num_files_offset,
                             bswap = bswap)

    xt.analyze_crosstalk(i_main_channel=i_main_channel,bFPN=bFPN,bRTN=bRTN,rtn_colstart=rtn_colstart,rtn_colstop=rtn_colstop,directory_suffix=directory_suffix,bsave=False,bfullresolution=bfullresolution,blog=blog)

    # cross-check on Ric's xtalk heatmap (horizontal)
    bxcheck = False
    if bxcheck:

        file_heatmap = "F:\\INVISAGE\\PC3\\Crosstalk\\Data\\from_Ric\\GrOverR.txt"
        
        f_heatmap = open(file_heatmap)
        lines_heatmap = f_heatmap.readlines()
        val = []
        for i in range(len(lines_heatmap)):
            val.append(lines_heatmap[i].split(',')[:-1])

        arr = numpy.array(val).astype('float32')
        print("Heatmap shape:", arr.shape)
        
        im_heatmap = Image.Image(arr)
        
        im_heatmap.plot_image(minval=0.3,maxval=0.5,bsave=True,filename=os.path.join(directory,'Ric_xtalk.png'))
