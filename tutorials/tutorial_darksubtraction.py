import Image

raw_bright = 'Q8A643w20#44R_Red//Bright_-0.8//image_0.raw'
raw_dark = 'Q8A643w20#44R_Red//Dark_-0.8//image_0.raw'

im_bright = Image.Image(raw_bright)
im_dark = Image.Image(raw_dark)

im_bright.info()

# Dark subtraction
im_bright.subtract(im_dark)


im_bright.plot_image(bsave=True,filename='image_darksubtracted.png')
im_bright.plot_histogram(bsave=True,filename='hist_darksubtracted.png')
