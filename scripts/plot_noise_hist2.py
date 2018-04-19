import numpy
import pylab
import glob, os
from pyvisage import Image

pylab.figure(2,(16,9))

bana1 = True
badc= False
bhist = False

color = ['b','g','r','c','m','y','k','0.75']

directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#53R1"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLadc0xB"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_cdsStatic_ISLacd0xB_activePixel"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_cdsStatic_ISLacd0xB_quietPixel2"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLacd0xB_single"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS2_BOTmTOP"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLacd0xB_double"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#26R1\\RawImages"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160314\\792w12#52R1\\RawImages_singleBS_gain1_bis2"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160321\\792w12#51R1\\RawImages"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160321\\792w12#83R1\\RawImages"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160321\\792w12#23R1\\RawImages"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160314\\792w12#83R1\\RawImages_singleBS_gain1_bis"
#"F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_hard_scan_20160127_140930"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160419\\811w24#26R1\\RawImages"

#file = os.path.join(directory,"image_0*.raw")
#file = os.path.join(directory,"image_BB_0*.raw")
#file = os.path.join(directory,"image_imaging_BB_gain1_0*.raw")
file = os.path.join(directory,"image_BB_gain1_0*.raw")
#file = os.path.join(directory,"image_imaging_BB_0*.raw")
#file = os.path.join(directory,"image_imagingFA_BB_0*.raw")
#file = os.path.join(directory,"image_BF_gain1_0*.raw")
#file = os.path.join(directory,"image_BB_gain16_0*.raw")
print(file)

#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_v2\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_FA\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_FA_ISLadcB\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_cdsStatic_ISLacd0xB\\image_*.raw"))
raw0 = glob.glob(file)
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_12M\\image_*.raw"))
print('raw0:',raw0)

suffix_analysis = 'v0'

num_adc = 8

Nimages = len(raw0)
print("Number of images found:",Nimages)

#rows = 3000
#columns = 4000
roi = None
#rows = 3136
#columns = 4352
rows = 3000
columns = 4352
#roi = (68,3135,0,3999)

col_chan = 16

im0 = Image.Image(raw0[1],rows=rows,columns=columns)
im1 = Image.Image(raw0[2],rows=rows,columns=columns)
im0.set_ROI(roi)
im1.set_ROI(roi)

im1.subtract(im0)

arr = im1.get_array()

arr_split = arr[:,0::col_chan]
for i in range(1,col_chan):
    arr_split = numpy.hstack((arr_split,arr[:,i::col_chan]))

ptn_col = numpy.std(arr,axis=0)/2**0.5
ptn_col_split = numpy.std(arr_split,axis=0)/2**0.5

import matplotlib as mpl
arr0 = im0.get_array()
mean = numpy.mean(arr0,axis=0)

if bana1:
    if badc:

        for i in range(num_adc):
            #if not(bhist): pylab.subplot(2,4,i+1)
            pylab.subplot(2,4,i+1)
            mean_p = numpy.concatenate((mean[i*2:len(mean):num_adc*2],mean[i*2+1:len(mean):num_adc*2]))
            ptn_col_p = numpy.concatenate((ptn_col[i*2:len(mean):num_adc*2],ptn_col[i*2+1:len(mean):num_adc*2]))
            if bhist:
                hist, bins = numpy.histogram(mean_p,bins=100)
                width = bins[1] - bins[0]
                center = (bins[:-1] + bins[1:]) / 2
                pylab.bar(center, hist, align='center', width=width, log=True, edgecolor=color[i],fill=False)
                #pylab.bar(center, hist, align='center', width=width, log=False, edgecolor=color[i],fill=False)
                #pylab.xlim([101,121])
                pylab.ylim([0.5,70])
                pylab.title('ADC %i'%(i+1))
                pylab.xlabel('Column average [DN]')
            else:
                pylab.hist2d(mean_p,ptn_col_p, bins=100,norm=mpl.colors.LogNorm(),range=[[101,121],[0,2.5]])
                pylab.xlim([101,121])
                pylab.ylim([0,2.5])
                pylab.title('ADC %i'%(i+1))
                pylab.xlabel('Column average [DN]')
                pylab.ylabel('Column PTN [DN]')

        pylab.show()

    else: 

        #pylab.hist2d(mean,ptn_col,bins=200)#,range=[[0,150],[-150,150]])
        #pylab.hist2d(mean,ptn_col, bins=200,norm=mpl.colors.LogNorm(), cmap=mpl.cm.gray)
        pylab.hist2d(mean,ptn_col, bins=200,norm=mpl.colors.LogNorm())
        #pylab.hist2d(mean,ptn_col, bins=200)

        pylab.xlabel('Column average [DN]')
        pylab.ylabel('Column PTN [DN]')
        pylab.grid(True)
        pylab.show()

        pylab.show()

else:

    ptn_col_7even = ptn_col[6*2:len(mean):num_adc*2]
    ptn_col_7odd = ptn_col[6*2+1:len(mean):num_adc*2]
    ptn_col_7 = numpy.concatenate((ptn_col_7even,ptn_col_7odd))
    for i in range(num_adc):

        meanX_even = mean[i*2:len(mean):num_adc*2]
        meanX_odd = mean[i*2+1:len(mean):num_adc*2]
        meanX = numpy.concatenate((meanX_even,meanX_odd))

        mean7_even = mean[6*2:len(mean):num_adc*2]
        mean7_odd = mean[6*2+1:len(mean):num_adc*2]
        mean7 = numpy.concatenate((mean7_even,mean7_odd))

        meanXm7_even = meanX_even - mean7_even
        meanXm7_odd = meanX_odd - mean7_odd
        meanXm7 = numpy.concatenate((meanXm7_even,meanXm7_odd))

        pylab.subplot(2,4,i+1)
        #pylab.hist2d(meanXm7,ptn_col_7, bins=100,norm=mpl.colors.LogNorm())
        pylab.hist2d(meanX,mean7, bins=60,norm=mpl.colors.LogNorm())
    
        #pylab.xlabel('Mean adc%i-adc7 [DN]'%(i+1))
        #pylab.ylabel('ADC7 PTN [DN]')
        pylab.xlabel('Mean adc%i [DN]'%(i+1))
        pylab.ylabel('Mean adc7 [DN]')
        pylab.grid(True)
    pylab.show()
