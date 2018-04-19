#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import numpy

import matplotlib
import pylab

import os

#colors = [(0,0,0),(1,0,0),(1,0.5,0),(0,1,0),(0,1,1),(0,0,1),(0.5,0,1),(1,0,1)]
colors = [(0,0,0),(1,0,0),(1,0.5,0),(0,1,0),(0,1,1),(0,0,1),(0.5,0,1),(1,0,1),(0.2,0.2,0.2),(1,0.2,0.2),(1,0.5,0.2),(0.2,1,0.2),(0.2,1,1),(0.2,0.2,1),(0.5,0.2,1),(1,0.2,1)]
colors=colors*2

def set_figure_font(size=14, xlabelsize=15, ylabelsize=17, legendsize=17):

    font = {'size'   : size}
    matplotlib.rc('font', **font)

    matplotlib.rc('xtick', labelsize=xlabelsize) 
    matplotlib.rc('ytick', labelsize=ylabelsize)

    params = {'legend.fontsize': legendsize}
    pylab.rcParams.update(params)


def set_minmax(arr,minval=None,maxval=None,bsigma=False):

    if bsigma:
        mean = numpy.mean(arr)
        std = numpy.std(arr)
        minval = mean - minval * std
        maxval = mean + maxval * std
    else:
        if minval==None:
            minval = arr.min()
        if maxval==None:
            maxval = arr.max()

    return minval,maxval

def pol1D(x, a, b):
    return a*x + b


def plot_histogram(list_values ,xmin=None, xmax=None, nbins=100, ylim=None, blog=False, figsize=9, bsave=False, filename="fig_hist.png", title='', xlabel="DN", ylabel="# pixels", color='b', legend_label=None, legend_location='upper center', bfit=False, image2=None, color2='r',legend_label2=None):

    fig = pylab.figure(2,(16/9.*figsize,figsize))

    show_channels = list(range(len(list_values)))

    xmin,xmax = set_minmax(list_values,minval=xmin,maxval=xmax)
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

        arr = list_values[i_channel_group]

        hist, bins = numpy.histogram(arr,bins=nbins,range=(xmin,xmax))
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
        # only show ylabels for pads on the left or xlabel for pads at the bottom
        if i_plot>=n_col_fig*(n_row_fig-1): pylab.xlabel(xlabel)
        if i_plot%n_col_fig==0: pylab.ylabel(ylabel)
        pylab.title('Channel %i'%i_channel_group)
        pylab.grid(True)

    if bsave:
        print("Saving histogram: %s"%filename)
        pylab.savefig(filename)
        pylab.clf()
        pylab.close()
    else:           
        pylab.show()


def plot_image(list_values ,xmin=None, xmax=None, nbins=100, ylim=None, blog=False, figsize=9, bsave=False, filename="fig_hist.png", title='', xlabel="DN", ylabel="# pixels", color='b', legend_label=None, legend_location='upper center', bfit=False, image2=None, color2='r',legend_label2=None):

    fig = pylab.figure(2,(16/9.*figsize,figsize))

    show_channels = list(range(len(list_values)))

    xmin,xmax = set_minmax(list_values,minval=xmin,maxval=xmax)
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

        arr = list_values[i_channel_group]

        hist, bins = numpy.histogram(arr,bins=nbins,range=(xmin,xmax))
        width = bins[1] - bins[0]
        center = (bins[:-1] + bins[1:]) / 2

        #if legend_label==None:
        #    pylab.bar(center, hist, align='center', width=width, log=blog, color=color)
        #else:
        #    pylab.bar(center, hist, align='center', width=width, log=blog, color=color,label=legend_label)
        #pylab.plot(center, hist,color=color)
        image = pylab.imshow(arr,interpolation='nearest')

        norm = matplotlib.colors.Normalize(vmin=4, vmax=12)
        image.set_norm(norm)
        legend = ax.legend(loc=legend_location, shadow=True)

        #pylab.xlim([xmin,xmax])

        #if ylim!=None:
        #    pylab.ylim([ylim[0],ylim[1]])
        #elif ylim==None and blog:
        #    (ymin,ymax) = pylab.ylim()
        #    pylab.ylim([0.1*ymin,ymax])

        pylab.title(title)
        # only show ylabels for pads on the left or xlabel for pads at the bottom
        if i_plot>=n_col_fig*(n_row_fig-1): pylab.xlabel(xlabel)
        if i_plot%n_col_fig==0: pylab.ylabel(ylabel)
        pylab.title('Channel %i'%i_channel_group)
        pylab.grid(True)

        pylab.colorbar()

    if bsave:
        print("Saving histogram: %s"%filename)
        pylab.savefig(filename)
        pylab.clf()
        pylab.close()
    else:           
        pylab.show()


def plot(X, Y, show_channels=None, error=None, xlabel='Xlabel', ylabel='Ylabel', xunit=None, yunit='', title=None, figsize=9, bsave=False, directory_save=None, filename=None, xlim=None, ylim=None, bfit=False, fitrange='all', linewidth=2.5,legend_labels=None,rotation_xlabel=0):

    assert(len(X)==len(Y))
    num_channels = len(X)
    if show_channels==None: show_channels=list(range(num_channels))

    plot = []
    fig = pylab.figure(1,(16/9.*figsize,figsize))
    ax = pylab.subplot(111)

    # plot X as labels if they are not floats
    try:
        x = numpy.array(X).astype(numpy.float)
    except ValueError:
        x = numpy.array([list(range(len(X[0])))]*num_channels)
        pylab.xticks(x[0],X[0])

    y = numpy.array(Y)
    if error!=None:
        error = numpy.array(error)

    if bfit and len(X)>1:
        offset = []
        slope = []
    else:
        offset = None
        slope = None

    for i_channel in show_channels:
        if error==None:
            pl, = pylab.plot(x[i_channel], y[i_channel], color=colors[i_channel], linestyle='solid', linewidth=linewidth, marker='D', markersize=8, markerfacecolor=colors[i_channel])
        else:
            (pl,p2,p3) = pylab.errorbar(x[i_channel], y[i_channel], yerr=error[i_channel], linestyle='solid', linewidth=linewidth, marker='D', markersize=8,color=colors[i_channel])
            
        plot.append(pl)

        # perform fit
        if bfit and len(X)>1:

            if fitrange=='all':
                minfit = x[i_channel][0]
                maxfit = x[i_channel][-1]
            elif fitrange=='best':
                minindex = numpy.argwhere(y[i_channel]>500).min()
                maxindex = numpy.argwhere(y[i_channel]<3500).max()
                minfit = x[i_channel][minindex]
                maxfit = x[i_channel][maxindex]
            elif type(fitrange)==tuple or type(fitrange)==list or type(fitrange)==numpy.ndarray:
                minindex = numpy.argwhere(x[i_channel]>fitrange[0]).min()
                maxindex = numpy.argwhere(x[i_channel]<fitrange[1]).max()
                minfit = x[i_channel][minindex]
                maxfit = x[i_channel][maxindex]

            print("fitrange: %i"%i_channel,fitrange)
            print("fitrange min/max: %i"%i_channel,minfit,maxfit)

            print(x[i_channel])

            try:
                from scipy.optimize import curve_fit
                fit_params = curve_fit(pol1D,x[i_channel][(minfit<=x[i_channel]) & (x[i_channel]<=maxfit)],y[i_channel][(minfit<=x[i_channel]) & (x[i_channel]<=maxfit)])
                offset.append(fit_params[0][1])
                slope.append(fit_params[0][0])
                # to plot fit range and best fit function
                x_pol1D = numpy.array([minfit,maxfit])
                pylab.plot([minfit,minfit],[y[i_channel].min(),y[i_channel].max()],color=colors[i_channel],linestyle='dashed')
                pylab.plot([maxfit,maxfit],[y[i_channel].min(),y[i_channel].max()],color=colors[i_channel],linestyle='dashed')
                y_pol1D = pol1D(x_pol1D,slope[i_channel],offset[i_channel])
                #pylab.plot(x_pol1D,y_pol1D,color=colors[i_channel],linestyle='solid',linewidth=2.5)
            except (TypeError,IndexError):
                print("WARNING: FIT FAILED BECAUSE OF TYPEERROR OR INDEXERROR (in channel %i) for %s vs %s"%(i_channel,ylabel,xlabel))
                pass

    if xlim==None:
        (xmin,xmax) = pylab.xlim()
        dx = xmax-xmin
        pylab.xlim([xmin-0.1*dx,xmax+0.1*dx])
    else:
        pylab.xlim([xlim[0],xlim[1]])
        
    if ylim==None:
        (ymin,ymax) = pylab.ylim()
        dy = ymax-ymin
        pylab.ylim([ymin-0.1*dy,ymax+0.1*dy])
    else:
        pylab.ylim([ylim[0],ylim[1]])
        
    # show legend to the right of the current axis if num_channels>1
    if len(show_channels)>1:
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        leg_labels = []
        for i_channel in show_channels:
            if legend_labels==None:
                leg_labels.append("Channel %i"%i_channel)
            else:
                leg_labels.append(legend_labels[i_channel])
        ax.legend(plot,leg_labels,loc='center left', bbox_to_anchor=(1, 0.5))

    if xunit==None:
        pylab.xlabel(xlabel)
    else:
        pylab.xlabel("%s [%s]"%(xlabel,xunit))

    if yunit==None:
        pylab.ylabel(ylabel)
    else:
        pylab.ylabel("%s [%s]"%(ylabel,yunit))

    locs, labels = pylab.xticks()
    pylab.setp(labels,rotation=rotation_xlabel)

    if title!=None:
        pylab.title(title)

    pylab.grid(True)

    if bsave:
        if filename is not None: 
                filename = os.path.join(directory_save,filename)            
        else:
            if title==None:
                filename = os.path.join(directory_save,"%s_vs_%s.png"%(ylabel,xlabel))
            else:
                filename = os.path.join(directory_save,"%s_vs_%s_%s.png"%(ylabel,xlabel,title))
        pylab.savefig(filename)
        pylab.clf()
        pylab.close()
    else:           
        pylab.show()

    return (offset,slope)


def plot2D(X1, X2, Y, show_channels=None, x1label='X1label', x2label='X2label', ylabel='Ylabel', x1unit=None, x2unit=None, yunit='', title=None, figsize=9, bsave=False, directory_save=None, filename=None, x1lim=None, x2lim=None, ylim=None, legend_labels=None, rotation_xlabel=0,colorscale='jet'):

    for i in range(len(Y)):
        assert(len(X1)*len(X2)==len(Y[i]))

    num_channels = len(Y)
    if show_channels==None: show_channels=list(range(num_channels))

    plot = []
    fig = pylab.figure(1,(16/9.*figsize,figsize))
    #ax = pylab.subplot(111)

    # Set rows and columns of figure:
    if len(show_channels)==1:
        n_row_fig = 1
    else:
        n_row_fig = numpy.ceil(len(show_channels)**0.5)
    n_col_fig = numpy.ceil(float(len(show_channels))/n_row_fig)

    # plot X1/X2 as labels if they are not floats
    try:
        x1 = numpy.array(X1).astype(numpy.float)
    except ValueError:
        #x1 = numpy.array(X1)#.astype(numpy.chararray)
        x1 = numpy.array(list(range(len(X1))))
        #pylab.xticks(x1,X1)

    try:
        x2 = numpy.array(X2).astype(numpy.float)
    except ValueError:
        #x2 = numpy.array(X2)#.astype(numpy.chararray)
        x2 = numpy.array(list(range(len(X2))))
        #pylab.yticks(x2,X2)

    y = numpy.array(Y)

    for i_plot,i_channel in enumerate(show_channels):

        ax = fig.add_subplot(n_row_fig,n_col_fig,i_plot+1)

        #pl, = pylab.plot(x2, y[i_channel], color=colors[i_channel], linestyle='solid', linewidth=2, marker='D', markersize=8, markerfacecolor=colors[i_channel])
        ytemp = y[i_channel].reshape((len(x2),len(x1)))
        dx1 = x1[1]-x1[0]
        dx2 = x2[1]-x2[0]
        #image = pylab.imshow(ytemp,interpolation='nearest',extent=(x1.min()-0.5*dx1,x1.max()+0.5*dx1,x2.max()+0.5*dx2,x2.min()-0.5*dx2))
        image = pylab.imshow(ytemp,interpolation='nearest')
        image.set_cmap(colorscale) # gray/hot/jet
        #plot.append(pl)
        
        pylab.colorbar()

        pos1 = numpy.array(list(range(len(X1))))
        pos2 = numpy.array(list(range(len(X2))))
        #pylab.xticks(x1,x1)
        #pylab.yticks(x2,x2)
        pylab.xticks(x1,X1)
        pylab.yticks(x2,X2)
        #pylab.xticks(pos1,x1)
        #pylab.yticks(pos2,x2)

        
        '''
        if x1lim==None:
            (xmin,xmax) = pylab.xlim()
            dx = xmax-xmin
            pylab.xlim([xmin-0.1*dx,xmax+0.1*dx])
        else:
            pylab.xlim([x1lim[0],x1lim[1]])

        if ylim==None:
            (ymin,ymax) = pylab.ylim()
            dy = ymax-ymin
            pylab.ylim([ymin-0.1*dy,ymax+0.1*dy])
        else:
            pylab.ylim([ylim[0],ylim[1]])

        # show legend to the right of the current axis if num_channels>1
        if len(show_channels)>1:
            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            leg_labels = []
            for i_channel in show_channels:
                if legend_labels==None:
                    leg_labels.append("Channel %i"%i_channel)
                else:
                    leg_labels.append(legend_labels[i_channel])
            ax.legend(plot,leg_labels,loc='center left', bbox_to_anchor=(1, 0.5))
        '''

        if x1unit==None:
            pylab.xlabel(x1label)
        else:
            pylab.xlabel("%s [%s]"%(x1label,x1unit))

        if x2unit==None:
            pylab.ylabel(x2label)
        else:
            pylab.ylabel("%s [%s]"%(x2label,x2unit))

        #if yunit==None:
        #    pylab.title(ylabel)
        #else:
        #    pylab.title("%s [%s]"%(ylabel,yunit))

        locs, labels = pylab.xticks()
        pylab.setp(labels,rotation=rotation_xlabel)

        if title!=None:
            pylab.title(title)

        #pylab.grid(True)

    if bsave:
        if filename is not None: 
                filename = os.path.join(directory_save,filename)            
        else:
            if title==None:
                filename = os.path.join(directory_save,"%s_vs_%s_%s.png"%(ylabel,x1label,x2label))
            else:
                filename = os.path.join(directory_save,"%s_vs_%s_%s_%s.png"%(ylabel,x1label,x2label,title))
        pylab.savefig(filename)
        pylab.clf()
        pylab.close()
    else:           
        pylab.show()


def plot_scatter(X,Y,figsize=9, xlabel='xlabel', xunit=None, ylabel='ylabel', yunit='uV/DN', bsave=False, directory_save=None):

    assert(len(Y)==len(X))
    
    fig_vscolchannel = pylab.figure(1,(16/9.*figsize,figsize))
    pylab.scatter(X, Y, s=200, c='red' ,alpha=0.8)

    if xunit==None:
        pylab.xlabel('%s'%(xlabel))
    else:
        pylab.xlabel('%s [%s]'%(xlabel,xunit))

    if yunit==None:
        pylab.ylabel('%s'%(ylabel))
    else:
        pylab.ylabel('%s [%s]'%(ylabel,yunit))

    pylab.grid(True)

    if bsave:
        filename = os.path.join(directory_save,"%s_vs_%s.png"%(ylabel,xlabel))
        pylab.savefig(filename)
        pylab.clf()
        pylab.close()
    else:           
        pylab.show()

if __name__=='__main__':

    mu = 3
    sigma = 2
    s = numpy.random.normal(mu,sigma,1000)
