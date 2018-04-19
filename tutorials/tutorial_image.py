#raw_bright = 'Q8A643w20#44R_Red//Bright_-0.8//image_0.raw'
#raw_dark = 'Q8A643w20#44R_Red//Dark_-0.8//image_0.raw'
raw_bright = 'Q8A625w04#63R_Green//Dark//DarkImage_0.raw'
raw_dark = 'Q8A625w04#63R_Green//Dark//DarkImage_1.raw'

import Image

im_bright = Image.Image(raw_bright)
im_dark = Image.Image(raw_dark)

im_bright.info()

#im_bright.plot_image()

# column swapping for odd rows
#im_bright.column_swap()

# Dark subtraction
im_bright.subtract(im_dark)

# ROI selection (note: can also be done when instantiating the Image object)
#im_bright.set_ROI(2000,2300,600,1000) # defect
#im_bright.set_ROI(2000,2300,1000,1300) # bayer
#im_bright.set_ROI(0,3000,0,150)
#im_bright.set_ROI(0,180,1000,1500) # reference rows

# Channel grouping
im_bright.set_channel_groups((2,2))

# RTN correction
im_bright.RTN_correction() # default columns used: 4-67

# Plot 2D image
im_bright.plot_image()
#im_bright.plot_image(bstack=True)

# Plot histogram
#im_bright.plot_histogram()
im_bright.plot_histogram(nbins='fullresolution')

# Get 
#print im_bright.get_median_channel_groups()
print(im_bright.get_rms_channel_groups())
