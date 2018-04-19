#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os, sys
import glob
import numpy as np
from optparse import OptionParser

from . import Image

def split_channel(image,prefix_out,channel_groups):

    im_channelsplit = image.get_image_channelsplit()
    outname = prefix_out+"_channelsplit_allchannels.raw"
    im_channelsplit.save2raw(filename=outname)

    if opts.single_channels:

        num_channels = channel_groups[0]*channel_groups[1]

        for i_channel_group in range(num_channels):
            
            im_channel = image.get_image_channel(i_channel_group)
            outname = prefix_out+"_channelsplit_channel%i.raw"%i_channel_group
            im_channel.save2raw(filename=outname)


if __name__ == '__main__':

    usage = "Usage: python hydra.py [options] <files>"
    
    parser = OptionParser(usage=usage)
    parser.add_option('-g','--channel_groups', default="1x1", type='string', help='channel groups for splitting. Syntax: (row)x(column)')
    parser.add_option('--dtype', default='uint16', type='string', help='Data type to be used: unsigned 16-bits integer (little endian) = \"uint16\" (or \"<u2\"), unsigned 16-bits integer (big endian) = \">u2\", 32-bits float (big endian) = \">f\"')
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Verbose mode')
    parser.add_option('--rows', default=3000, type='int', help='Number of rows')
    parser.add_option('--columns', default=4000, type='int', help='number of columns')
    parser.add_option('--column_swap', action='store_true', default=False, help='Save RAW file with channel split')
    parser.add_option('-d','--dark', default=None, type='string', help='Performs dark subtraction using the RAW file provided as dark frame')
    parser.add_option('--rtn', action='store_true', default=False, help='Performs RTN correction using columns specified by rtn_cols')
    parser.add_option('--rtn_cols', default="4,67", type='string', help='Columns to use for RTN correction')
    parser.add_option('--fpn', action='store_true', default=False, help='Performs RTN correction using rows specified by fpn_rows')
    parser.add_option('--fpn_rows', default="0,63", type='string', help='Rows to use for FPN correction')
    parser.add_option('--plot_image', action='store_true', default=False, help='Save 2D image in png format')
    parser.add_option('--fullresolution', action='store_true', default=False, help='Save image in full resolution')
    parser.add_option('--plot_histogram', action='store_true', default=False, help='Save histogram in png format')
    parser.add_option('--plot_row_profile', action='store_true', default=False, help='Save row profile in png format')
    parser.add_option('--plot_column_profile', action='store_true', default=False, help='Save column profile in png format')
    parser.add_option('--csv', action='store_true', default=False, help='Save image in CSV format')
    parser.add_option('--channel_split', action='store_true', default=False, help='Save RAW file with channel split')
    parser.add_option('--single_channels', action='store_true', default=False, help='Save single channel RAW file')
    parser.add_option('--suffix', default="postprocessed", type='string', help='Suffix to add to output file')
    parser.add_option('--view', action='store_true', default=False, help='only view plots if set to True')

    (opts, args) = parser.parse_args()

    if len(args)==0: 
        print("No RAW input files were specified. Please add at least one file to process")
        print(usage)
        sys.exit(0)

    files = []
    for raw_wildcard in args:
        for file in glob.glob(raw_wildcard):
            files.append(file)

    print("\nNUMBER OF FILES: %i\n"%len(files))
    print("DATA TYPE: %s"%opts.dtype)
    print("ROWS: %i"%opts.rows)
    print("COLUMNS: %i"%opts.columns)

    datatype=opts.dtype
    #datatype='>f' # Big Endian
    
    # Parse channel groups from command line option
    row_group = int(opts.channel_groups.split('x')[0])
    column_group = int(opts.channel_groups.split('x')[1])
    channel_groups = (row_group,column_group)
    if row_group*column_group>1: bstack=True

    bsave = not(opts.view)

    print("CHANNEL GROUPS:",channel_groups)

    # Parse RTN columns to use
    if opts.rtn:
        rtn_colstart = int(opts.rtn_cols.split(',')[0])
        rtn_colstop = int(opts.rtn_cols.split(',')[1])
    # Parse FPN rows to use
    if opts.fpn:
        fpn_rowstart = int(opts.fpn_rows.split(',')[0])
        fpn_rowstop = int(opts.fpn_rows.split(',')[1])
        
    for rawfilename in files:

        im = Image.Image(rawfilename,rows=opts.rows,columns=opts.columns,datatype=opts.dtype,channel_groups=channel_groups)

        # Dark subtraction
        if opts.dark!=None:
            print("\nApplying dark subtraction using following dark file: %s"%opts.dark)
            print("Warning: output RAW file will be save with following encoding: 32-bit float, little endian")
            im_dark = Image.Image(opts.dark,rows=opts.rows,columns=opts.columns,datatype=opts.dtype)
            im.subtract(im_dark)

        # Column swapping
        if opts.column_swap:
            im.column_swap()

        # RTN correction
        if opts.rtn:
            im.RTN_correction(colstart=rtn_colstart,colstop=rtn_colstop)

        # FPN correction
        if opts.fpn:
            im.FPN_correction(rowstart=fpn_rowstart,rowstop=fpn_rowstop)

        
        prefix_out = os.path.splitext(rawfilename)[0] + "_" + opts.suffix

        # Save image/histogram png file
        if opts.plot_image:
            outname = prefix_out+"_image.png"
            im.plot_image(bstack=bstack,bsave=bsave,filename=outname,bfullresolution=opts.fullresolution)
        if opts.plot_histogram:
            outname = prefix_out+"_hist.png"
            im.plot_histogram(bsave=bsave,filename=outname)
        if opts.plot_row_profile:
            outname = prefix_out+"_row_profile.png"
            im.plot_row_profile(bsave=bsave,filename=outname)
        if opts.plot_column_profile:
            outname = prefix_out+"_column_profile.png"
            im.plot_column_profile(bsave=bsave,filename=outname)
            #im.plot_column_profile(ylim=[700,2100],bsave=bsave,filename=outname)
            #im.plot_column_profile(xlim=[0,200],ylim=[-700,700],show_channels=range(4),bsave=bsave,filename=outname)
            #im.plot_column_profile(ylim=[-700,700],show_channels=range(4),bsave=bsave,filename=outname)
            #im.plot_column_profile(ylim=[-200,200],show_channels=range(4,8),bsave=bsave,filename=outname)
            #im.plot_column_profile(xlim=[0,200],ylim=[-200,200],show_channels=range(4,8),bsave=bsave,filename=outname)

        # Save post-processed file
        outname = prefix_out+".raw"
        im.save2raw(filename=outname)

        # Save CSV file
        if opts.csv:
            im.save2csv(prefix_out+'.csv',bverbose=True)

        # Save channel splitted file
        if opts.channel_split:
            split_channel(im,prefix_out,channel_groups)
        
    print("\nImage post-processing successfully completed!")
    
 
