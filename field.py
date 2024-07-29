import math
import numpy
import os
from tkinter import *
import _tkinter
from PIL import Image


class field:
    def __init__ (self,finite, infinitessimal, infinite):
        self.r=finite
        self.p=infinitessimal
        self.m=infinite

    def __add__ (self,o):
        return field(self.r+o.r, self.p+o.p, self.m+o.m)
    
    def __mul__ (self,o):
        re=(self.r*o.r)+(self.p*o.m)+(self.m*o.p)
        ep=(self.r*o.p)+(self.p*o.r)
        om=(self.m*o.r)+(self.m*o.m)+(self.r*o.m)
        return field(re,ep,om)
    
    def __repr__ (self):
        return(str(self.r)+" "+str(self.p)+"p "+str(self.m)+"m")
    
    def mag (self):
        return math.sqrt(self.r*self.r+self.p*self.p+self.m*self.m)
    
    def magsq (self):
        return self.r*self.r+self.p*self.p+self.m*self.m


