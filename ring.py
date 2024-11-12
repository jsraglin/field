import math
import numpy
import os
from tkinter import *
import _tkinter
from PIL import Image

class ring():
##################################################################
# General class for representing 3-value mathematical rings      #
# Initially created for the triel class, i+ j*epsilon+ k*omega   #
# Where epsilon in infinitessimal and omega is infinite, both    #
# treated niavely, then expanded into other variants             #
# So far multiplication is virtual as the thing being varied over#
# And addition is only virtual to return the correct type        #
##################################################################

    def __init__ (self,finite, infinitessimal, infinite):
        self.r=finite
        self.p=infinitessimal
        self.m=infinite
        
    def __repr__ (self):
        return(str(self.r)+" "+str(self.p)+"p "+str(self.m)+"m")
    
    def mag (self):
        return math.sqrt(self.r*self.r+self.p*self.p+self.m*self.m)
    
    def magsq (self):
        return self.r*self.r+self.p*self.p+self.m*self.m
    
    def polar (self):
        r=self.mag()
        theta=numpy.arctan2(self.p,self.r)
        phi=numpy.arctan2(numpy.sqrt(self.r*self.r+self.p*self.p),self.m)
        return (r,theta,phi)


class triel(ring):
# Basic triel numbers, extending the dual numbers by adding an infinite term.
# epsilon*epsilon is 0, as with dual numbers.  omega*omega is omega
# epsilon*omega and omega*epsilon are 1
# Fractal structure is present, but is mostly planar along a skew plane
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return triel(self.r+o.r, self.p+o.p, self.m+o.m)
        
    def __mul__ (self,o):
        re=(self.r*o.r)+(self.p*o.m)+(self.m*o.p)
        ep=(self.r*o.p)+(self.p*o.r)
        om=(self.m*o.r)+(self.m*o.m)+(self.r*o.m)
        return triel(re,ep,om)

class atriel(ring):
# variant on the triels, the one change is that omega*omega is -omega,
# again naively/arbitrarily modelling asymptotic behavior.
# Simialr to the triels for fractal-ness
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return atriel(self.r+o.r, self.p+o.p, self.m+o.m)
    
    def __mul__ (self,o):
        re=(self.r*o.r)+(self.p*o.m)+(self.m*o.p)
        ep=(self.r*o.p)+(self.p*o.r)
        om=(self.m*o.r)-(self.m*o.m)+(self.r*o.m)
        return atriel(re,ep,om)
    
class braid(ring):
# Moving to other ring structures, this is a simple braided one where
# i*i=-j, j*j=-k, k*k=-i, ij=ji=km jk=kj=i, ki=ik=j
# Still investigating
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return braid(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=-(self.m*o.m)+(self.p*o.m)+(self.m*o.p)
        ep=-(self.r*o.r)+(self.r*o.m)+(self.m*self.r)
        om=-(self.p*o.p)+(self.r*o.p)+(self.p*o.r)
        return braid(re,ep,om)
    
class abraid(ring):
# Variant of the braid, inverting the signs of each product.
# promising shapes
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return abraid(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=(self.m*o.m)-(self.p*o.m)-(self.m*o.p)
        ep=(self.r*o.r)-(self.r*o.m)-(self.m*self.r)
        om=(self.p*o.p)-(self.r*o.p)-(self.p*o.r)
        return abraid(re,ep,om)

class chaos(ring):
# A mostly random set of multiplcation values.  There are 9 products
# in each of these types of ring, and seven possible values for each one
# (+/- i,j,k and 0)  Obviously even more chaos could be added by adding
# scaling factors as well.
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return chaos(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=self.r*o.m+self.p*o.m-self.p*o.p
        ep=-self.p*o.r+self.m*o.m
        om=self.r*o.p-self.r*o.r-self.m*o.p
        return chaos(re,ep,om)

class cbraid(ring):
# Another braid variant, this one using positive values for the
# squares and having the other products produce different signs
# in different orders.  Not great fractals here but the julias show
# some deep structure. More interesting in the z*3 areas.

    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return cbraid(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=(self.m*o.m)+(self.p*o.m)-(self.m*o.p)
        ep=(self.r*o.r)-(self.r*o.m)+(self.m*self.r)
        om=(self.p*o.p)+(self.r*o.p)-(self.p*o.r)
        return cbraid(re,ep,om)

class dbraid(ring):
# cbraid, but the squares are changed with one positive, one negative, one zero
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return dbraid(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=(self.m*o.m)+(self.p*o.m)-(self.m*o.p)
        ep=-(self.r*o.r)-(self.r*o.m)+(self.m*self.r)
        om=+(self.r*o.p)-(self.p*o.r)
        return dbraid(re,ep,om)

class anarch(ring):
# An even random set of multiplcation values.  with scaling
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return anarch(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        om=0.8*self.m*o.m-1.1*self.p*o.r-0.8*self.p*o.p
        ep=2*math.pi*math.sin(self.m*o.r)-0.7*self.r*o.m
        re=self.r*o.p-1.2*self.r*o.r-0.2*self.p*o.m
        return anarch(re,ep,om)

class zbraid(ring):
# braid with all three squared terms trif functionized
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return zbraid(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=(self.m*o.m)-math.pi*math.sin(self.p*o.m)-math.pi*math.sin(self.m+o.p)
        ep=-(self.r*o.r)+math.pi*math.sin(self.r*o.m)+math.pi*math.sin(self.m+self.r)
        om=0*(self.p*o.p)-math.pi*math.sin(self.r*o.p)+math.pi*math.sin(self.p+o.r)
        return zbraid(re,ep,om)

class flatq(ring):
# Flat quaternion with the fourth component hidden
    def __init__ (self, finite, infinitessimal, infinite, q=0.0):
        self.q=q
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return flatq(self.r+o.r, self.p+o.p, self.m+o.m, self.q+o.q)

    def __mul__ (self,o):
        re=(self.r*o.r)-(self.p*self.p)-(self.m*self.m)-(self.q*self.q)
        ep=(self.r*o.p)+(self.p*o.r)+(self.m*o.q)-(self.q*o.m)
        om=(self.r*o.m)+(self.m*o.r)-(self.p*o.q)+(self.q*o.p)
        qq=(self.r*o.q)+(self.q*o.r)+(self.p*o.m)-(self.m*o.p)
        return flatq(re,ep,om,qq)

class bulb3(ring):
# Mandelbulb cubic, multiplaction is wonky here because it's assuming
# self and o are identical, which they will be in z*z at least.
# may behave wonkily in the other itertypes
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return bulb3(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=self.r*self.r*self.r-3*self.r*(self.p*self.p+self.m*self.m)
        ep=-1*(self.p*self.p*self.p)+3*self.p*self.r*self.r-self.p*self.m*self.m
        om=self.m*self.m*self.m-3*self.m*self.r*self.r+self.m*self.p*self.p
        return bulb3(re,ep,om)

class cbulb3(ring):
# Mandelbulb variation class, still assuming self and o identical
# self and o are identical, which they will be in z*z at least.
# may behave wonkily in the other itertypes]#
# first go: sines in some places
    def __init__ (self, finite, infinitessimal, infinite):
        super().__init__(finite,infinitessimal,infinite)

    def __add__ (self,o):
        return cbulb3(self.r+o.r, self.p+o.p, self.m+o.m)

    def __mul__ (self,o):
        re=self.r*self.r*self.r-3*self.r*(math.sin(self.r)*math.pi)*(self.p*self.p+self.m*self.m)
        ep=-1*(self.p*self.p*self.p)+3*self.p*(math.cos(self.p)*math.pi)*(self.r*self.r-self.m*self.m)
        om=self.m*self.m*self.m-3*self.m*(math.sin(self.m)*math.pi)*(self.r*self.r+self.p*self.p)
        return cbulb3(re,ep,om)
