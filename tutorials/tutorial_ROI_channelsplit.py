import Image

raw_bright = 'Q8A643w20#44R_Red//Bright_-0.8//image_0.raw'
raw_dark = 'Q8A643w20#44R_Red//Dark_-0.8//image_0.raw'

im_bright = Image.Image(raw_bright)
im_dark = Image.Image(raw_dark)

# Dark subtraction
im_bright.subtract(im_dark)

# Channel grouping
im_bright.set_channel_groups((2,2))

# Set ROI in Bayer region
im_bright.set_ROI(2000,2300,1000,1300) # bayer

im_bright.plot_image(bstack=True,bsave=True,filename='image_darksubtracted_roi_channelsplit.png')
im_bright.plot_histogram(bsave=True,filename='hist_darksubtracted_roi_channelsplit.png')

Median = im_bright.get_median_channel_groups()

print("horizontal xtalk = %.1f%%"%(Median[1]/Median[0]*100))
print("vertical xtalk = %.1f%%"%(Median[2]/Median[0]*100))
