import math
import numpy
from PIL import Image
import os
import numba
from field import field

class fractal:
    @numba.jit
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, imagesize):
        self.colormap=numpy.zeros((256,3),dtype=numpy.uint8)
        self.shape=numpy.zeros((imagesize,imagesize,imagesize,3),dtype=numpy.uint8)
        for c in range(256):
            self.colormap[c][0]=c*15%255
            self.colormap[c][1]=c*22%255
            self.colormap[c][2]=c*9%255
        for xpix in range(imagesize):
            x=xmin+xpix*(xmax-xmin)/imagesize
            for ypix in range(imagesize):
                y=ymin+ypix*(ymax-ymin)/imagesize
                for zpix in range(imagesize):
                    z=zmin+zpix*(zmax-zmin)/imagesize
                    c=field(x,y,z)
                    zz=field(0,0,0)
                    count=0
                    while (count<50) and (zz.magsq()<10000):
                        zz=(zz*zz)+c
                        count=count+1
                    if count<50:
                        self.shape[xpix][ypix][zpix][0]=self.colormap[count][0]
                        self.shape[xpix][ypix][zpix][1]=self.colormap[count][1]
                        self.shape[xpix][ypix][zpix][2]=self.colormap[count][2]
                        self.xmin=xmin
                        self.xmax=xmax
                        self.ymin=ymin
                        self.ymax=ymax
                        self.zmin=zmin
                        self.zmax=zmax
                        self.imagesize=imagesize

    def render(self):
        dir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(self.imagesize)
        os.makedirs(dir,exist_ok=True)
        for xpix in range(self.imagesize):
            rawslice=self.shape[xpix,:,:,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(dir+"\XFrame"+str(xpix)+".gif")
        for ypix in range(self.imagesize):
            rawslice=self.shape[:,ypix,:,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(dir+"\YFrame"+str(ypix)+".gif")
        for zpix in range(self.imagesize):
            rawslice=self.shape[:,:,zpix,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(dir+"\ZFrame"+str(zpix)+".gif")
