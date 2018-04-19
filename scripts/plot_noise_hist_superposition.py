import numpy
import pylab
import glob, os
import PlotTools
from pyvisage import Image

pylab.figure(2,(16,9))
PlotTools.set_figure_font()

mycolor=['r','b']

directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#53R1"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLadc0xB"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_cdsStatic_ISLacd0xB_activePixel"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_cdsStatic_ISLacd0xB_quietPixel2"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLacd0xB_single"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS2_BOTmTOP"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS2_singleCDSsweep"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS_ISLacd0xB_double"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#83R1\\RawImages_BS"
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160309\\792w12#26R1"
#"F:\\INVISAGE\\Q13S\\Timing_Optimization\\Data\\20160127\\790w08#35R1_hard_scan_20160127_140930"
directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160419"

#""
#directory = "F:\\INVISAGE\\Q13S\\Column_issues\\Data\\20160419\\792w15#52R1\\RawImages"

#file = os.path.join(directory,"image_*.raw")
#file0 = os.path.join(directory,"image_vCDS0x3A*.raw")
#file1 = os.path.join(directory,"image_vCDS0x5A*.raw")
file0 = os.path.join(directory,"792w15#52R1\\RawImages\\image_imaging_BB_gain1_*.raw")
file1 = os.path.join(directory,"811w24#45R1\\RawImages\\image_imaging_BB_gain1_*.raw")
print(file0)
print(file1)
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_v2\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_FA\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_FA_ISLadcB\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages\\image_*.raw"))
#raw0 = glob.glob(os.path.join(directory,"RawImages_cdsStatic_ISLacd0xB\\image_*.raw"))
raw0 = glob.glob(file0)
raw1 = glob.glob(file1)
#raw0 = glob.glob(os.path.join(directory,"RawImages_gain1_12M\\image_*.raw"))
print('raw0:',raw0)
print('raw0:',raw1)

Nimages0 = len(raw0)
Nimages1 = len(raw1)
print("Number of images0 found:",Nimages0)
print("Number of images1 found:",Nimages1)

#rows = 3000
#columns = 4000
roi = None
#rows = 3136
#columns = 4352
rows = 3000
columns = 4352
#roi = (68,3135,0,3999)

col_chan = 16

n_adc =6
col_start = n_adc * columns/8
col_stop = col_start + columns/8


PTNtoplot = []

for raw in [raw0,raw1]:
    im0 = Image.Image(raw[1],rows=rows,columns=columns)
    im1 = Image.Image(raw[2],rows=rows,columns=columns)
    im0.set_ROI(roi)
    im1.set_ROI(roi)

    im1.subtract(im0)

    arr = im1.get_array()

    # to use to split adc:
    #arr = arr[:,col_start:col_stop]
    arr = arr[:,0:4178]

    arr_split = arr[:,0::col_chan]
    for i in range(1,col_chan):
        arr_split = numpy.hstack((arr_split,arr[:,i::col_chan]))

    ptn_col = numpy.std(arr,axis=0)/2**0.5
    ptn_col_split = numpy.std(arr_split,axis=0)/2**0.5

    #PTNtoplot.append(ptn_col)
    PTNtoplot.append(ptn_col_split)

    
#pylab.plot(range(len(ptn_col_split)),ptn_col_split)
#pylab.show()
#for ptntoplot in PTNtoplot:
for i in range(len(PTNtoplot)):
    pylab.plot(list(range(len(PTNtoplot[i]))),PTNtoplot[i],color=mycolor[i],linewidth=2)
#pylab.show()

pylab.xlabel('Column')
pylab.ylabel('Column PTN [DN]')

pylab.grid(True)
pylab.show()
'''
pylab.savefig(os.path.join(directory,"ptn_split.png"))
pylab.clf()
pylab.close()
'''
