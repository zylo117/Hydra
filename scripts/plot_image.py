import os
import pylab
import glob
from pyvisage import Image
from pyvisage import ImageArray

#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140930\\Q8A670w07#75B_LNtesting\\1hardonly_vpix2.2V"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140930\\Q8A670w07#75B_LNtesting\\1hardonly_vpix2.2V_Adie"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140930\\Q8A670w07#75B_LNtesting\\3softonly_vpix2.8V"
#directory = "F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140930\\Q8A670w07#75B_LNtesting\\3softonly_vpix2.8V_Adie"
directory_list = glob.glob("F:\\INVISAGE\\PC5\\Read_Noise\\Pixel_Temporal\\Data\\20140930\\Q8A670w07#75B_LNtesting\\*")

for directory in directory_list:

    file_bright = "image_bright_0.raw"
    file_dark = "image_dark_0.raw"

    file_bright = os.path.join(directory,file_bright)
    file_dark = os.path.join(directory,file_dark)

    raw_bright = glob.glob(file_bright)
    raw_dark = glob.glob(file_dark)

    im_bright = ImageArray.ImageArray(raw_bright).average()
    im_dark = ImageArray.ImageArray(raw_dark).average()

    im_bright.subtract(im_dark)

    #im0.set_ROI(1400,1599,44,299) # CDS amp #2
    #im1.set_ROI(1400,1599,44,299) # CDS amp #2
    #im1.set_ROI(1300,1699,144,1299) # in region where bot vcmi switches are off
    #im0.set_ROI((999,999))
    #im1.set_ROI((999,999))

    #im0.set_channel_groups((1,4))
    #im1.set_channel_groups((1,4))

    #im1.plot_image(bstack=True)
    filename = os.path.join(directory,"image_scalezoomed.png")
    #im_bright.plot_image(minval=0,maxval=4096,colorscale='gray',dpi=200,bsave=True,filename=filename, bcolorbar=False)
    im_bright.plot_image(minval=0,maxval=3000,colorscale='gray',dpi=200,bsave=True,filename=filename, bcolorbar=False)

    #im1.plot_histogram(xmin=0,xmax=4096,image2=im0,blog=True)
    #im1.plot_histogram(legend_label='AVDD28 = 2.0V',image2=im0,legend_label2='AVDD28 = 2.8V')
    #im1.plot_histogram(show_channels=[0,2],xmin=0,xmax=4096,nbins=200,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')
    #im1.plot_histogram(show_channels=[0,2],xmin=0,xmax=4096,nbins=200,legend_label=label1,image2=im0,legend_label2=label0,legend_location='upper right')

    #im1.plot_profile(xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='lower left')
    #im1.plot_profile(show_channels=[0,2],xlabel='Column',color='r',legend_label=label1,image2=im0,color2='b',legend_label2=label0,legend_location='upper center')
    #im1.plot_profile(legend_label='VANA28 = 2.8V',image2=im0,legend_label2='VANA28 = 2.0V')
    #im1.plot_profile(legend_label='pre-FIB',image2=im0,legend_label2='post-FIB')
