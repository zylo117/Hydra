import os
import numpy
import pylab
from pyvisage import Image

bsave = True
bdark = False

figsize=9
fig = pylab.figure(2,(16/9.*figsize,figsize))

suffix = 'v0'

raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_CDSinject_16.8MHz_0.5V_corr.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_CDSinject_30MHz_0.5V_corr.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_CDSinject_34.8MHz_0.5V_corr.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_VANA1.8V.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_PWRMOD.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_lookahead4.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_pipeline.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_pipeline_powerMOD.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\Q8A752W03#31-A1\\Light\\Light_0000.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_218uA.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_62uA.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_v2.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_mirror.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_34.8MHz_normal.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_16.8MHz_VANA1.8V.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\75A1\\image_16.8MHz_normal.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\56A3\\image_CDSinject_16.8MHz_0.5V_corr.raw"

raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_normal.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_v2_normal.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_v2_pddelay3cc.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_v2_VANA28_3.2V.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150804\\rto2\\Image_lookahead4_capOFF_0000.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_125uA.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_218uA.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_stage1_218uA.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_stage1_218uA_PWRAN1_1.8V.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_97.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_98_skew.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\75A1\\image_34.8MHz_stage1_218uA_PWRAN234_3.2V.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_delay3cc.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150730\\75A1\\image_34.8MHz_5CDS.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\65A1\\image_34.8MHz_65A1.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\65A1\\image_34.8MHz_65A1_lookahead32.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_34.8MHz_64A2_lookahead8.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150810\\image_58A3.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\65A1\\image_65A1_postFIB_lookahead0.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_64A2_postFIB_lookahead64.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_64A2_postFIB_lookahead64_40MHz_pddelay0.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_64A2_postFIB_lookahead64_test4_6dB.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_64A2_postFIB_lookahead64_24MHz.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150805\\64A2\\image_64A2_postFIB_lookahead64_gain12dB.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150810\\Image_58A3_capON_0000.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150821\\75A1\\image_75A1_24MHz_0dB.raw"
#raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150821\\64A2\\image_64A2_35MHz_12dB_skew91.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150821\\64A2\\image_64A2_35MHz_0dB_skew_bot95.raw"
raw0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150821\\64A2\\image_64A2_20MHz_12dB_skew95.raw"

if bdark: dark0 = "F:\\INVISAGE\\PC6\\Column_response_loss\\Data\\20150728\\Q8A752W03#31-A1\\Dark\\Dark_0000.raw"

rows = 3128
columns = 4352
#rows = 3128
#columns = 768
#columns = 1280

num_channels = 4
num_columns = 64
num_cds = 16 #1st CDS skipped

im0 = Image.Image(raw0, rows=rows, columns=columns)
if bdark: 
    dark0 = Image.Image(dark0, rows=rows, columns=columns)
    im0.subtract(dark0)

im0.set_channel_groups((1,num_channels))

R_cds = numpy.zeros((num_channels,num_cds))
R_col = numpy.zeros((num_channels,num_columns))
gain_col = numpy.zeros((num_channels,num_columns))

for i_chan in range(num_channels): 
#for i_chan in range(1): 

    profile_ch = im0.get_profile(axis=0, i_channel_group=i_chan)
    #profile_ch = profile_ch[num_columns:]
    #profile_ch = profile_ch[num_columns:-num_columns]
    profile_ch = profile_ch[num_columns:-num_columns]
    #profile_ch = profile_ch[15*num_columns:(15+1)*num_columns]
    #pylab.plot(range(num_columns*num_cds),profile_ch)

    for i_cds in range(num_cds):
        profile_ch_cds = profile_ch[i_cds*num_columns:(i_cds+1)*num_columns]
        R_cds[i_chan,i_cds] = numpy.average(profile_ch_cds)
        #R_cds[i_chan,i_cds] = numpy.median(profile_ch_cds)
        #print profile_ch_cds
        #print numpy.average(profile_ch_cds)

    for i_col in range(num_columns):
        profile_ch_col = profile_ch[i_col::num_columns]
        R_col[i_chan,i_col] = numpy.average(profile_ch_col)
        #R_col[i_chan,i_col] = numpy.median(profile_ch_col)

#print R_cds
#pylab.show()

#print R_col.shape
#print R_col[:,int(num_columns/2.)].shape
#print numpy.reshape(R_col[:,int(num_columns/2.)],(4,1)).shape
#gain_col = R_col/R_col[:,int(num_columns/2.)][:,None]
gain_col = R_col/numpy.average(R_col[:,20:40],axis=1)[:,None]

#im0_ch = Image.Image(arr_ch,rows=rows,columns=int(columns/num_channels))
#im0_ch.set_channel_groups((1,num_columns))

# Gain
fig = pylab.figure(2,(16,9))
ax = fig.add_subplot(1,1,1)
for i_chan in range(num_channels):
    pylab.plot(list(range(num_columns)),gain_col[i_chan],label='%i'%i_chan)
pylab.xlabel('Column')
pylab.ylabel('Relative Gain')
pylab.xlim([-1,num_columns+1])
#pylab.ylim([0.94,1.02])
pylab.ylim([0.95,1.02])
#pylab.ylim([0.95,1.1])
pylab.ylim([0.90,1.03])
pylab.grid(True)
legend = ax.legend(loc='lower center', shadow=True)
if bsave:
    filename = os.path.join(os.path.dirname(raw0),'plots','gain',os.path.splitext(os.path.basename(raw0))[0]+'_gain_%s.png'%suffix)
    pylab.savefig(filename)
    pylab.clf()
    pylab.close()
else:
    pylab.show()

# Response
for i_chan in range(num_channels):
    pylab.plot(list(range(num_columns)),R_col[i_chan])
pylab.xlabel('Column')
pylab.ylabel('Response')
pylab.xlim([-1,num_columns+1])
#pylab.ylim([1850,2040])
pylab.grid(True)
if bsave:
    filename = os.path.join(os.path.dirname(raw0),'plots','response',os.path.splitext(os.path.basename(raw0))[0]+'_response_%s.png'%suffix)
    pylab.savefig(filename)
    pylab.clf()
    pylab.close()
else:
    pylab.show()

# CDS profile
for i_chan in range(num_channels):
    pylab.plot(list(range(num_cds)),R_cds[i_chan])
pylab.xlabel('CDS unit')
pylab.ylabel('Response [DN]')
pylab.grid(True)
if bsave:
    filename = os.path.join(os.path.dirname(raw0),'plots','cds',os.path.splitext(os.path.basename(raw0))[0]+'_cds_%s.png'%suffix)
    pylab.savefig(filename)
    pylab.clf()
    pylab.close()
else:
    pylab.show()
