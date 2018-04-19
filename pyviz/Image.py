#! /usr/bin/env python

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os
import numpy
import matplotlib
import pylab

from . import PlotTools

def gaus(x,norm,mean,sigma):
    return norm*numpy.exp(-(x-mean)**2/(2*sigma**2))

class ROI(object):
    ''' Class to define a rectangular Region Of Interest in image.
        Defined as:
        (rowstart,colstart) (rowstart,colstop)
        (rowstop,colstart)  (rowstop,colstop)
    '''

    def __init__(self, rowstart, rowstop, colstart, colstop):
        self.rowstart = rowstart
        self.rowstop = rowstop
        self.colstart = colstart
        self.colstop = colstop

        self.Nrows = rowstop - rowstart + 1
        self.Ncolumns = colstop - colstart + 1

    def info(self):
        print("width x height = %i x %i"%(self.rowstop-self.rowstart,self.colstop-self.colstart))
        print("(%i,%i)\t(%i,%i)\n(%i,%i)\t(%i,%i)"%(self.rowstart,self.colstart,self.rowstart,self.colstop,self.rowstop,self.colstart,self.rowstop,self.colstop))

    def get_shape(self):
        return (self.Nrows,self.Ncolumns)


class Image(object):
    ''' Class to handle RAW images '''
    
    file = None
    
    def __init__(self, data, rows=3000, columns=4000, datatype='uint16',channel_groups=(1,1)):
        '''
        Supports for 2 types of data input:
         - Numpy array
         - Path to RAW file
        '''

        if type(data) is numpy.ndarray:
            self.load_array(data)
        elif type(data) is str:
            self.load_RAWfile(data,rows,columns,datatype)
        else:
            raise Exception("first argument to RAW image constructor call is of the wrong type (array and string are valid)")

        self.set_channel_groups(channel_groups)


    def load_array(self, array):

        self.datatype = array.dtype.name
        self.array = numpy.array(array)

        self.rows = self.array.shape[0]
        self.columns = self.array.shape[1]

        self.ROI = ROI(0,self.rows,0,self.columns)


    def load_RAWfile(self, RAWfile, rows, columns, datatype):
        
        self.file = RAWfile
        
        self.datatype = datatype
        self.rows = rows
        self.columns = columns
        
        self.array = numpy.fromfile(RAWfile,dtype=self.datatype)

        if self.array.size < self.rows*self.columns:
            raise Exception("RAW data are smaller than the requested size for the array. Verify that you have the correct data type (dtype=%s?) and image size (rows=%i? columns=%i?)"%(self.datatype,rows,columns))
        elif self.array.size > self.rows*self.columns:
            raise Exception("RAW data are larger than the requested size for the array. Verify that you have the correct data type (dtype=%s?) and image size (rows=%i? columns=%i?)"%(self.datatype,rows,columns))
            #print "WARNING: RAW data are larger than the requested size for the array. We will only use the first %i values from the RAW image in this object."%(self.rows*self.columns)

        self.array = numpy.reshape(self.array,(self.rows,self.columns))        
        self.ROI = ROI(0,self.rows,0,self.columns)


    def info(self):
        print("FILE: %s"%self.file)
        print("ROWS: %i"%self.rows)
        print("COLUMNS: %i"%self.columns)
        print("DATA TYPE: %s"%self.datatype)
        print("CHANNEL GROUPS:",self.channel_groups)
        self.ROI.info()
        #print self.array
        print()


    # function overloaded
    #def set_ROI(self, rowstart, rowstop, colstart, colstop):
    #    print "Image: %ix%i ROI set"%(rowstop-rowstart,colstop-colstart)
    #    self.ROI = ROI(rowstart,rowstop,colstart,colstop)
    #    print "ROI modified to:"
    #    self.ROI.info()

    def set_ROI(self, roi):

        if roi==None:
            rowstart = 0
            rowstop = self.rows
            colstart = 0
            colstop = self.columns
        elif len(roi)==4:
            assert(roi[1]<self.rows and roi[3]<self.columns)
            rowstart = roi[0]
            rowstop = roi[1]
            colstart = roi[2]
            colstop = roi[3]
        elif len(roi)==2:
            assert(roi[0]<self.rows and roi[1]<self.columns)
            rowstart = int((self.rows-roi[0])/2.)
            rowstop = int((self.rows+roi[0])/2.)
            colstart = int((self.columns-roi[1])/2.)
            colstop = int((self.columns+roi[1])/2.)

        #print "Image: %ix%i ROI set"%(rowstop-rowstart,colstop-colstart)
        self.ROI = ROI(rowstart,rowstop,colstart,colstop)
        #print "ROI modified to:"
        #self.ROI.info()


    def set_center_ROI(self, roi_dim):
        # roi_dim is a tuple of dimension 2
        rowstart = int((self.rows-roi_dim[0])/2.)
        rowstop = int((self.rows+roi_dim[0])/2.)
        colstart = int((self.columns-roi_dim[1])/2.)
        colstop = int((self.columns+roi_dim[1])/2.)
        self.ROI = ROI(rowstart,rowstop,colstart,colstop)
        self.ROI.info()


    def infoROI(self):
        print("INFO ROI")
        self.ROI.info()
        print(self.array[self.ROI.rowstart:self.ROI.rowstop+1,self.ROI.colstart:self.ROI.colstop+1])
        print()


    def set_channel_groups(self,channel_groups):
        self.channel_groups = channel_groups
        self.num_channel_groups = self.channel_groups[0]*self.channel_groups[1]
        #print "Modified channel groups to:",self.channel_groups

        
    def get_row_group(self, i_channel_group):

        return i_channel_group / self.channel_groups[1]


    def get_column_group(self, i_channel_group):

        return i_channel_group % self.channel_groups[1]


    def get_rows(self):
        return self.rows


    def get_columns(self):
        return self.columns


    def get_shape(self):
        return (self.rows,self.columns)


    def get_shape_ROI(self):
        return self.ROI.get_shape()


    def get_datatype(self):
        return self.datatype


    def get_array(self, i_channel_group=None, bstack=False,bmerge=False,merge_group=(None,None)):

        # Returns array within selected ROI
        
        # bstack only if all channels and no merging
        assert(bstack==False or i_channel_group==None)
        assert(not(bstack and bmerge))
        
        if i_channel_group!=None:
            ''' return image for channel group i_channel_group only'''

            assert(i_channel_group<self.num_channel_groups)

            i_row_group = self.get_row_group(i_channel_group) #i_channel_group / self.channel_groups[1]
            i_col_group = self.get_column_group(i_channel_group) #i_channel_group % self.channel_groups[1]

            arr = self.array[self.ROI.rowstart+i_row_group:self.ROI.rowstop+1:self.channel_groups[0],self.ROI.colstart+i_col_group:self.ROI.colstop+1:self.channel_groups[1]]

        elif bmerge:
            ''' returns full array in ROI '''
            arr = self.array[self.ROI.rowstart:self.ROI.rowstop+1,self.ROI.colstart:self.ROI.colstop+1]
        
        elif bstack:
            ''' returns image split in channel groups '''

            arr = numpy.array([])

            for i_row_group in range(self.channel_groups[0]):

                arr_stack_row = numpy.array([])

                for i_col_group in range(self.channel_groups[1]):
                    arr_channel = self.array[self.ROI.rowstart+i_row_group:self.ROI.rowstop+1:self.channel_groups[0],self.ROI.colstart+i_col_group:self.ROI.colstop+1:self.channel_groups[1]]

                    if i_col_group==0:
                        arr_stack_row = arr_channel
                    else:
                        arr_stack_row = numpy.hstack((arr_stack_row,arr_channel))

                if i_row_group==0:
                    arr = arr_stack_row
                else:
                    arr = numpy.vstack((arr,arr_stack_row))

        else:
            ''' return full array in ROI '''
            arr = self.array[self.ROI.rowstart:self.ROI.rowstop+1,self.ROI.colstart:self.ROI.colstop+1]
        
        return arr


    def get_array_value(self, i, j):

        return self.array[i,j]


    def get_array_value_inROI(self, i, j, i_channel_group=None):

        arr = self.get_array(i_channel_group=i_channel_group)

        return arr[i,j]


    def get_image_channelsplit(self):

        return Image(self.get_array(bstack=True))


    def get_image_channel(self,i_channel_group):

        return Image(self.get_array(i_channel_group=i_channel_group))


    def zerocopy(self):

        import copy
        im = copy.deepcopy(self)
        shape = im.get_shape()
        im.array = numpy.zeros(shape,dtype='float32')
        
        im.ROI = self.ROI

        return im

    def zeroarray(self, bROI=False, channel=None):

        if bROI:
            shape = self.get_shape_ROI()
        else:
            shape = self.get_shape()

        if channel is not None:

            i_row_group = self.get_row_group(channel)
            i_col_group = self.get_column_group(channel)

            shape_row = shape[0] / self.channel_groups[0] + ((shape[0]%self.channel_groups[0]) > i_row_group)
            shape_col = shape[1] / self.channel_groups[1] + ((shape[1]%self.channel_groups[1]) > i_col_group)

            shape = (shape_row,shape_col)

        array = numpy.zeros(shape,dtype='float32')
        
        return array


    def subtract(self, image):
        self.array = self.array.astype('float32') - image.array.astype('float32')
        print("Image subtraction performed")
        return self.array


    def power(self, pow):
        self.array = self.array**pow
        print("Power operation performed")
        

    def divide(self, image):

        self.array = self.array.astype('float32')
        image.array = image.array.astype('float32')

        # to avoid 0./0. error (change below will lead to zero result instead for such case)
        numpy.place(image.array,image.array==0,[numpy.inf])

        self.array = self.array / image.array
        print("Image division performed\n")
        return self.array


    def multiply(self, constant):
        # Note the conversion from uint16 to int16 for proper arithmetic
        self.array = self.array.astype('float32')*constant
        #print "Image multiplied by %f\n"%constant
        return self.array


    def get_profile(self,axis=0,i_channel_group=None, bstack=False):
        
        if bstack:
            arr = self.get_array(bstack=bstack)
        else:
            arr = self.get_array(i_channel_group=i_channel_group)

        # compute average array along axis
        profile_array = numpy.sum(arr,axis=axis)
        profile_array = profile_array / arr.shape[axis]

        return profile_array


    def get_profile_image(self,axis=0,i_channel_group=None):

        profile_array = self.get_profile(axis=axis,i_channel_group=i_channel_group)

        # reshape to transform 1D array into 2D
        if axis==0:
            profile_array = profile_array.reshape((1,profile_array.shape[0]))
        else:
            profile_array = profile_array.reshape((profile_array.shape[0],1))

        im = Image(profile_array)

        return im


    def get_mean(self):
        return numpy.mean(self.get_array())


    def get_mean_channel_groups(self):
        # this should be merged into get_mean method; and while we're at it get_mean method should be constructed with the same template structure
        means = []
        for i_channel_group in range(self.num_channel_groups):
            arr = self.get_array(i_channel_group)
            means.append(arr.mean())
        return means


    def get_median(self):
        return numpy.median(self.get_array())


    def get_median_channel_groups(self):
        medians = []
        for i_channel_group in range(self.num_channel_groups):
            arr = self.get_array(i_channel_group)
            medians.append(numpy.median(arr))
        return medians


    def get_rms(self,minval=None,maxval=None):
        arr = self.get_array()
        if minval!=None:
            arr = arr[arr>=minval]
        if maxval!=None:
            arr = arr[arr<=maxval]
        stddev = numpy.std(arr)
        return stddev


    def get_rms_channel_groups(self,bfit=False,nbins=100,Nsigma=3):
        # if bfit==True, gaussian fit will be performed to determine standard deviation

        stddev = []

        if not(bfit):

            for i_channel_group in range(self.num_channel_groups):
                arr = self.get_array(i_channel_group)
                #arr = arr[numpy.abs(arr)<2000]
                stddev.append(numpy.std(arr))

        else:
            
            from scipy.optimize import curve_fit
            
            for i_channel_group in range(self.num_channel_groups):
                
                arr = self.get_array(i_channel_group)

                xmin,xmax = PlotTools.set_minmax(arr)

                hist, bins = numpy.histogram(arr,bins=nbins,range=(xmin,xmax))
                width = bins[1] - bins[0]
                center = (bins[:-1] + bins[1:]) / 2
                
                mean_fit = numpy.mean(arr)
                sigma_fit = numpy.std(arr)
                center_fit = center[abs(center-mean_fit) < Nsigma * sigma_fit]
                hist_fit = hist[abs(center-mean_fit) < Nsigma * sigma_fit]
                
                pstart = [hist_fit[numpy.abs(center_fit-mean_fit).argmin()],mean_fit,sigma_fit]
                print("PSTART:",pstart)
                popt,pcov = curve_fit(gaus,center_fit,hist_fit,p0=pstart)
                
                print("POPT:",abs(popt))
                stddev.append(abs(popt[2]))

        return stddev


    def get_noise(self,bminmax=False):

        total_noise = []
        row_noise = []
        column_noise = []
        pixel_noise = []

        for i_channel_group in range(self.num_channel_groups):

            arr = self.get_array(i_channel_group)
            #arr2 = arr[numpy.abs(arr)<2000]
            arr_row = numpy.mean(arr,axis=1)
            arr_col = numpy.mean(arr,axis=0)

            if bminmax:
                total_noise.append(numpy.amax(arr)-numpy.amin(arr))
                row_noise.append(numpy.amax(arr_row)-numpy.amin(arr_row))
                column_noise.append(numpy.amax(arr_col)-numpy.amin(arr_col))
            else:
                total_noise.append(numpy.std(arr))
                row_noise.append(numpy.std(arr_row))
                column_noise.append(numpy.std(arr_col))

            pixel_noise.append((total_noise[-1]**2-row_noise[-1]**2-column_noise[-1]**2)**0.5)

        return total_noise,row_noise,column_noise,pixel_noise


    def column_swap(self):
        '''
        Swap of odd/even columns in odd rows only:
        a0 b0 c0 d0 => a0 b0 c0 d0
        a1 b1 c1 d1 => b1 a1 d1 c1
        Physical map of ADC readout:
        even row: 1 2 3 4
        odd row : 2 1 4 3
        !!! Upgrade with option to column swap odd and/or even rows
        '''

        # separate odd and even rows
        arr_fix = self.array[::2,:] # even rows
        arr_swap = self.array[1::2,:] # odd rows

        # in odd rows: separate odd and even columns
        arr_swap_col0 = arr_swap[:,::2]
        arr_swap_col1 = arr_swap[:,1::2]

        # column swapping for odd rows happen here
        arr_swap = numpy.insert(arr_swap_col0,list(range(0,arr_swap_col1.shape[1])),arr_swap_col1,axis=1)

        # merge odd and even rows back
        self.array = numpy.insert(arr_fix,list(range(1,arr_swap.shape[0]+1)),arr_swap,axis=0)


    def hstack(self, image, bresetROI=True):
        '''
        Stack image argument below self.image.
        Number of columns must be the same in both images.
        '''

        assert(self.array.shape[0]==image.array.shape[0])

        self.array = numpy.hstack((self.array,image.array))
        self.rows += image.rows

        if bresetROI:
            self.ROI = ROI(0,self.rows,0,self.columns)


    def vstack(self, image, bresetROI=True):
        '''
        Stack image argument to the right of self.image.
        Number of rows must be the same in both images.
        '''

        assert(self.array.shape[1]==image.array.shape[1])

        self.array = numpy.vstack((self.array,image.array))
        self.columns += image.columns

        if bresetROI:
            self.ROI = ROI(0,self.rows,0,self.columns)


    def FPN_correction(self, bswap=False,  rowstart=0, rowstop=64, target=None):

        fpn_correction_factors = self.calculate_FPN_correction(bswap=bswap,rowstart=rowstart,rowstop=rowstop,target=target)
        self.apply_FPN_correction(fpn_correction_factors,bswap=bswap)

    def calculate_FPN_correction(self, bswap=False, rowstart=0, rowstop=64, target=None):
        '''
        Note: column swap needed to align pixels read out by same ADCs in regular images.
        '''

        print("\nCalculating FPN correction factors (fpn row used: %i=>%i)..."%(rowstart,rowstop))

        if bswap:
            self.column_swap()

        arr_refcol = self.array[rowstart:rowstop+1,:]

        if target==None:
            targetval = self.array.mean()
        else:
            targetval = target

        fpn_correction_factors = targetval - arr_refcol.mean(axis=0).astype('float32')

        if bswap:
            self.column_swap()

        return fpn_correction_factors


    def apply_FPN_correction(self, fpn_correction_factors, bswap=False):
        '''
        Apply FPN correction factor on the whole array
        '''

        print("Applying FPN correction factors...")
        
        if len(fpn_correction_factors)!=self.array.shape[1]:
            raise Exception("Length of FPN correction factor array is different from number of columns in image array. Please fix.")

        if bswap:
            self.column_swap()

        # fpn_correction_factors vector added to all rows
        print(fpn_correction_factors)
        self.array = self.array + fpn_correction_factors

        if bswap:
            self.column_swap()

        print("FPN correction applied")


    def RTN_correction(self, bswap=False, colstart=4, colstop=67, target=None, boddeven=False, bsave=False, filename=None):

        rtn_correction_factors = self.calculate_RTN_correction(bswap=bswap,colstart=colstart,colstop=colstop,target=target,bsave=bsave,filename=filename)
        self.apply_RTN_correction(rtn_correction_factors,bswap=bswap)


    def calculate_RTN_correction(self, bswap=False, colstart=4, colstop=67, target=None, boddeven=False, bsave=False, filename=None):
        '''
        Estimate RTN correction factors in selected columns (colstart:colstop) for each ADC channels.
        Note: column swap needed to align pixels read out by same ADCs in regular images.
        '''

        print("\nCalculating RTN correction factors (rtn col used: %i=>%i)..."%(colstart,colstop))

        if bswap:
            self.column_swap()

        number_adc = 4
        arr_adc = []
        rtn_correction_factors = []
        self.rtn_noise = []

        arr_refcol = self.array[:,colstart:colstop+1]

        for i_adc in range(number_adc):

            arr_adc.append(arr_refcol[:,i_adc::number_adc])
            assert(arr_adc[-1].shape==arr_adc[0].shape) # to ensure each ADC uses the same number of pixel

            if target==None and boddeven:
                # computes correction factor independently for odd and even rows (can be used to apply RTN on color parts where R and B should go to different target values)
                for i_row in [0,1]:
                    arr_even = arr_adc[i_adc][::2,:]
                    arr_odd = arr_adc[i_adc][1::2,:]

                targetval_even = arr_even.mean()
                targetval_odd = arr_odd.mean()
                print('target even:',targetval_even)
                print('target odd:',targetval_odd)

                rtn_corr_even = targetval_even - arr_even.mean(axis=1).astype('float32')
                rtn_corr_odd = targetval_odd - arr_odd.mean(axis=1).astype('float32')

                rtn_corr_oddeven = numpy.insert(rtn_corr_even,list(range(1,rtn_corr_odd.shape[0]+1)),rtn_corr_odd)

                rtn_correction_factors.append(rtn_corr_oddeven)

            else:

                if target==None:
                    targetval = arr_adc[i_adc].mean()
                    print('target [ADC %i]:'%i_adc,targetval)
                else:
                    targetval = target

                rtn_correction_factors.append(targetval - arr_adc[i_adc].mean(axis=1).astype('float32'))

            self.rtn_noise.append(numpy.std(rtn_correction_factors[i_adc]))

        print("RTN noise:", self.rtn_noise)

        if bswap:
            self.column_swap()

        if bsave:

            title = "Row Noise:"
            #title = "RTN:"
            correc_fact = 1
            #correc_fact = 1/2**0.5
            for i_adc in range(number_adc):
                title += ' %.1f'%(self.rtn_noise[i_adc]*correc_fact)
                #pylab.plot(range(self.rows),rtn_correction_factors[i_adc])
                #pylab.plot(range(100),rtn_correction_factors[i_adc][:100])
                #pylab.plot(range(1000,1200),rtn_correction_factors[i_adc][1000:1200])
                #pylab.plot(range(1000,1200),[v*correc_fact for v in rtn_correction_factors[i_adc][1000:1200]])
                pylab.plot(list(range(self.rows)),[v*correc_fact for v in rtn_correction_factors[i_adc]])
            title += ' DN'
            pylab.xlabel('Rows')
            pylab.ylabel('RTN correction [DN]')
            pylab.title(title)
            print("Saving RTN profiles: %s"%filename)
            pylab.savefig(filename)
            pylab.clf()
            pylab.close()

        return rtn_correction_factors


    def apply_RTN_correction(self,rtn_correction_factors,bswap=False):
        '''
        Apply RTN correction factor on the whole array
        '''

        print("Applying RTN correction factors...")

        import copy

        if len(rtn_correction_factors[0])!=self.array.shape[0]:
            raise Exception("Length of RTN correction factor array is different from number of rows in image array. Please fix.")

        if bswap:
            self.column_swap()

        number_adc = 4
        arr_adc = []

        for i_adc in range(number_adc):

            #arr_adc.append(self.array[:,i_adc::number_adc])
            arr_adc.append(copy.deepcopy(self.array[:,i_adc::number_adc]))

            # rtn_correction_factors vector added to all columns of each ADC
            arr_adc[i_adc] += rtn_correction_factors[i_adc][:,numpy.newaxis]

        # putting the RTN corrected array back together
        array_RTNcorrected = arr_adc[0]
        array_RTNcorrected = numpy.insert(array_RTNcorrected,list(range(1,arr_adc[1].shape[1]+1)),arr_adc[1],axis=1)
        array_RTNcorrected = numpy.insert(array_RTNcorrected,list(range(2,arr_adc[2].shape[1]*2+1,2)),arr_adc[2],axis=1)
        array_RTNcorrected = numpy.insert(array_RTNcorrected,list(range(3,arr_adc[3].shape[1]*3+1,3)),arr_adc[3],axis=1)
        self.array = array_RTNcorrected

        if bswap:
            self.column_swap()

        print("RTN correction applied")


    def correlate(self,image,channel=None,bPearson=True,bplot=True,figsize=9):

        fig = pylab.figure(2,(16/9.*figsize,figsize))

        if channel==None:
            channels_to_plot = list(range(self.num_channel_groups))
        else:
            channels_to_plot = [channel]

        # Set rows and columns of figure:
        if len(channels_to_plot)==1:
            n_row_fig = 1
        else:
            n_row_fig = numpy.ceil(len(channels_to_plot)**0.5)
        n_col_fig = numpy.ceil(float(len(channels_to_plot))/n_row_fig)

        r_pearson = []

        for i_plot,i_channel_group in enumerate(channels_to_plot):

            ax = fig.add_subplot(n_row_fig,n_col_fig,i_plot+1)

            profile0 = self.get_profile(axis=0,i_channel_group=i_channel_group)
            profile1 = image.get_profile(axis=0,i_channel_group=i_channel_group)

            # recenter profile
            profile0_forcorr = profile0 - numpy.mean(profile0)
            profile1_forcorr = profile1 - numpy.mean(profile1)

            assert(len(profile0)==len(profile1))

            from scipy import stats
            
            if bPearson:
                # Compute Pearson's statistics
                rp_pearson = stats.pearsonr(profile0,profile1)
                print(rp_pearson)
                r_pearson.append(rp_pearson[0])
            
            from scipy import signal

            correlation_array = signal.correlate(profile0_forcorr,profile1_forcorr,mode='full')
        
            if bplot:

                if bPearson:
                    #xmin = 550
                    #xmax = 650
                    #pylab.plot(range(len(profile0)),profile0,linewidth=3,color='b')
                    #pylab.plot(range(len(profile1)),profile1,linewidth=3,color='r')
                    #pylab.xlabel('Column')
                    #pylab.ylabel('Average response [DN]')
                    #pylab.xlim([xmin,xmax])
                    #pylab.ylim([0.9*min(min(profile0[xmin:xmax]),min(profile1[xmin:xmax])),1.1*max(max(profile0[xmin:xmax]),max(profile1[xmin:xmax]))])
                    #pylab.title('Channel %i'%i_plot)
                    pylab.scatter(profile0,profile1)
                    pylab.xlabel('Image0 column average [DN]')
                    pylab.ylabel('Image1 column average [DN]')
                    pylab.title(r'$r_{Pearson}$ = %.3f'%r_pearson[i_channel_group])
                else:
                    delta = list(range(-(len(correlation_array)-1)/2,(len(correlation_array)-1)/2+1))
                    pylab.plot(delta,correlation_array)
                    pylab.xlabel(r'$\Delta$Column')
                    pylab.ylabel('Correlation')
                    #pylab.xlim([-100,100])
                    pylab.title('Channel %i'%i_plot)
                
                pylab.grid(True)
                

        if bplot: pylab.show()

        if bPearson:
            return r_pearson
        else:
            return correlation_array
        

    def autocorrelate(self,channel=None,bplot=True,figsize=9):

        self.correlate(self,bPearson=False,bplot=bplot,figsize=figsize)


    def plot_histogram(self, show_channels=None,bsigma=False,xmin=None, xmax=None, nbins=100, ylim=None, blog=False, figsize=9, bsave=False, filename="fig_hist.png", title='', xlabel="DN", ylabel="# pixels", color='b', legend_label=None, legend_location='upper center', bfit=False, image2=None, color2='r',legend_label2=None):

        fig = pylab.figure(2,(16/9.*figsize,figsize))

        if show_channels==None:
            show_channels = list(range(self.num_channel_groups))
            arr = self.get_array()
            xmin,xmax = PlotTools.set_minmax(arr,minval=xmin,maxval=xmax,bsigma=bsigma)
        elif type(show_channels)==int:
            show_channels = [show_channels]
            for i_chan in show_channels:
                arr = self.get_array(i_channel_group=i_chan)
                xmin,xmax = PlotTools.set_minmax(arr,minval=xmin,maxval=xmax,bsigma=bsigma)
        xmin = xmin - 0.05*(xmax-xmin)
        xmax = xmax + 0.05*(xmax-xmin)

        if nbins=='fullresolution':
            xmin = numpy.floor(xmin)-0.5
            xmax = numpy.ceil(xmax)+0.5
            nbins = xmax-xmin

        # Set rows and columns of figure:
        if len(show_channels)==1:
            n_row_fig = 1
        else:
            n_row_fig = numpy.ceil(len(show_channels)**0.5)
        n_col_fig = numpy.ceil(float(len(show_channels))/n_row_fig)

        for i_plot,i_channel_group in enumerate(show_channels):

            ax = fig.add_subplot(n_row_fig,n_col_fig,i_plot+1)

            arr = self.get_array(i_channel_group)
            
            hist, bins = numpy.histogram(arr,bins=nbins,range=(xmin,xmax))
            width = bins[1] - bins[0]
            center = (bins[:-1] + bins[1:]) / 2
            
            if legend_label==None:
                pylab.bar(center, hist, align='center', width=width, log=blog, color=color)
            else:
                pylab.bar(center, hist, align='center', width=width, log=blog, color=color,label=legend_label)
            #pylab.plot(center, hist,color=color)

            # 2nd image plotting
            if image2 != None:

                assert(self.channel_groups==image2.channel_groups)

                arr2 = image2.get_array(i_channel_group)
            
                hist2, bins2 = numpy.histogram(arr2,bins=nbins,range=(xmin,xmax))
            
                if legend_label2==None:
                    pylab.bar(center, hist2, align='center', width=width, log=blog, color=color2,edgecolor='r',fill=False)
                else:
                    pylab.bar(center, hist2, align='center', width=width, log=blog, color=color2,edgecolor='r',fill=False,label=legend_label2)

            if bfit:

                from scipy.optimize import curve_fit

                mean_fit = numpy.mean(arr)
                sigma_fit = numpy.std(arr)
                center_fit = center[abs(center-mean_fit)<3*sigma_fit]
                hist_fit = hist[abs(center-mean_fit)<3*sigma_fit]

                popt,pcov = curve_fit(gaus,center_fit,hist_fit,p0=[hist_fit[numpy.abs(hist_fit-mean_fit).argmin()],mean_fit,sigma_fit])

                pylab.plot(center_fit,gaus(center_fit,*popt),'b--',linewidth=3)

            legend = ax.legend(loc=legend_location, shadow=True)

            pylab.xlim([xmin,xmax])

            if ylim!=None:
                pylab.ylim([ylim[0],ylim[1]])
            elif ylim==None and blog:
                (ymin,ymax) = pylab.ylim()
                pylab.ylim([0.1*ymin,ymax])

            # only show ylabels for pads on the left or xlabel for pads at the bottom
            if i_plot>=n_col_fig*(n_row_fig-1): pylab.xlabel(xlabel)
            if i_plot%n_col_fig==0: pylab.ylabel(ylabel)
            #pylab.title(title)
            pylab.title('Channel %i'%i_channel_group)
            pylab.grid(True)

        if bsave:
            print("Saving histogram: %s"%filename)
            pylab.savefig(filename)
            pylab.clf()
            pylab.close()
        else:           
            pylab.show()


    def plot_image(self, bstack=False,bsigma=False, minval=None, maxval=None, figsize=9, bsave=False, filename="fig_image.pdf", title='', bfullresolution=False, dpi=80, colorscale='jet',bcolorbar=True,colorbar_label=''):

        arr = self.get_array(bstack=bstack)

        minval,maxval = PlotTools.set_minmax(arr,minval=minval,maxval=maxval,bsigma=bsigma)

        if bfullresolution:

            import matplotlib.cm as cm
            fig = pylab.figure(figsize=(self.columns*0.01,self.rows*0.01))
            #pylab.figimage(arr,cmap=cm.jet,vmin=minval,vmax=maxval,origin='upper')
            pylab.figimage(arr,cmap=cm.hot,vmin=minval,vmax=maxval,origin='upper')

        else:

            fig = pylab.figure(1,(4/3.*figsize,figsize))
            ax = fig.add_subplot(111)
            image = pylab.imshow(arr,interpolation='nearest')
            
            norm = matplotlib.colors.Normalize(vmin=minval, vmax=maxval)
            image.set_norm(norm)
        
            pylab.title(title)

            image.set_cmap(colorscale) # gray/hot/jet
        
            if bcolorbar: pylab.colorbar(label=colorbar_label)

        if bsave:
            print("Saving image: %s"%filename)
            if bfullresolution:
                pylab.savefig(filename)
            else:
                pylab.savefig(filename,dpi=dpi)
            pylab.clf()
            pylab.close()
        else:
            pylab.show()


    def plot_profile(self, axis=0, bstack=False, show_channels=None, figsize=9, xlim=None, ylim=None, bsave=False, filename="fig_profile.png", title=None, xlabel=None, ylabel=None, color='b', lw=2, legend_label=None, legend_location='upper center', image2=None, color2='r', legend_label2=None):

        fig = pylab.figure(2,(16/9.*figsize,figsize))

        if show_channels==None: 
            show_channels = list(range(self.num_channel_groups))
        elif type(show_channels)==int:
            show_channels = [show_channels]

        if axis==0:
            if xlabel==None: xlabel = 'Column'
            if ylabel==None: ylabel = 'Column average'
        else:
            if xlabel==None: xlabel = 'Row'
            if ylabel==None: ylabel = 'Row average'

        # Set rows and columns of figure:
        if len(show_channels)==1:
            n_row_fig = 1
        else:
            n_row_fig = numpy.ceil(len(show_channels)**0.5)
        n_col_fig = numpy.ceil(float(len(show_channels))/n_row_fig)

        # set min/max
        if ylim==None:
            profile_array = self.get_profile(axis=axis, bstack=bstack)
            ymin,ymax = PlotTools.set_minmax(profile_array)
            dy = ymax - ymin
            ymin = ymin - 0.1*dy
            ymax = ymax + 0.1*dy

        for i_plot,i_channel_group in enumerate(show_channels):

            ax = fig.add_subplot(n_row_fig,n_col_fig,i_plot+1)
            
            profile_array = self.get_profile(axis=axis,i_channel_group=i_channel_group, bstack=bstack)

            if legend_label==None:
                pylab.plot(list(range(len(profile_array))),profile_array,color=color,linewidth=lw)
            else:
                pylab.plot(list(range(len(profile_array))),profile_array,color=color,linewidth=lw,label=legend_label)


            # 2nd image plotting
            if image2 != None:

                assert(self.channel_groups==image2.channel_groups)

                profile_array2 = image2.get_profile(axis=axis,i_channel_group=i_channel_group)
            
                if legend_label2==None:
                    pylab.plot(list(range(len(profile_array2))),profile_array2,color=color2,linewidth=lw)
                else:
                    pylab.plot(list(range(len(profile_array2))),profile_array2,color=color2,linewidth=lw,label=legend_label2)
            

            legend = ax.legend(loc=legend_location, shadow=True)

            #locs,labels = pylab.yticks()
            #pylab.yticks(locs, map(lambda x: "%.2f" % x, locs))
            
            if xlim != None: pylab.xlim([xlim[0],xlim[1]])
            if ylim != None: 
                pylab.ylim([ylim[0],ylim[1]])
            else:
                pylab.ylim([ymin,ymax])                

            if title==None: 
                pylab.title('Channel %i'%i_channel_group)
            else: 
                pylab.title(title)

            if i_plot>=n_col_fig*(n_row_fig-1): pylab.xlabel(xlabel)
            if i_plot%n_col_fig==0: pylab.ylabel(ylabel)

            pylab.grid(True)

        if bsave:
            print("Saving histogram: %s"%filename)
            pylab.savefig(filename)
            pylab.clf()
            pylab.close()
        else:           
            pylab.show()


    def plot_column_profile(self, show_channels=None, figsize=9, xlim=None, ylim=None, bsave=False, filename="fig_profile.png", title=None, xlabel=None, ylabel=None, color='b', lw=2, legend_label=None, legend_location='upper center', image2=None, color2='r', legend_label2=None):

        self.plot_profile(axis=0, show_channels=show_channels, figsize=figsize, xlim=xlim, ylim=ylim, bsave=bsave, filename=filename, title=title, xlabel=xlabel, ylabel=ylabel, color=color, lw=lw, legend_label=legend_label, legend_location=legend_location, image2=image2, color2=color2, legend_label2=legend_label2)


    def plot_row_profile(self, show_channels=None, figsize=9, xlim=None, ylim=None, bsave=False, filename="fig_profile.png", title=None, xlabel=None, ylabel=None, color='b', lw=2, legend_label=None, legend_location='upper center', image2=None, color2='r', legend_label2=None):

        self.plot_profile(axis=1, show_channels=show_channels, figsize=figsize, xlim=xlim, ylim=ylim, bsave=bsave, filename=filename, title=title, xlabel=xlabel, ylabel=ylabel, color=color, lw=lw, legend_label=legend_label, legend_location=legend_location, image2=image2, color2=color2, legend_label2=legend_label2)


    def save2raw(self,filename='image.raw'):
        
        print('\nsaving RAW file %s...'%filename)
        #self.array.tofile(filename)
        self.get_array(bstack=True).tofile(filename)
        print('Image saved to %s'%filename)


    def save2ascii(self,filename,separator=',',bverbose=True):

        print("Saving to ASCII file...")
        fascii = open(filename,'w')

        fascii.write("ROW%sCOLUMN%sVALUE\n"%(separator,separator))

        for (x,y),value in numpy.ndenumerate(self.get_array()):
            pixel_num = x*self.columns + y
            if pixel_num%100000==0 and bverbose: print('at pixel %i...'%pixel_num)
            fascii.write("%i%s%i%s%.1f\n"%(x,separator,y,separator,value))

        fascii.close()

        print("Created ASCII file: %s"%filename)
        print("Separator used: '%c'"%separator)


    def save2csv(self,filename,bverbose=True):

        self.save2ascii(filename,separator=',',bverbose=bverbose)


if __name__ == '__main__':

    rawfile = 'F:\\INVISAGE\\PC3\\Read_Noise\\Data\\20140131_Q8A624w05#35-H\\LowNoiseAurel_sim_nonsim_Q8A624w17#14-D_v0_013114_140607\\RawImages_noise\\image_non-simultaneous_1.raw'

    im = Image(rawfile,rows=3000,columns=4000,datatype='uint16')
    im.plot_histogram()
    im.plot_image()
