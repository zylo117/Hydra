#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import copy
import numpy
import pylab

from . import Image
from . import PlotTools

class ImageArray(object):
    
    Nimages = 0
    
    def __init__(self, data_array, rows=3000, columns=4000, datatype='uint16',channel_groups=(1,1)):
        '''
        data_array: list of RAW files or list of Image objects
        '''

        self.Images = []

        self.channel_groups = channel_groups
        self.num_channel_groups = self.channel_groups[0]*self.channel_groups[1]

        if len(data_array)>0 and type(data_array[0])==str:
            self.load_RAWfiles(data_array,rows,columns,datatype,channel_groups=self.channel_groups)
        else:
            self.load_Images(data_array)

    def __getitem__(self, key):
        return self.Images[key]
        
    def info(self):
        print("Number of images: %i"%self.Nimages)
        #for image in self.Images:
        #    image.info()
    
    def load_RAWfiles(self, RAWfiles, rows, columns, datatype,channel_groups=1):
        for RAWfile in RAWfiles:
            self.Images.append(Image.Image(RAWfile,rows,columns,datatype,channel_groups=channel_groups))
        self.Nimages += len(RAWfiles)
        print('Loaded %i images in ImageArray object'%self.Nimages)

    def deepcopy(self):

        return copy.deepcopy(self)

    def load_Images(self, Images):
        for image in Images:
            self.Images.append(image)
        self.Nimages += len(Images)
        print('Loaded %i images in ImageArray object'%self.Nimages)
        
    def set_ROI(self, roi):
        print("ImageArray: ROI set at",roi)
        for image in self.Images:
            image.set_ROI(roi)
        
    def set_center_ROI(self, roi_dim):
        # roi_dim is a tuple of dimension 2
        for image in self.Images:
            image.set_center_ROI(roi_dim)

    def subtract(self, ref_image):
        for image in self.Images:
            image.subtract(ref_image)
            
    def power(self, pow):
        for image in self.Images:
            image.power(pow)

    def sum(self):
        '''
        Returns image sum (sum performed at a pixel by pixel level)
        '''

        if self.Nimages==0:
            return None
        elif self.Nimages==1:
            return copy.deepcopy(self.Images[0])
        else:
            sum_image = self.Images[0].zerocopy() # copy with array zero initialized
            for image in self.Images:
                sum_image.array += image.array
            return sum_image


    def average(self):
        '''
        Returns average image (average performed at a pixel by pixel level)
        '''

        if self.Nimages==0:
            return None
        else:
            avg_image = self.sum()
            avg_image.array = avg_image.array / self.Nimages
            return avg_image


    def column_swap(self):
        for image in self.Images:
            image.column_swap()

    def combine(self,shape):
        '''
        Combine all images in a single image
        '''

        for j in range(shape[0]):

            himage = copy.deepcopy(self.Images[j*shape[1]])

            for i in range(1,shape[1]):
                himage.hstack(self.Images[j*shape[1]+i])

            if j==0:
                combined_image = copy.deepcopy(himage)
            else:
                combined_image.vstack(himage)
                
        return combined_image


    def FPN_correction(self, bswap=True, rowstart=0, rowstop=64, target=None):

        for image in self.Images:
            image.FPN_correction(bswap=bswap, rowstart=rowstart, rowstop=rowstop, target=target)


    def apply_FPN_correction(self, fpn_correction_factors, bswap=True):

        for image in self.Images:
            image.apply_FPN_correction(fpn_correction_factors, bswap=bswap)


    def RTN_correction(self, bswap=True, colstart=4, colstop=67, target=None, boddeven=False, bsave=False, filename=None):

        for image in self.Images:
            print(bswap)
            image.RTN_correction(bswap=bswap, colstart=colstart, colstop=colstop, target=target, boddeven=boddeven, bsave=bsave, filename=filename)


    def apply_RTN_correction(self,rtn_correction_factors,bswap=True):

        for image in self.Images:
            image.apply_RTN_correction(rtn_correction_factors, bswap=bswap)


    def get_profiles(self,axis=0,i_channel_group=None):

        profiles = []
        for im in self.Images:
            profiles.append(im.get_profile(axis=axis,i_channel_group=i_channel_group))

        return profiles


    def get_noise(self, bsave=False, directory=None, bfullresolution=False):

        # Compute FPN noise
        
        total_fpn_noise = []
        row_fpn_noise = []
        column_fpn_noise = []
        pixel_fpn_noise = []

        Image_avg = self.average()
        row_profile_avg = [] # split in channels
        column_profile_avg = [] # split in channels

        # Average row/col profiles
        for i_channel_group in range(self.num_channel_groups):

            arr = Image_avg.get_array(i_channel_group)

            arr_row = numpy.mean(arr,axis=1)
            row_profile_avg.append(arr_row)
            
            arr_col = numpy.mean(arr,axis=0)
            column_profile_avg.append(arr_col)
            
        row_profile_avg = numpy.array(row_profile_avg)
        column_profile_avg = numpy.array(column_profile_avg)
        
        # Compute temporal noise:
        
        row_temporal_noise = []
        column_temporal_noise = []
        pixel_temporal_noise = []
        total_temporal_noise = []

        # Compute pixel temporal noise:
        Image_copy = self.deepcopy()
        Image_copy.subtract(Image_avg)
        Image_copy.power(2)
        im = Image_copy.sum()
        im.multiply(1/float(self.Nimages-1))
        im.power(0.5)
        #total_temporal_noise = im.get_mean_channel_groups()

        # Compute Temporal Noise:
        pixel_temporal_noises = []
        row_temporal_noises = []
        column_temporal_noises = []
        total_temporal_noises = []
        for i_channel_group in range(self.num_channel_groups):

            total_temporal_noises.append(im.get_array(i_channel_group))
            total_temporal_noise.append(numpy.mean(total_temporal_noises[i_channel_group]))

            row_profiles = numpy.array(self.get_profiles(axis=1,i_channel_group=i_channel_group))
            row_temporal_noises.append((numpy.sum((row_profiles - row_profile_avg[i_channel_group])**2, axis=0) / float(self.Nimages-1))**0.5)
            row_temporal_noise.append(numpy.mean(row_temporal_noises[i_channel_group]))

            column_profiles = numpy.array(self.get_profiles(axis=0,i_channel_group=i_channel_group))
            column_temporal_noises.append((numpy.sum((column_profiles - column_profile_avg[i_channel_group])**2, axis=0) / float(self.Nimages-1))**0.5)
            column_temporal_noise.append(numpy.mean(column_temporal_noises[i_channel_group]))

            row_temporal_noises_expanded = numpy.hstack([numpy.reshape(row_temporal_noises[i_channel_group],(row_temporal_noises[i_channel_group].shape[0],1))]*(self.Images[0].ROI.Ncolumns/self.channel_groups[1]))
            column_temporal_noises_expanded = numpy.vstack([numpy.reshape(column_temporal_noises[i_channel_group],(1,column_temporal_noises[i_channel_group].shape[0]))]*(self.Images[0].ROI.Nrows/self.channel_groups[0]))
            #pixel_temporal_noises.append((total_temporal_noises[i_channel_group]**2 - row_temporal_noises_expanded**2 - column_temporal_noises_expanded**2)**0.5)

            #pixel_temporal_noises.append((total_temporal_noises[i_channel_group]**2 - row_temporal_noises_expanded**2 - column_temporal_noises_expanded**2)**0.5)
            temp = (total_temporal_noises[i_channel_group]**2 - row_temporal_noises_expanded**2 - column_temporal_noises_expanded**2)
            pixel_temporal_noises.append(numpy.where(temp<0,0,temp)**0.5)
            pixel_temporal_noise.append(numpy.mean(pixel_temporal_noises[i_channel_group]))


        # Compute Fixed Pattern Noise
        for i_channel_group in range(self.num_channel_groups):

            arr = Image_avg.get_array(i_channel_group)
            # correcting for left over temporal noise
            total_fpn_noise.append(numpy.sqrt(numpy.std(arr)**2-total_temporal_noise[i_channel_group]**2/self.Nimages))
            row_fpn_noise.append(numpy.sqrt(numpy.std(row_profile_avg[i_channel_group])**2-row_temporal_noise[i_channel_group]**2/self.Nimages))
            column_fpn_noise.append(numpy.sqrt(numpy.std(column_profile_avg[i_channel_group])**2-column_temporal_noise[i_channel_group]**2/self.Nimages))
            pixel_fpn_noise.append((total_fpn_noise[-1]**2-numpy.nan_to_num(row_fpn_noise[-1])**2-numpy.nan_to_num(column_fpn_noise[-1])**2)**0.5)
            # without corrections
            #total_fpn_noise.append(numpy.std(arr))
            #row_fpn_noise.append(numpy.std(row_profile_avg[i_channel_group]))            
            #column_fpn_noise.append(numpy.std(column_profile_avg[i_channel_group]))
            #pixel_fpn_noise.append((total_fpn_noise[-1]**2-row_fpn_noise[-1]**2-column_fpn_noise[-1]**2)**0.5)


        if bsave:
            minval,maxval = 0,20
            #minval,maxval = None, None
            #im.plot_image(bsave=True,minval=minval,maxval=maxval,filename=os.path.join(directory,'image_total_temporal_noise.png'))
            im.plot_histogram(blog=False,bsave=True,xmin=minval,xmax=maxval,xlabel='Total Temporal Noise [DN]',filename=os.path.join(directory,'hist_total_temporal_noise.png'))
            PlotTools.plot_histogram(pixel_temporal_noises,blog=True,bsave=True,xmin=minval,xmax=maxval,xlabel='Pixel Temporal Noise [DN]',filename=os.path.join(directory,'hist_pixel_temporal_noise.png'))

        # Plot individual pixel value histogram:
        def func():
            dir = os.path.join(directory,"pixel_hist")
            if not(os.path.isdir(dir)): os.mkdir(dir)
            count = 0
#            for i in range(1000,1500):
#                for j in range(2000,3000):
            for i in range(pixel_temporal_noises[0].shape[0]):
                for j in range(pixel_temporal_noises[0].shape[1]):
                    val = pixel_temporal_noises[0][i,j]
                    if val>10:
                        count+=1
                        print(count,i,j)
                        self.plot_pixel_histogram(i,j,blog=False,bsave=True,filename=os.path.join(directory,'pixel_hist','hist_pixel_%i_%i.png'%(i,j)))
                        if count>10: return 
        #func()

        return total_fpn_noise,row_fpn_noise,column_fpn_noise,pixel_fpn_noise, total_temporal_noise,row_temporal_noise,column_temporal_noise,pixel_temporal_noise


    def plot_pixel_histogram(self, i, j, xmin=None, xmax=None, nbins=100, ylim=None, blog=False, figsize=9, bsave=False, filename="fig_hist.png", title='', xlabel="DN", ylabel="# events", color='b', legend_label=None, legend_location='upper center'):

        fig = pylab.figure(2,(16/9.*figsize,figsize))

        ax = fig.add_subplot(1,1,1)

        pixel_values = []
        for im in self.Images:
#            pixel_values.append(im.get_array_value(i,j))
            pixel_values.append(im.get_array_value_inROI(i,j,i_channel_group=0))
        pixel_values = numpy.array(pixel_values)

        xmin,xmax = PlotTools.set_minmax(pixel_values,minval=xmin,maxval=xmax)
        xmin = xmin - 0.05*(xmax-xmin)
        xmax = xmax + 0.05*(xmax-xmin)

        hist, bins = numpy.histogram(pixel_values,bins=nbins,range=(xmin,xmax))
        width = bins[1] - bins[0]
        center = (bins[:-1] + bins[1:]) / 2
            
        if legend_label==None:
            pylab.bar(center, hist, align='center', width=width, log=blog, color=color)
        else:
            pylab.bar(center, hist, align='center', width=width, log=blog, color=color,label=legend_label)
        #pylab.plot(center, hist,color=color)

        legend = ax.legend(loc=legend_location, shadow=True)

        pylab.xlim([xmin,xmax])

        if ylim!=None:
            pylab.ylim([ylim[0],ylim[1]])
        elif ylim==None and blog:
            (ymin,ymax) = pylab.ylim()
            pylab.ylim([0.1*ymin,ymax])

        pylab.title(title)
        pylab.grid(True)

        if bsave:
            print("Saving histogram: %s"%filename)
            pylab.savefig(filename)
            pylab.clf()
            pylab.close()
        else:           
            pylab.show()
