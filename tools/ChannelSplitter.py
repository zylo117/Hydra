#! /usr/bin/env python 

__author__ = "Aurelien Bouvier"
__email__ = "aurelien.bouvier@gmail.com"

import os, sys
import glob
import numpy as np
from optparse import OptionParser

import Image

def raw2ascii(rawfilename,asciifilename,separator,datatype):
    
    print("Converting RAW file: %s"%rawfilename)
    print("To ASCII file: %s"%asciifilename)
    print("SEPARATOR: %c"%separator)
    
    array = np.fromfile(rawfilename,dtype=datatype)
    
    print("Image size: ",array.size)
    if array.size != shape[0]*shape[1]:
        raise Exception("Array dimensions do not match size of RAW data. Verify that you have the correct data type (dtype) and image size (rows,columns)")
    
    array = array.reshape(shape)
    
    fascii = open(asciifilename,'w')
    
    fascii.write("ROW%sCOLUMN%sVALUE\n"%(separator,separator))
    
    for (x,y),value in np.ndenumerate(array):
        
        pixel_num = x*shape[1] + y
        if opts.verbose and pixel_num%100000==0: print(pixel_num)
        fascii.write("%i%s%i%s%.1f\n"%(x,separator,y,separator,value))
    
    fascii.close()
    
    
def raw2csv(rawfilename,csvfilename):
    
    raw2ascii(rawfilename,csvfilename,',',datatype)


def split_channel(rawfilename,outfilename,channel_groups):

    im = Image.Image(rawfilename,rows=opts.rows,columns=opts.columns,datatype=opts.dtype,channel_groups=channel_groups)

    im_channelsplit = Image.Image(im.get_array(bstack=True))
    outname = os.path.splitext(outfilename)[0]+"_allchannels.raw"
    im_channelsplit.save2raw(filename=outname)

    if opts.singlechannels:

        num_channels = channel_groups[0]*channel_groups[1]

        for i_channel_group in range(num_channels):
            
            im_channel = Image.Image(im.get_array(i_channel_group=i_channel_group))
            outname = os.path.splitext(outfilename)[0]+"_channel%i.raw"%i_channel_group
            im_channel.save2raw(filename=outname)


if __name__ == '__main__':

    usage = "Usage: python ChannelSplitter.py [options] <files>"
    
    parser = OptionParser(usage=usage)
    parser.add_option('-o','--output', default=None, type='string', help='output file name')
    parser.add_option('--channel_groups', default="1x8", type='string', help='channel groups for splitting. Syntax: (row)x(column)')
    parser.add_option('--dtype', default='uint16', type='string', help='Data type to be used: unsigned 16-bits integer (little endian) = \"uint16\" (or \"<u2\"), unsigned 16-bits integer (big endian) = \">u2\", 32-bits float (big endian) = \">f\"')
    parser.add_option('-v', '--verbose', action='store_true', default=False, help='Verbose mode')
    parser.add_option('--rows', default=3000, type='int', help='Number of rows')
    parser.add_option('--columns', default=4000, type='int', help='number of columns')
    parser.add_option('--singlechannels', action='store_true', default=False, help='Save single channel raw file')

    (opts, args) = parser.parse_args()

    if len(args)==0: 
        print("No RAW input files were specified. Please add at least one as argument if you would like to split your RAW files into different channels")
        print(usage)
        sys.exit(0)

    files = []
    for raw_wildcard in args:
        for file in glob.glob(raw_wildcard):
            files.append(file)

    print("\nNUMBER OF FILES: %i\n"%len(files))
    print("\nDATA TYPE: %s"%opts.dtype)
    print("ROWS: %i"%opts.rows)
    print("COLUMNS: %i"%opts.columns)

    shape = (opts.rows,opts.columns)
    
    datatype=opts.dtype
    #datatype='>f' # Big Endian
    
    # Parse channel groups from command line option
    row_group = int(opts.channel_groups.split('x')[0])
    column_group = int(opts.channel_groups.split('x')[1])
    channel_groups = (row_group,column_group)
        
    for rawfilename in files:

        if opts.output == None:
            outfilename = os.path.splitext(rawfilename)[0]+"_channelsplit.raw"
        else:
            outfilename = opts.output

        #raw2csv(rawfilename,csvfilename)
        split_channel(rawfilename,outfilename,channel_groups)
        
    print("\nFINISHED!")
    
 
