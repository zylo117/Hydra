import glob

file_darks = 'Z:\\PROGRAMS\\PyVisage\\test\\Intro_tutorial\\Q8A636w14#25-D_greenL\\Dark\\DarkImage_*.raw'

raw_images = glob.glob(file_darks)

import ImageArray

im_arr = ImageArray.ImageArray(raw_images[:2])

im_avg = im_arr.average()

#im_avg.plot_image()

import Image

im_ref = Image.Image('Q8A636w14#25-D_greenL\\Dark\\DarkImage_5.raw')

im_arr.subtract(im_ref)

#im_arr[1].plot_image()
im_arr[1].plot_histogram(xmin=-50,xmax=+50,bsave=True,filename="Hist_dark_difference.png")

print("Read Noise = %.1f DN"%(im_arr.Images[1].get_rms()/2**0.5))
