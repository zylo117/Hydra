import numpy
import pylab
import glob
import os
from pyvisage import Image
from pyvisage import ImageArray
from pyvisage import PlotTools

#directory = "F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A636w14#54A_baselineSensor"
#directory = "F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A661w01#64F_normalVT"
#directory = "F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A661w07#73F_lowVT"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150122\\RTO#3_23B_DAC4_0.75V_VLN2.1V"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150122\\RTO#3_23B_DAC4_0.0V_VLN2.3V"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150122\\RTO#3_23B_DAC4_0.75V_VLN2.3V"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_taper2.3to2.1_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_taper0.2to0.0_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.2V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.3V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.1V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.25V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.15V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.125V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.175V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.225V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_staircase2.275V_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_hardRST_NoLN_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150126\\RTO#3_35B_crushedcurrent_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.35V_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.40V_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_staircase_2.30V_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_tapering_2.35V_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150218\\RTO#3_24L_1000images_staircase2.35V_dT_scan_20150218_102828"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_hardRST_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_tapering_2.40V_1000images"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_24L_hardsoftRST_1000images"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150217\\RTO#3_13B_afterFIB_GPIB_baseline_scanVPIX2.2V_20150219_154807"
directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20150226\\RTO#3_24L_1000images_GPIB_tapering_dT_scan_20150226_123541"
directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_1000images_scan_20150615_171803"
directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_1000images_scan_20150615_172132"
#directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_HardSoft_1000images_scan_20150615_173850"
#directory = "F:\\INVISAGE\\PC6\\Noise\\Data\\20150611\\33A5_Elec_1000images_scan_20150615_174518"

#raw0 = glob.glob("F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A661w01#64F_normalVT\\RawImages\\image_[3]?.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A661w01#64F_normalVT\\RawImages\\image_3[3,4].raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A636w14#54A_baselineSensor\\RawImages\\image_3[3,4].raw")
#raw0 = glob.glob(os.path.join(directory,"RawImages\\image_[3,4]?.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages\\image_[3,4].raw"))
raw0 = glob.glob(os.path.join(directory,"RawImages\\image_000?.raw"))
raw0 = glob.glob(os.path.join(directory,"RawImages\\image_01??.raw"))
raw0 = glob.glob(os.path.join(directory,"RawImages\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages\\image_18.2_*.raw"))
#raw0 = glob.glob("F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A636w14#54A_baselineSensor\\RawImages\\image_3??.raw")
#raw0 = glob.glob("F:\\INVISAGE\\PC3\\Low_SF_VT_device\\Data\\20141209\\Q8A661w07#73F_lowVT\\RawImages\\image_[3]?.raw")
#raw0_ref = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.2uA_1.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.1uA_0.raw")
#raw1_ref = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20141028\\Q8A672w15#52B_Itaper_scan_wait10_20141028_154811\\RawImages\\image_0.1uA_1.raw")

#suffix_analysis = 'v6_image_wholeimage'
suffix_analysis = 'v2'

Nimages = len(raw0)
print("Number of images found:",Nimages)

#rows = 3000
#columns = 4000
#rows_roi = 1000
#columns_roi = 1000
rows_roi = 3000
columns_roi = 4000
roi = (rows_roi-1,columns_roi-1)
roi = (0,2999,294,797) # CDS 3-4

nbins = 200
#xmin,xmax = None,None
xmin = 6
#xmin = 0
xmax = 10
#xmax = 9

channel_groups = (1,4)
#channel_groups = (1,1)
num_channels = channel_groups[0] * channel_groups[1]

bswap = False

Npixels = 10 # number of pixel histogram to plot for each channel
PTN_min = 10.0
PTN_max = 10.5

im0 = Image.Image(raw0[0])
im0.set_channel_groups(channel_groups)
im0.set_ROI(roi)

tmp_mean = []
tmp_mean_row = []
tmp_mean_column = []
tmp_rms = []
tmp_rms_row = []
tmp_rms_column = []
for i_channel_group in range(num_channels):
    tmp_mean.append(im0.zeroarray(bROI=True,channel=i_channel_group))
    tmp_mean_row.append(numpy.zeros(tmp_mean[-1].shape[0]))
    tmp_mean_column.append(numpy.zeros(tmp_mean[-1].shape[1]))
    tmp_rms.append(im0.zeroarray(bROI=True,channel=i_channel_group))
    tmp_rms_row.append(numpy.zeros(tmp_rms[-1].shape[0]))
    tmp_rms_column.append(numpy.zeros(tmp_rms[-1].shape[1]))

print("Computing mean")

for raw in raw0:

    print(raw)
    im = Image.Image(raw)
    if bswap: im.column_swap()
    im.set_channel_groups(channel_groups)
    #im.set_ROI((rows_roi-1,columns_roi-1))
    im.set_ROI(roi)
    #im.RTN_correction()

    for i_channel_group in range(num_channels):
        tmp_mean[i_channel_group] += im.get_array(i_channel_group=i_channel_group)
        tmp_mean_row[i_channel_group] += im.get_profile(axis=1,i_channel_group=i_channel_group)
        tmp_mean_column[i_channel_group] += im.get_profile(axis=0,i_channel_group=i_channel_group)

Mean = numpy.array(tmp_mean) / float(Nimages)
Mean_row = numpy.array(tmp_mean_row) / float(Nimages)
Mean_column = numpy.array(tmp_mean_column) / float(Nimages)

mean = Mean.mean(axis=1).mean(axis=1)
mean_row  = Mean_row.mean(axis=1)
mean_col = Mean_column.mean(axis=1)

print("mean:", mean)
print("mean row:", mean_row)
print("mean col:", mean_col)

#im0 = Image.Image(raw0[0])
#im0.set_ROI((rows_roi-1,columns_roi-1))
#im0.set_ROI(roi)
#pr0 = im0.get_profile(axis=1)
#pylab.plot(pr0)
#pylab.plot(Mean_row)

#im0 = Image.Image(raw0[0])
#im1 = Image.Image(raw0[1])
#im0.subtract(im1)
#im0.set_ROI((rows_roi-1,columns_roi-1))
#im0.set_ROI(roi)
#im0.set_channel_groups((1,4))
#im0.column_swap()
#im0.set_ROI((1000,1999,4,67))
#im0.set_ROI((0,2999,4,67))
#im0.plot_row_profile(show_channels=[0])
#pr = im0.get_profile(axis=1,i_channel_group=0)
#print "RTN diff:",numpy.std(pr)/2**0.5
#print "RTN:",numpy.std(pr)

#pylab.plot(pr+700)
#pylab.plot(pr)
#pylab.show()


print("Computing RMS")

for raw in raw0:

    print(raw)
    im = Image.Image(raw)
    if bswap: im.column_swap()
    im.set_channel_groups(channel_groups)
    im.set_ROI((rows_roi-1,columns_roi-1))
    im.set_ROI(roi)
    #im.RTN_correction()
    
    for i_channel_group in range(num_channels):
        tmp_rms[i_channel_group] += (im.get_array(i_channel_group=i_channel_group)-Mean[i_channel_group])**2
        tmp_rms_row[i_channel_group] += (im.get_profile(axis=1,i_channel_group=i_channel_group)-Mean_row[i_channel_group])**2
        tmp_rms_column[i_channel_group] += (im.get_profile(axis=0,i_channel_group=i_channel_group)-Mean_column[i_channel_group])**2
        #print "mean",i_channel_group,Mean[i_channel_group]


RMS = (numpy.array(tmp_rms) / float(Nimages-1))**0.5
RMS_row = (numpy.array(tmp_rms_row) / float(Nimages-1))**0.5
RMS_column = (numpy.array(tmp_rms_column) / float(Nimages-1))**0.5

total_temporal_noise = RMS.mean(axis=1).mean(axis=1)
row_temporal_noise  = RMS_row.mean(axis=1)
column_temporal_noise = RMS_column.mean(axis=1)

print("Total temporal noise:", total_temporal_noise)
print("Row temporal noise:", row_temporal_noise)
print("Column temporal noise:", column_temporal_noise)

RMS_pixel = []

for i_channel_group in range(num_channels):

    RMS_row_expanded = numpy.hstack([numpy.reshape(RMS_row[i_channel_group],(RMS_row[i_channel_group].shape[0],1))]*RMS[i_channel_group].shape[1])
    RMS_column_expanded = numpy.vstack([numpy.reshape(RMS_column[i_channel_group],(1,RMS_column[i_channel_group].shape[0]))]*RMS[i_channel_group].shape[0])

    rms_pixel = RMS[i_channel_group]**2 - RMS_row_expanded**2 - RMS_column_expanded**2
    rms_pixel = numpy.where(rms_pixel<0,0,rms_pixel)
    rms_pixel = rms_pixel**0.5

    RMS_pixel.append(rms_pixel)

#    if i_channel_group==0:
    if 0:
        print('total',RMS[i_channel_group])
        print('row',RMS_row_expanded)
        print('rms_col',RMS_column[i_channel_group])
        #print 'col',RMS_column_expanded
        #print 'col2',numpy.vstack([numpy.reshape(RMS_column[i_channel_group],(1,RMS_column[i_channel_group].shape[0]))]*RMS[i_channel_group].shape[0])
        #print 'col3',[numpy.reshape(RMS_column[i_channel_group],(1,RMS_column[i_channel_group].shape[0]))]
        print('pix',RMS_pixel[i_channel_group])

RMS_pixel = numpy.array(RMS_pixel)

pixel_temporal_noise = RMS_pixel.mean(axis=1).mean(axis=1)
print("Pixel temporal noise:", pixel_temporal_noise)

#print 'pixel 0,0:'
#print RMS[0][0,0:10], RMS_row[0][0]
#print RMS[0][10,0:10], RMS_row[0][10]
#print RMS[0][100,0:10], RMS_row[0][100]
#print RMS[0][200,0:10], RMS_row[0][200]

#im0.set_channel_groups((1,4))

dir_ana = os.path.join(directory,'analysis_pixhist_'+suffix_analysis)
if not(os.path.isdir(dir_ana)):
    os.mkdir(dir_ana)

# write results into file:
f = open(os.path.join(dir_ana,'noise_results.txt'),'w')
f.write("Total temporal noise: %s\n"%(', '.join(str(v) for v in total_temporal_noise)))
f.write("Row temporal noise: %s\n"%(', '.join(str(v) for v in row_temporal_noise)))
f.write("Column temporal noise: %s\n"%(', '.join(str(v) for v in column_temporal_noise)))
f.write("Pixel temporal noise: %s\n"%(', '.join(str(v) for v in pixel_temporal_noise)))
f.close()

#PlotTools.plot_histogram(RMS,blog=True,bsave=False,xmin=None,xmax=None,xlabel='Total Temporal Noise [DN]',filename=os.path.join(directory,'hist_pixel_temporal_noise.png'))
#PlotTools.plot_histogram(numpy.array([RMS_pixel]),blog=False,bsave=False,xmin=0,xmax=20,xlabel='Pixel Temporal Noise [DN]')
#PlotTools.plot_histogram(numpy.array([RMS]),blog=False,bsave=False,xmin=0,xmax=20,xlabel='Total Temporal Noise [DN]')
#PlotTools.plot_histogram(numpy.array([RMS_row]),blog=False,bsave=False,xmin=0,xmax=20,xlabel='Row Temporal Noise [DN]')
#PlotTools.plot_histogram(numpy.array([RMS_column]),blog=False,bsave=False,xmin=0,xmax=5,xlabel='Column Temporal Noise [DN]')

#PlotTools.plot_histogram(numpy.array(RMS_pixel),blog=True,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise.png'))
PlotTools.plot_histogram(numpy.array(RMS_pixel),blog=True,xmin=5,xmax=15,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise.png'))
#PlotTools.plot_histogram(numpy.array(RMS_pixel),xmin=0,xmax=20,blog=True,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise.png'))
#PlotTools.plot_histogram(numpy.array(RMS_pixel),xmin=xmin,xmax=xmax,nbins=nbins,blog=True,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise.png'))
PlotTools.plot_histogram(numpy.array(RMS),nbins=nbins,blog=True,bsave=True,xlabel='Total Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_total_temporal_noise.png'))
PlotTools.plot_histogram(numpy.array(RMS_row),nbins=nbins,blog=True,bsave=True,xlabel='Row Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_row_temporal_noise.png'))
PlotTools.plot_histogram(numpy.array(RMS_column),nbins=nbins,blog=True,bsave=True,xlabel='Column Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_column_temporal_noise.png'))

#PlotTools.plot_histogram(numpy.array(RMS_pixel),nbins=nbins,blog=False,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise_linear.png'))
PlotTools.plot_histogram(numpy.array(RMS_pixel),nbins=nbins,blog=False,xmin=xmin,xmax=xmax,bsave=True,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_pixel_temporal_noise_linear.png'))
PlotTools.plot_histogram(numpy.array(RMS),nbins=nbins,blog=False,bsave=True,xlabel='Total Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_total_temporal_noise_linear.png'))
PlotTools.plot_histogram(numpy.array(RMS_row),nbins=nbins,blog=False,bsave=True,xlabel='Row Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_row_temporal_noise_linear.png'))
#PlotTools.plot_histogram(numpy.array(RMS_column),nbins=nbins,blog=False,xmin=0,xmax=3,bsave=True,xlabel='Column Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_column_temporal_noise_linear.png'))
PlotTools.plot_histogram(numpy.array(RMS_column),nbins=nbins,blog=False,bsave=True,xlabel='Column Temporal Noise [DN]',filename=os.path.join(dir_ana,'hist_column_temporal_noise_linear.png'))

#print RMS_pixel[0].shape
#print RMS_pixel[1].shape

rms_tot = RMS_pixel[0]
#print rms_tot.shape
rms_tot = numpy.hstack((rms_tot,RMS_pixel[1]))
rms_tot = numpy.hstack((rms_tot,RMS_pixel[2]))
rms_tot = numpy.hstack((rms_tot,RMS_pixel[3]))

print(rms_tot)
PlotTools.plot_image([rms_tot],nbins=nbins,blog=False,xmin=xmin,xmax=xmax,bsave=True,xlabel='',filename=os.path.join(dir_ana,'image_pixel_temporal_noise.png'))
#PlotTools.plot_image([rms_tot],nbins=nbins,blog=False,bsave=True,xlabel='',filename=os.path.join(dir_ana,'image_pixel_temporal_noise.png'))
#PlotTools.plot_image(numpy.array(RMS_pixel),nbins=nbins,blog=False,xmin=xmin,xmax=xmax,bsave=True,xlabel='',filename=os.path.join(dir_ana,'image_pixel_temporal_noise.png'))

indices = []
for i_channel_group in range(num_channels):
    indices.append(numpy.where((PTN_min<RMS_pixel[i_channel_group])*(RMS_pixel[i_channel_group]<PTN_max)))

pixel = [[[] for i in range(Npixels)] for j in range(num_channels)]
'''
for raw in raw0:

    print raw

    im = Image.Image(raw)
    if bswap: im.column_swap()
    im.set_channel_groups(channel_groups)
    im.set_ROI((rows_roi-1,columns_roi-1))
    im.set_ROI(roi)
    #im.get_array(i_channel_group=i_channel_group)

    for i_channel_group in range(num_channels):

        for k in range(Npixels):

            i = indices[i_channel_group][0][k]
            j = indices[i_channel_group][1][k]
            #pixel[k].append(im.get_array_value_inROI(i,j,i_channel_group=i_channel_group))
            pixel[i_channel_group][k].append(im.get_array(i_channel_group)[i,j])

dir_ana_pix = os.path.join(dir_ana,"hist_pix")
if not(os.path.isdir(dir_ana_pix)):
    os.mkdir(dir_ana_pix)

for i_channel_group in range(num_channels):
    for k in range(Npixels):
        print numpy.array(pixel[i_channel_group][k]).std()
        i = indices[i_channel_group][0][k]
        j = indices[i_channel_group][1][k]
        PlotTools.plot_histogram(numpy.array([pixel[i_channel_group][k]]),blog=True,bsave=True,xlabel='Pixel value [DN]',filename=os.path.join(dir_ana_pix,'hist_pixel_%i_%i_%i.png'%(i_channel_group,i,j)))
        PlotTools.plot_histogram(numpy.array([pixel[i_channel_group][k]]),blog=False,bsave=True,xlabel='Pixel value [DN]',filename=os.path.join(dir_ana_pix,'hist_pixel_linear_%i_%i_%i.png'%(i_channel_group,i,j)))

'''
import pickle
pickle.dump(RMS,open(os.path.join(dir_ana,'pickle_RMS.p'),'wb'))
pickle.dump(RMS_row,open(os.path.join(dir_ana,'pickle_RMS_row.p'),'wb'))
pickle.dump(RMS_column,open(os.path.join(dir_ana,'pickle_RMS_column.p'),'wb'))
pickle.dump(RMS_pixel,open(os.path.join(dir_ana,'pickle_RMS_pixel.p'),'wb'))

