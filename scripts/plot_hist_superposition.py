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
raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.2uA_0.raw")
raw0_ref = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.2uA_1.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.7uA_0.raw")
#raw1_ref = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.7uA_1.raw")
raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.1uA_0.raw")
raw1_ref = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.1uA_1.raw")

#label0 = r'$C_{sampling}$ = 200fF (Q8A671w02#72C)'
#label1 = r'$C_{sampling}$ = 100fF (Q8A670w12#33A)'
#label0 = r'$C_{sampling}$ = 200fF - VANA28=2.5V - VANA15=1.8V'
#label1 = r'$C_{sampling}$ = 200fF - VANA28=2.8V - VANA15=1.5V'
#label0 = r'$C_{sampling}$ = 100fF - VANA28=2.5V - VANA15=1.8V'
#label1 = r'$C_{sampling}$ = 100fF - VANA28=2.8V - VANA15=1.5V'
#label0 = 'AZ enabled'
#label1 = 'AZ disabled'
label0 = 'Itaper = 0.2 uA'
label1 = 'Itaper = 0.1 uA'
#label0 = 'VANA15 = 1.8V'
#label1 = 'VANA15 = 1.5V'
#label0 = 'post-FIB'
#label1 = 'pre-FIB'

im0 = ImageArray.ImageArray(raw0).average()
im1 = ImageArray.ImageArray(raw1).average()

im0_ref = ImageArray.ImageArray(raw0_ref).average()
im1_ref = ImageArray.ImageArray(raw1_ref).average()

im0.subtract(im0_ref)
im1.subtract(im1_ref)

im0.multiply(1/2**0.5)
im1.multiply(1/2**0.5)

#im0.set_ROI((0,2999,1500,1999)) # CDS amp #2
#im1.set_ROI((0,2999,1500,1999)) # CDS amp #2
#im1.set_ROI(1300,1699,144,1299) # in region where bot vcmi switches are off
im0.set_ROI((999,999))
im1.set_ROI((999,999))

im0.set_channel_groups((1,4))
im1.set_channel_groups((1,4))

print(im0.get_rms_channel_groups())
print(im1.get_rms_channel_groups())

#im1.plot_image(bstack=True)
#im1.plot_image()

#im1.plot_histogram(xmin=0,xmax=4096,image2=im0,blog=True)
#im1.plot_histogram(legend_label=label0,image2=im0,legend_label2=label1)
im1.plot_histogram(xmin=-100,xmax=100,nbins=100,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')
#im1.plot_histogram(show_channels=[0,2],xmin=0,xmax=4096,nbins=200,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')


#im1.plot_profile(xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='lower left')
#im1.plot_profile(show_channels=[0,2],xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='upper center')
#im0.plot_profile(show_channels=[0,2],xlabel='Column',color='r',legend_label=label1,legend_location='upper center')
#im1.plot_profile(legend_label='VANA28 = 2.8V',image2=im0,legend_label2='VANA28 = 2.0V')
#im1.plot_profile(legend_label='pre-FIB',image2=im0,legend_label2='post-FIB')
