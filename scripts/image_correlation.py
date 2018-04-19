import pylab
import glob
from pyvisage import Image
from pyvisage import ImageArray

channel_groups = (1,4)

roi = None
#roi = (0,2999,0,1600)
#roi = (0,2999,400,800)
#roi = (0,2999,2200,2600)

raw0 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#55E_baseline\\RawImages\\image_0.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_1.raw")
#raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140909\\Q8A670w10#54E_baseline\\RawImages\\image_0.raw")
raw1 = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Data\\20140905\\Q8A670w10#54E_crushedIsource_bypass2ndLevelMUX\\RawImages\\image_0.raw")

im0 = ImageArray.ImageArray(raw0).average()
im1 = ImageArray.ImageArray(raw1).average()

if roi !=None:
    im0.set_ROI(roi)
    im1.set_ROI(roi)

#im0.set_ROI(1400,1599,44,299) # CDS amp #2
#im1.set_ROI(1300,1699,144,1299) # in region where bot vcmi switches are off
im0.set_channel_groups(channel_groups)
im1.set_channel_groups(channel_groups)

#im1.plot_image(bstack=True)
#im1.plot_image()

#im1.plot_histogram(xmin=0,xmax=4096,image2=im_prefib,blog=True)

im0.plot_profile()
im1.plot_profile()

#r_pearson = im1.correlate(im0,bplot=True,bPearson=False)
#print "Pearson's coeff.:",r_pearson
#im1.autocorrelate(bplot=True)
