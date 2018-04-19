import pylab
import glob
from pyvisage import Image
from pyvisage import ImageArray

#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut\\RawImages\\image_2.0_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140912\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut_AVDD15_1.8V\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140912\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut_AVDD15_1.8V\\RawImages\\image_2.0_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140912\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut_AVDD15_1.8V\\RawImages\\image_2.0_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140912\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut_AVDD15_1.8V\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut\\RawImages\\image_2.8_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut\\RawImages\\image_2.0_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140911\\Q8A670w10#54E_afterFIB_DAC01_2.8V_PWRAN2_scan_afterwirebondcut\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140915\\Q8A671w02#72C_VANA28_2.5V_VANA15_1.8V\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140915\\Q8A670w12#33A_VANA28_2.5V_VANA15_1.8V\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140915\\Q8A671w02#72C_VANA28_2.8V_VANA15_1.5V\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140915\\Q8A670w12#33A_VANA28_2.8V_VANA15_1.5V\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140916\\Q8A670w12#33A\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140916\\Q8A670w12#33A_AZoff\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140916\\Q8A671w02#72C\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140916\\Q8A671w02#72C_AZoff\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140919\\Q8A670w12#33A\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140919\\Q8A670w12#33A_AZoff\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140919\\Q8A670w12#33A_pdlookahead3\\RawImages\\Image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140919\\Q8A670w12#33A_AZoff_pdlookahead3\\RawImages\\Image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_20140922_122039\\RawImages\\image_2.0_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_20140922_122039\\RawImages\\image_2.8_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_VANA15_1.5V_PWRAN2scan_20140922_141431\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_175715\\RawImages\\image_2.0_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_PWRAN2scan_1to3V_20140922_175715\\RawImages\\image_2.8_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20140922\\Q8A670w10#54E_afterFIB_specialWB_VANA15_1.5V_PWRAN2scan_1to3V_20140922_170932\\RawImages\\image_2.8_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20141030\\RTO2_test\\crushed_current_source_0dB_AZon\\RawImages\\image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\CFPN\\Data\\20150105\\Q8A685W13#23-C1_20150105_135038\\RawImages\\image_0.raw")
raw0 = glob.glob("F:\\INVISAGE\\PC6\\Bringup\\Data\\20150511\\pc6_new_bringup_cds_dV_scan_20150511_170111\\RawImages\\image_0.800_0000.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC6\\Bringup\\Data\\20150511\\pc6_new_bringup_cds_dV_scan_20150511_170111\\RawImages\\image_0.800_0000.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC6\\Bringup\\Data\\20150514\\46A\\RawImages\\image_0000.raw")
raw1 = glob.glob("F:\\INVISAGE\\PC6\\Bringup\\Data\\20150514\\large_offset\\RawImages\\LARGE_cds_OFFSET_0000.raw")
raw1 = glob.glob("F:\\INVISAGE\\PC6\\Bringup\\Data\\20150514\\large_offset\\RawImages\\LARGE_cds_OFFSET_AFE_test_0000.raw")

#label0 = r'$C_{sampling}$ = 200fF (Q8A671w02#72C)'
#label1 = r'$C_{sampling}$ = 100fF (Q8A670w12#33A)'
#label0 = r'$C_{sampling}$ = 200fF - VANA28=2.5V - VANA15=1.8V'
#label1 = r'$C_{sampling}$ = 200fF - VANA28=2.8V - VANA15=1.5V'
#label0 = r'$C_{sampling}$ = 100fF - VANA28=2.5V - VANA15=1.8V'
#label1 = r'$C_{sampling}$ = 100fF - VANA28=2.8V - VANA15=1.5V'
#label0 = 'AZ enabled'
#label1 = 'AZ disabled'
#label0 = 'PWRAN2 = 2.0V'
#label1 = 'PWRAN2 = 2.8V'
label0 = 'RTO#2 - C die'
#label1 = 'RTO#3 - C die'
label1 = 'pc6'
#label0 = 'VANA15 = 1.8V'
#label1 = 'VANA15 = 1.5V'
#label0 = 'post-FIB'
#label1 = 'pre-FIB'

rows = 3000
columns = 4000
#rows = 3065
#columns = 4064

#im0 = ImageArray.ImageArray(raw0,rows=rows,columns=columns).average()
im0 = ImageArray.ImageArray(raw0,rows=3000,columns=4000).average()
im1 = ImageArray.ImageArray(raw1,rows=rows,columns=columns).average()

#im1.subtract(im0)

#im0.set_ROI((0,2999,1500,1999)) # CDS amp #2
#im1.set_ROI((0,2999,1500,1999)) # CDS amp #2
im1.set_ROI((0,2999,1832,2340)) # CDS amp #9 & 10
#im1.set_ROI(1300,1699,144,1299) # in region where bot vcmi switches are off
#im0.set_ROI((999,999))
#im1.set_ROI((999,999))
#im0.set_ROI((2899,2899))
#im1.set_ROI((2899,2899))
#im0.set_ROI((100,2999,2900,3899))
#im1.set_ROI((100,2999,2900,3899))
#im0.set_ROI((100,2999,3156,3411))
#im1.set_ROI((100,2999,3156,3411))
#im0.set_ROI((100,2999,1000,1254))
#im1.set_ROI((100,2999,1000,1254))
#im0.set_ROI((100,2999,500,1499))
#im1.set_ROI((100,2999,500,1499))

im0.set_channel_groups((1,4))
im1.set_channel_groups((1,4))
#im1.set_channel_groups((1,1))

print(im0.get_rms_channel_groups())
print(im1.get_rms_channel_groups())

#im1.plot_image(bstack=True)
#im1.plot_image()

#im1.plot_histogram(xmin=0,xmax=4096,image2=im0,blog=True)
#im1.plot_histogram(legend_label='AVDD28 = 2.0V',image2=im0,legend_label2='AVDD28 = 2.8V')
#im1.plot_histogram(show_channels=[0,2],xmin=0,xmax=4096,nbins=200,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')
#im1.plot_histogram(show_channels=[0,2],xmin=0,xmax=4096,nbins=200,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')


#im1.plot_profile(xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='lower left')
#im1.plot_profile(show_channels=[0,2],xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='upper center')
#im1.plot_profile(xlabel='Column',color='r',ylim=[750,1650],legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='upper center')
#im0.plot_profile(show_channels=[0,2],xlabel='Column',color='r',legend_label=label1,legend_location='upper center')
#im1.plot_profile(legend_label='VANA28 = 2.8V',image2=im0,legend_label2='VANA28 = 2.0V')
#im1.plot_profile(legend_label='pre-FIB',image2=im0,legend_label2='post-FIB')

#im1.plot_profile(xlabel='Column',color='b',legend_label=label1,legend_location='upper center')
#im1.plot_profile(xlabel='Column',color='b',ylim=[1900,2500])
#im1.plot_profile(xlabel='Column',color='b',ylim=[1700,2600])
#im1.plot_profile(xlabel='Column',color='b',ylim=[0,4000])
im1.plot_profile(xlabel='Column',color='b')
#im1.plot_profile(xlabel='Column',color='b',bstack=True)
