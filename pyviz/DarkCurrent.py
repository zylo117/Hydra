#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import numpy
import glob
import os
import copy
import pylab

from . import Image
from . import ImageArray

class DarkCurrent(object):

    def __init__(self,directory, integration_times, sensor_name="Sensor999", vbias=99, rows=3000, columns=4000, datatype='uint16', roi_type=None, roi_dim=None, file_wildcard_offset=None, analysis_type = "mean", max_files=None):
        
        self.directory = directory

        self.integration_times = integration_times
        self.sensor_name = sensor_name
        self.vbias = vbias

        self.file_wildcard_offset = file_wildcard_offset

        self.rows = rows
        self.columns = columns
        self.datatype = datatype

        if roi_type == 'center':
            self.ROI = Image.ROI((rows-roi_dim[0])/2.,(rows+roi_dim[0])/2.,(columns-roi_dim[1])/2.,(columns+roi_dim[1])/2.)
        else:
            print("No ROI selected. Analysis will be performed over the whole image.")
            self.ROI = None

        self.images_integration_times = []
        
        self.analysis_type = analysis_type

        print("max files:",max_files)
        self.max_files = max_files

    def info(self):
        print("Directory: %s"%self.directory)
        for i in range(len(self.integration_times)):
            print("Integration time: %s sec"%str(self.integration_times[i]))
            if self.file_wildcard_offset ==None:
                print("No offset files provided")
            else:
                print("File wildcard offset: %s sec"%(self.file_wildcard_offset))
            print()

    def load_data(self):

        if self.file_wildcard_offset != None:
            RAWfiles_offset = glob.glob(self.file_wildcard_offset)
            self.images_offset = ImageArray.ImageArray(RAWfiles_offset,self.rows,self.columns,self.datatype)
            self.image_avg_offset = self.images_offset.average()
        
        self.image_avg_integration_times = []

        for i in range(len(self.integration_times)):
        
            print("Integration time: %s sec"%str(self.integration_times[i]))

            wildcard_search = os.path.join(self.directory,'*'+str(self.integration_times[i])+'Tintsecs*.raw')
            print("Searching files with wildcard %s"%wildcard_search)
            RAWfiles_integration_time = glob.glob(wildcard_search)

            print("Number of files found:",len(RAWfiles_integration_time))

            if self.max_files != None:
                RAWfiles_integration_time = RAWfiles_integration_time[:self.max_files]
                print("Number of files used:",self.max_files)

            self.images_integration_times.append(ImageArray.ImageArray(RAWfiles_integration_time,self.rows,self.columns,self.datatype))

            print("Computing average image...")
            self.image_avg_integration_times.append(self.images_integration_times[i].average())

            if self.file_wildcard_offset != None:
                self.image_avg_integration_times[i].subtract(self.image_avg_offset)

            if self.ROI != None:
                self.image_avg_integration_times[i].ROI = self.ROI
                #self.image_avg_integration_times[i].infoROI()

    def compute_avgDN(self,image_avg_integration_times):

        avgDN = []
        for i in range(len(self.integration_times)):
            if self.analysis_type == "mean":
                avgDN.append(image_avg_integration_times[i].get_mean())
            elif self.analysis_type == "median":
                avgDN.append(image_avg_integration_times[i].get_median())

        return avgDN


    @staticmethod
    def _pol1D(x,a,b): 
        # Fitting function for dark current computation
        return a*x+b

    def compute_DarkCurrent(self, avgDN):

        from scipy.optimize import curve_fit
        
        params = curve_fit(self._pol1D,numpy.array(self.integration_times),numpy.array(avgDN))
        dark_current = params[0][0]
        offset = params[0][1]

        print("Dark Current: %f DN/sec"%dark_current)

        return (offset,dark_current)

    def create_DarkCurrent_image(self):
        i1 = -1
        i0 = 0
        # replace with more exact extrapolation of linear fitting on each pixel !!
        image = copy.deepcopy(self.image_avg_integration_times[i1])
        image.subtract(self.image_avg_integration_times[i0])
        image.multiply(1/(self.integration_times[i1]-self.integration_times[i0]))
        return image

    def compute_QF_DarkCurrent(self, dc_ref):
        
        self.image_QF_avg_integration_times = []
        for i in range(len(self.integration_times)):
            self.image_QF_avg_integration_times.append(copy.deepcopy(self.image_avg_integration_times[i]))
            self.image_QF_avg_integration_times[i].subtract(dc_ref.image_avg_integration_times[i])

        self.avgDN_QF_in_roi = self.compute_avgDN(self.image_QF_avg_integration_times)
        self.offset_DN_QF,self.dark_current_QF = self.compute_DarkCurrent(self.avgDN_QF_in_roi)

        '''
        self.image_QF_DarkCurrent = copy.deepcopy(self.image_DarkCurrent)
        self.image_QF_DarkCurrent.subtract(dc_ref.image_DarkCurrent)
        self.dark_current_QF = self.image_QF_DarkCurrent.get_mean()
        #self.dark_current_QF = self.dark_current - dc_ref.dark_current
        print "COMPARISON:", self.dark_current_QF, self.dark_current - dc_ref.dark_current
        print "QF Dark Current: %f DN/sec"%self.dark_current_QF
        '''

    def save2csv(self):
        '''
        for i in range(len(self.integration_times)):
            csvfilename = os.path.join(self.directory,''+str(int(1000*self.integration_times[i]))+'ms','Dark','average.csv')
            self.image_avg_integration_times[i].save2ascii(csvfilename,',')
        '''
        csvfilename = os.path.join(self.directory_analysis,'%s_DarkCurrent_%.1fV.csv'%(self.sensor_name,self.vbias))
        self.image_DarkCurrent.save2ascii(csvfilename,',')
        
    def save2csv_QF(self):
        csvfilename = os.path.join(self.directory,'%s_DarkCurrent_QF_%.1fV.csv'%(self.sensor_name,self.vbias))
        self.image_QF_DarkCurrent.save2ascii(csvfilename,',')

    def plot_response_vs_integration_time(self, avgDN, figsize=9, bfit=False, fit_offset=None, fit_slope=None, bsave=False, filename="fig_resp.png", title='', xmin=None, xmax=None, xlabel="Integration Times [sec]", ylabel="Average DN", color='b'):
        
        fig = pylab.figure(2,(16/9.*figsize,figsize))

        pl_data,=pylab.plot(self.integration_times,avgDN,marker='D',markersize=10,linewidth=3,color=color)

        x_pol1D = numpy.linspace(self.integration_times[0], self.integration_times[-1], 100)
        y_pol1D = self._pol1D(x_pol1D,fit_slope,fit_offset)
        pl_fit,=pylab.plot(x_pol1D,y_pol1D,linewidth=3,color='cyan')

        pylab.legend([pl_data,pl_fit],["Data","Fit"],loc='upper center')

        pylab.title(title)
    
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        
        if xmin==None:
            xmin = pylab.xlim()[0]
        if xmax==None:
            xmax = pylab.xlim()[1]
        pylab.xlim([xmin,xmax])

        pylab.grid(True)

        if bsave:
            pylab.savefig(filename)
            pylab.close()
        else:           
            pylab.show()

    def save_plots(self, blog=False):

        for i in range(len(self.integration_times)):

            pngfilename = os.path.join(self.directory_analysis,'%s_avgDNdist_%.4fsec.png'%(self.sensor_name,self.integration_times[i]))
            self.image_avg_integration_times[i].plot_histogram(xmin=0,nbins=400,bsave=True,filename=pngfilename,title=self.sensor_name,blog=blog)
            pngfilename = os.path.join(self.directory_analysis,'%s_avgDNimage_%.4fsec.png'%(self.sensor_name,self.integration_times[i]))
            self.image_avg_integration_times[i].plot_image(bsave=True,filename=pngfilename,title=self.sensor_name)

        pngfilename = os.path.join(self.directory_analysis,'%s_DNvsT.png'%self.sensor_name)
        self.plot_response_vs_integration_time(self.avgDN_in_roi,bfit=True,fit_offset=self.offset_DN, fit_slope=self.dark_current, bsave=True, filename=pngfilename,title='%s; DC = %.1f DN/sec'%(self.sensor_name,self.dark_current),xmin=0)

        pngfilename = os.path.join(self.directory_analysis,'%s_DCdist.png'%self.sensor_name)
        self.image_DarkCurrent.plot_histogram(xmin=0,nbins=400,bsave=True,filename=pngfilename,title=self.sensor_name,xlabel="DN/sec",blog=blog)
        pngfilename = os.path.join(self.directory_analysis,'%s_DCimage.png'%self.sensor_name)
        self.image_DarkCurrent.plot_image(bsave=True,filename=pngfilename,title=self.sensor_name)

    def save_plots_QF(self, blog=False):

        #pngfilename = os.path.join(self.directory_analysis,'%s_DCdist_QF_%.1fV.png'%(self.sensor_name,self.vbias))
        #self.image_QF_DarkCurrent.plot_histogram(xmin=0,bsave=True,filename=pngfilename,xlabel="DN/sec",blog=blog)
        #pngfilename = os.path.join(self.directory_analysis,'%s_DCImage_QF_%.1fV.png'%(self.sensor_name,self.vbias))
        #self.image_QF_DarkCurrent.plot_image(bsave=True,filename=pngfilename)
    
        pngfilename = os.path.join(self.directory_analysis,'%s_QF_DNvsT.png'%self.sensor_name)
        self.plot_response_vs_integration_time(self.avgDN_QF_in_roi,bfit=True,fit_offset=self.offset_DN_QF, fit_slope=self.dark_current_QF, bsave=True, filename=pngfilename,title='%s; DC [QF] = %.1f DN/sec'%(self.sensor_name,self.dark_current_QF), xmin=0)

    def analyze(self,bsave=False):

        print("Starting ANALYSIS")
        
        self.directory_analysis = os.path.join(self.directory,"Analysis_v0")
        if not(os.path.exists(self.directory_analysis)):
            os.mkdir(self.directory_analysis)

        self.load_data()

        self.avgDN_in_roi = self.compute_avgDN(self.image_avg_integration_times)

        self.offset_DN,self.dark_current = self.compute_DarkCurrent(self.avgDN_in_roi)

        self.image_DarkCurrent = self.create_DarkCurrent_image()

        self.dsnu = self.image_DarkCurrent.get_rms()
