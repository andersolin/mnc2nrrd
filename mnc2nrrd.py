#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 12:24:12 2019

@author: andersolin
"""
# % Import stuff
import nrrd
import os
import pyminc.volumes.factory as pyminc
import numpy as np
import matplotlib.pyplot as plt
import argparse

def get_nhdr_info(filename):
    infile = pyminc.volumeFromFile(filename) # mincreshape -dimorder time,xspace,yspace,zspace dyn.mnc dyn_reorder.mnc -clobber
    img = np.array(infile.data)
    infile.closeVolume()
    #b = b.flatten('F').reshape(20,192,192,35)
    header = {}
    header['type']=infile.dtype
    header['dimension']= infile.ndims
    header['space'] = 'right-anterior-superior' # Hardcoded!!
    header['sizes'] =np.array(infile.data.shape)
    header['endian']='little'
    header['encoding']='gzip' 
    header['measurement frame'] = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
    if infile.ndims==4:
        header['space directions']=np.array([[np.nan, np.nan, np.nan],
                                        [infile.separations[1], 0, 0],
                                        [0, infile.separations[2], 0],
                                        [0, 0, infile.separations[3]]])
        header['kinds']=['list', 'domain', 'domain', 'domain']
        header['space origin']=np.array([infile.starts[1], 
                                    infile.starts[2], 
                                    infile.starts[3]])
        TE = str(float(os.popen('mincinfo -attvalue acquisition:echo_time ' + filename + ' -error_string noTE').read().rstrip())*1000)
        header['MultiVolume.DICOM.EchoTime']=TE
        flip = str(float(os.popen('mincinfo -attvalue acquisition:flip_angle ' + filename + ' -error_string noKVP').read().rstrip()))
        header['MultiVolume.DICOM.FlipAngle']=flip
        TR = str(float(os.popen('mincinfo -attvalue acquisition:repetition_time ' + filename + ' -error_string noKVP').read().rstrip())*1000)
        header['MultiVolume.DICOM.RepetitionTime']=TR
        header['MultiVolume.FrameIdentifyingDICOMTagName']='AcquisitionTime'
        header['MultiVolume.FrameIdentifyingDICOMTagUnits']='ms'
        header['MultiVolume.FrameLabels']= '0.0,7585.0,15167.5,22750.0,30332.5,37917.5,45500.0,53082.5,60665.0,68250.0,75832.5,83415.0,90997.5,98582.5,106165.0,113747.5,121330.0,128915.0,136497.5,144080.0,151662.5,159247.5,166830.0,174412.5,181995.0,189580.0,197162.5,204745.0,212327.5,219912.5,227495.0,235077.5,242660.0,250245.0,257827.5'
        header['MultiVolume.NumberOfFrames'] = '35'
    if infile.ndims==3:
        header['space directions']=np.array([[infile.separations[0], 0, 0],
                                        [0, infile.separations[1], 0],
                                        [0, 0, infile.separations[2]]])
        header['kinds']=['domain', 'domain', 'domain']
        header['space origin']=np.array([infile.starts[0], 
                                    infile.starts[1], 
                                    infile.starts[2]])
    return img, header
    
    
    
    
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='covert mnc to nrrd')
    parser.add_argument("in_mnc", help="Minc file input", type=str)
    parser.add_argument("out_nrrd", help="Nrrd file output", type=str)
    args = parser.parse_args()

    img, header = get_nhdr_info(args.in_mnc)
    header['data file'] = args.out_nrrd
    nrrd.write(args.out_nrrd, img, header=header, detached_header=True)
