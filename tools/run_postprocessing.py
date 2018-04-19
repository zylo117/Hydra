import pyviz.Image as Image

channel_groups = (1,8)

dir = ''
filename1 = 'image_grounded_1.raw'

im = Image.Image('image_grounded_1.raw',rows=3000,columns=4000)

im.set_channel_groups(channel_groups)

Img = []
for i in range(im.num_channel_groups):
    Img.append(Image.Image(im.get_array(i_channel_group=i)))

    Img[i].save2raw(filename='image_group%i.raw'%i)
