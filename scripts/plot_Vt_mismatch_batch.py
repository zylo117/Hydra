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
    im.set_channel_groups((1,4))
    im.FPN_correction(rowstart=0,rowstop=2999,target=0)
    im.RTN_correction(False,colstart=0,colstop=3999,target=0)
    im.multiply(-1/4000.*1200) # conversion to Vt (minus because DN = rst-sig = Vpix-Vt-DAC)

    return im


#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_35B_Vt_mismatch\\RawImages\\image_hard_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_24L_Vt_mismatch\\RawImages\\image_hard2_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_24L_Vt_mismatch\\RawImages\\image_hardsoft2_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150212\\RTO#3_35B_Vt_mismatch\\RawImages\\image_1.700_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A685w06#85C_VTmismatch_normalVt\\RawImages\\image_hard_1.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\Q8A685w06#85C_VTmismatch_normalVt\\RawImages\\image_hardsoft_1.raw")
# clipped at 0
raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W13*\\HardSoft\\image_0.raw")
raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W13*\\Hard\\image_0.raw")
# good
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A693W19#3[3,5]*\\HardSoft\\image_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A693W19#3[3,5]*\\Hard\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A693W19*\\HardSoft\\image_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A693W19*\\Hard\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W23*\\HardSoft\\image_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W23*\\Hard\\image_0.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W24*\\HardSoft\\image_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W24*\\Hard\\image_0.raw")
raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W24#53*\\HardSoft\\image_0.raw")
raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W24#53*\\Hard\\image_0.raw")
print(raw0)
print(raw0_hard)

#raw0 = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W23*\\HardSoft\\image_0.raw")
#raw0_hard = glob.glob("F:\\INVISAGE\\PC5\\VT_mismatch\\Data\\20150410\\new2\\Q8A690W23*\\Hard\\image_0.raw")
legend0 = 'Normal wafer'
bcomp = True

#im0 = Image.Image(raw0[0])
#im0.set_channel_groups((1,4))
#im0.FPN_correction(rowstart=0,rowstop=2999,target=0)
#im0.RTN_correction(False,colstart=0,colstop=3999,target=0)
#im0.multiply(-1/4000.*1200) # conversion to Vt (minus because DN = rst-sig = Vpix-Vt-DAC)

#im0.plot_histogram(xlabel="SF+RST Vt [mV]",xmin=-150,xmax=150)
#im0.plot_histogram(xlabel="SF+RST Vt [mV]",xmin=-300,xmax=300,blog=True)
#im0.plot_image(title="SF+RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
#print "RST+SF Vt:",im0.get_rms_channel_groups()

#im0_hard = Image.Image(raw0_hard[0])
#im0_hard.set_channel_groups((1,4))
#im0_hard.FPN_correction(rowstart=0,rowstop=2999,target=0)
#im0_hard.RTN_correction(False,colstart=0,colstop=3999,target=0)
#im0_hard.multiply(-1/4000.*1200) # conversion to Vt (minus because DN = rst-sig = Vpix-Vt-DAC)

Array_SF_Vts = []
Array_RST_Vts = []

for i in range(len(raw0_hard)):

    im0 = get_mV_image(raw0[i])
    array_Vt = im0.get_array()

    im0_hard = get_mV_image(raw0_hard[i])
    array_Vt_sf = im0_hard.get_array()
    array_Vt_rst = array_Vt - array_Vt_sf
    Array_SF_Vts.append(array_Vt_sf)
    Array_RST_Vts.append(array_Vt_rst)
    im0.subtract(im0_hard)

    '''
    # SF vs RST Vt
    pylab.hist2d(array_Vt_sf.flatten(),array_Vt_rst.flatten(),bins=200,range=[[-150,150],[-150,150]])
    pylab.xlabel(r'$\Delta$ SF Vgs [mV]')
    pylab.ylabel(r'$\Delta$ RST Vt [mV]')
    pylab.grid(True)
    pylab.show()
    '''

    #im0_hard.plot_histogram(xlabel=r'$\Delta$ SF Vgs [mV]',xmin=-150,xmax=150)

    #im0_hard.plot_histogram(xlabel="SF Vt [mV]",xmin=-300,xmax=300,blog=True)
    #im0_hard.plot_image(title="SF Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
    print(raw0_hard[i])
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa SF Vt:",im0_hard.get_rms_channel_groups())
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb RST Vt:",im0.get_rms_channel_groups())

    #im0.plot_histogram(xlabel="RST Vt [mV]",xmin=-300,xmax=300,blog=True)
    #im0.plot_image(title="RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
    im0_hard.plot_image(title="SF Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)

# RST Vt comparison between sensor
#pylab.hist2d(Array_RST_Vts[0].flatten(),Array_RST_Vts[1].flatten(),bins=200,range=[[-100,100],[-100,100]])
#pylab.xlabel(r'$\Delta$ RST Vt - Sensor 1 [mV]')
#pylab.ylabel(r'$\Delta$ RST Vt - Sensor 2 [mV]')
#pylab.grid(True)
#pylab.show()

'''
if bcomp:
    im1.subtract(im1_hard)
    im0.plot_histogram(xlabel=r'$\Delta$ RST Vt [mV]',xmin=-150,xmax=150, legend_label=legend0 ,image2=im1, legend_label2=legend1, legend_location='upper right')
else:
    im0.plot_histogram(xlabel=r'$\Delta$ RST Vt [mV]',xmin=-150,xmax=150)
#im0.plot_histogram(xlabel="RST Vt [mV]",xmin=-300,xmax=300,blog=True)
#im0.plot_image(title="RST Vt mismatch",colorscale='hot',colorbar_label='mV',minval=-150,maxval=150)
print "RST Vt:",im0.get_rms_channel_groups()
if bcomp: print "RST Vt:",im1.get_rms_channel_groups()
'''

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

