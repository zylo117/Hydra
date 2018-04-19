import pylab
import glob
from pyvisage import Image

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)

def get_mV_image(raw):

    im = Image.Image(raw)
    #im.set_channel_groups((1,4))
    im.FPN_correction(rowstart=0,rowstop=2999,target=0)
    im.RTN_correction(False,colstart=0,colstop=3999,target=0)
    #im.multiply(-1/4000.*1200) # conversion to mV (minus because DN = rst-sig = Vpix-Vt-DAC)
    im.multiply(-1/511.*1000) # conversion to mV (minus because DN = rst-sig = Vpix-Vt-DAC)

    return im


#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_35B_Vt_mismatch\\RawImages\\image_hard_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_24L_Vt_mismatch\\RawImages\\image_hard2_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_24L_Vt_mismatch\\RawImages\\image_hardsoft2_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_35B_Vt_mismatch\\RawImages\\image_1.700_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A685w06#85C_VTmismatch_normalVt\\RawImages\\image_hard_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A685w06#85C_VTmismatch_normalVt\\RawImages\\image_hardsoft_1.raw")
raw0_hard = glob.glob("F:\\INVISAGE\\Q13S\\VT_mismatch\\Data\\20160303\\test1\\image_singleSampling_HS_0003.raw")
raw0 = glob.glob("F:\\INVISAGE\\Q13S\\VT_mismatch\\Data\\20160303\\test1\\image_singleSampling_hard_0003.raw")
#legend0 = 'Normal wafer'
#legend0 = 'Standard SF'
legend0 = 'Q8A685w06#85C'

print(raw0)
print(raw0_hard)

bcomp = False
if bcomp:
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A693w18#55C_VTmismatch_lowVt\\RawImages\\image_hard_1.raw")
    #raw1 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A693w18#55C_VTmismatch_lowVt\\RawImages\\image_hardsoft_1.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#64A\\RawImages\\Hard\\image_hard_0.raw")
    #raw1 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#64A\\RawImages\\HardSoft\\image_hardsoft_0.raw")
    raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#76A\\RawImages\\Hard\\image_hard_0.raw")
    raw1 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#76A\\RawImages\\HardSoft\\image_hardsoft_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\Q8A690W24#13-C3_20150410_105401\\Dark\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\Q8A690W24#22-C3_20150410_105421\\Dark\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\Q8A693W19#24-C3_20150410_120336\\Dark\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new\\Q8A690W13#22-C3_20150410_154022\\Hard\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new\\Q8A693W19#24-C3_20150410_155153\\Hard\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new\\Q8A690W24#13-C3_20150410_151804\\Hard\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new\\Q8A690W23#22-C3_20150410_153020\\Hard\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new\\Q8A690W23#24-C3_20150410_153057\\Hard\\image_0.raw")
    #raw1_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W24#62-C3_20150410_152450\\Hard\\image_1.raw")
    #legend1 = 'Low SF Vt'
    #legend1 = 'Reduced LDD'
    #legend1 = 'low SF Vt + Reduced LDD'
    legend1 = 'Q8A672w08#76A'

#im0 = Image.Image(raw0[0])
#im0.set_channel_groups((1,4))
#im0.FPN_correction(rowstart=0,rowstop=2999,target=0)
#im0.RTN_correction(False,colstart=0,colstop=3999,target=0)
#im0.multiply(-1/4000.*1200) # conversion to Vt (minus because DN = rst-sig = Vpix-Vt-DAC)

im0 = get_mV_image(raw0[0])
array_Vt = im0.get_array()

if bcomp:
    im1 = get_mV_image(raw1[0])
    array1_Vt = im1.get_array()

#im0.plot_histogram(xlabel="SF+RST Vt [mV]",xmin=-150,xmax=150)
#im0.plot_histogram(xlabel="SF+RST Vt [mV]",xmin=-300,xmax=300,blog=True)
#im0.plot_image(title="SF+RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
#print "RST+SF Vt:",im0.get_rms_channel_groups()

#im0_hard = Image.Image(raw0_hard[0])
#im0_hard.set_channel_groups((1,4))
#im0_hard.FPN_correction(rowstart=0,rowstop=2999,target=0)
#im0_hard.RTN_correction(False,colstart=0,colstop=3999,target=0)
#im0_hard.multiply(-1/4000.*1200) # conversion to Vt (minus because DN = rst-sig = Vpix-Vt-DAC)

im0_hard = get_mV_image(raw0_hard[0])
array_Vt_sf = im0_hard.get_array()
array_Vt_rst = array_Vt - array_Vt_sf

if bcomp:
    im1_hard = get_mV_image(raw1_hard[0])
    array1_Vt_sf = im1_hard.get_array()
    #array1_Vt_rst = array1_Vt - array1_Vt_sf

# SF vs RST Vt
pylab.hist2d(array_Vt_sf.flatten(),array_Vt_rst.flatten(),bins=200,range=[[-150,150],[-150,150]])
pylab.xlabel(r'$\Delta$ SF Vgs [mV]')
pylab.ylabel(r'$\Delta$ RST Vt [mV]')
pylab.grid(True)
pylab.show()
'''
if bcomp:
    pylab.hist2d(array1_Vt_sf.flatten(),array1_Vt_rst.flatten(),bins=200,range=[[-150,150],[-150,150]])
    pylab.xlabel(r'$\Delta$ SF Vgs [mV]')
    pylab.ylabel(r'$\Delta$ RST Vt [mV]')
    pylab.grid(True)
    pylab.show()
'''
if bcomp:
    im0_hard.plot_histogram(xlabel=r'$\Delta$ SF Vgs [mV]',xmin=-150,xmax=150, legend_label=legend0, image2=im1_hard, legend_label2=legend1, legend_location='upper right')
    im1_hard.plot_image(title="SF Vgs mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
    im1_hard.save2raw(filename="F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#76A\\Plots\\SF_Vgs.raw")
else:
    im0_hard.plot_histogram(xlabel=r'$\Delta$ SF Vgs [mV]',xmin=-150,xmax=150)
    #im0_hard.plot_histogram(xlabel="SF Vt [mV]",xmin=-300,xmax=300,blog=True)
    im0_hard.plot_image(title="SF Vgs mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
print("SF Vt:",im0_hard.get_rms_channel_groups())
if bcomp: print("SF Vt:",im1_hard.get_rms_channel_groups())

im0.subtract(im0_hard)
if bcomp:
    im1.subtract(im1_hard)
    im0.plot_histogram(xlabel=r'$\Delta$ RST Vt [mV]',xmin=-150,xmax=150, legend_label=legend0 ,image2=im1, legend_label2=legend1, legend_location='upper right')
    im1.plot_image(title="RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
    im1.save2raw(filename="F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150420\\Q8A672w08#76A\\Plots\\RST_Vt.raw")
else:
    im0.plot_histogram(xlabel=r'$\Delta$ RST Vt [mV]',xmin=-150,xmax=150)
    #im0.plot_histogram(xlabel="RST Vt [mV]",xmin=-300,xmax=300,blog=True)
    im0.plot_image(title="RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
print("RST Vt:",im0.get_rms_channel_groups())
if bcomp: print("RST Vt:",im1.get_rms_channel_groups())

##im0.plot_histogram(xlabel="mV")
##im0.plot_histogram(xlabel="mV",blog=True)
##im0.plot_image(title="SF Vt mismatch",colorscale='hot',colorbar_label='mV')
##im0.plot_image(bstack=True,title="SF Vt mismatch")
##im0.plot_histogram(xlabel="mV",xmin=-200,xmax=200)
##im0.plot_histogram(xlabel="mV",blog=True,xmin=-300,xmax=300)
##im0.plot_image(title="SF Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-200,maxval=200)
##print im0.get_rms_channel_groups()

'''
import pickle, PlotTools, numpy
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.2V_1000images\\analysis_pixhist_test7_image\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.35V_1000images\\analysis_pixhist_v0_image\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.40V_1000images\\analysis_pixhist_v0_image\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.30V_1000images\\analysis_pixhist_v0_image\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_tapering_2.35V_1000images\\analysis_pixhist_v0_image\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150218\\RTO#3_24L_1000images_staircase2.35V_dT_scan_20150218_102828\\analysis_pixhist_v0_2.3us\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_tapering_2.40V_1000images\\analysis_pixhist_v0\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_hardRST_1000images\\analysis_pixhist_v0\\pickle_RMS_pixel.p", "rb" ) )
#array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_hardsoftRST_1000images\\analysis_pixhist_v0\\pickle_RMS_pixel.p", "rb" ) )
array_noise = pickle.load( open( "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_24L_1000images_GPIB_tapering_dT_scan_20150226_123541\\analysis_pixhist_v0_18.2us\\pickle_RMS_pixel.p", "rb" ) )
#PlotTools.plot_histogram(array_noise,nbins=200,blog=False,xmin=4,xmax=13)

#print array_Vt[1400:1600,1900:2100]
#print array_noise[0][1400:1600,1900:2100]

#pylab.scatter(array_Vt,array_noise[0])
#pylab.scatter(array_Vt[1400:1600,1900:2100],array_noise[0][1400:1600,1900:2100])
#pylab.hist2d(array_Vt[1400:1600,1900:2100].flatten(),array_noise[0][1400:1600,1900:2100].flatten(),bins=200)
#pylab.hist2d(array_Vt[1000:2000,1500:2500].flatten(),array_noise[0][1000:2000,1500:2500].flatten(),bins=200)
pylab.hist2d(array_Vt.flatten(),array_noise[0].flatten(),bins=200,range=[[-150,150],[5,14]])
#pylab.hist2d(array_Vt_rst.flatten(),array_noise[0].flatten(),bins=200,range=[[-150,150],[5,14]])

pylab.xlabel('Vt: SF+RST [mV]')
#pylab.xlabel('Vt: RST [mV]')
pylab.ylabel('Pixel Temporal Noise [DN]')

pylab.grid(True)
pylab.show()
'''
#im0.set_channel_groups((1,4))
#im0.FPN_correction(rowstart=0,rowstop=2999,target=0)
#im0.RTN_correction(False,colstart=0,colstop=3999,target=0)
#im0.multiply(1/4000.*1200)

