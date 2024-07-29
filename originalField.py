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
imagesize=100
shape=numpy.zeros((imagesize,imagesize,imagesize,3),dtype=numpy.uint8)
appMap=dict()
#z=field(0.1,0.2,0.3)
#c=field(-0.2,-0.375,0.11)
count=0
xmin=-1.5
xmax=1.5
ymin=-1.5
ymax=1.5
zmin=-1.5
zmax=1.5
step=0.05
colormap=numpy.zeros((256,3),dtype=numpy.uint8)
for c in range(256):
    colormap[c][0]=c*15%255
    colormap[c][1]=c*22%255
    colormap[c][2]=c*9%255
dir="shape"+str(xmin)+str(xmax)+str(ymin)+str(ymax)+str(zmin)+str(zmax)+str(imagesize)
os.makedirs(dir,exist_ok=True)
for xpix in range(imagesize):
    x=xmin+xpix*(xmax-xmin)/imagesize
    print(xpix)
#    print(x)
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
#                if xpix==50 and ypix==99 and zpix==99:
#                    print(zz)
            if count<50:
                shape[xpix][ypix][zpix][0]=colormap[count][0]
                shape[xpix][ypix][zpix][1]=colormap[count][1]
                shape[xpix][ypix][zpix][2]=colormap[count][2]

for xpix in range(imagesize):
    rawslice=shape[xpix,:,:,:]
    slice=Image.fromarray(rawslice,mode="RGB")
#     slice=Image.fromarray(shape[xpix],mode="L")
    slice.save(dir+"\XFrame"+str(xpix)+".gif")
for ypix in range(imagesize):
    rawslice=shape[:,ypix,:,:]
    slice=Image.fromarray(rawslice,mode="RGB")
#     slice=Image.fromarray(shape[xpix],mode="L")
    slice.save(dir+"\YFrame"+str(ypix)+".gif")
for zpix in range(imagesize):
    rawslice=shape[:,:,zpix,:]
    slice=Image.fromarray(rawslice,mode="RGB")
#     slice=Image.fromarray(shape[xpix],mode="L")
    slice.save(dir+"\ZFrame"+str(zpix)+".gif")
xfr=imagesize//2
yfr=imagesize//2
zfr=imagesize//2
app=Tk()
cxf=Frame(app)
cxf.grid(row=1,column=1)
cx=Canvas(cxf,height=imagesize,width=imagesize)
cx.pack()
xlabeltext=StringVar()
xlabeltext.set("Frame# "+str(xfr)+ "X="+str(xmin+xfr*(xmax-xmin)/imagesize))
cxlabel=Label(cxf,textvariable=xlabeltext)
cxlabel.pack()
xim=PhotoImage(file=(dir+"\XFrame"+str(xfr)+".gif"))
conx=cx.create_image(0,0,image=xim,anchor=NW)
appMap['conx']=conx
cyf=Frame(app)
cyf.grid(row=1,column=2)
cy=Canvas(cyf,height=imagesize,width=imagesize)
cy.pack()
ylabeltext=StringVar()
ylabeltext.set("Frame# "+str(yfr)+ "Y="+str(ymin+yfr*(ymax-ymin)/imagesize))
cylabel=Label(cxf,textvariable=ylabeltext)
cylabel.pack()
yim=PhotoImage(file=(dir+"\YFrame"+str(yfr)+".gif"))
#yim=PhotoImage(file=(dir+"\YFrame50.gif"))
cony=cy.create_image(0,0,image=yim,anchor=NW)
appMap['cony']=cony
czf=Frame(app)
czf.grid(row=2,column=1)
cz=Canvas(czf,height=imagesize,width=imagesize)
cz.pack()
zlabeltext=StringVar()
zlabeltext.set("Frame# "+str(zfr)+ "Z="+str(zmin+zfr*(zmax-zmin)/imagesize))
czlabel=Label(czf,textvariable=zlabeltext)
czlabel.pack()
zim=PhotoImage(file=(dir+"\ZFrame"+str(zfr)+".gif"))
#zim=PhotoImage(file=(dir+"\ZFrame50.gif"))
conz=cz.create_image(0,0,image=zim,anchor=NW)
appMap['conz']=conz
fr22=Frame(app)
fr22.grid(row=2,column=2)
boxXFrame=Text(fr22,height=1,width=5)
boxYFrame=Text(fr22,height=1,width=5)
boxZFrame=Text(fr22,height=1,width=5)

def update_frames():
    xfr=int(boxXFrame.get("1.0", 'end-1c'))
    yfr=int(boxYFrame.get("1.0", 'end-1c'))
    zfr=int(boxZFrame.get("1.0", 'end-1c'))
    xim=PhotoImage(file=(dir+"\XFrame"+str(xfr)+".gif"))
#    cx.delete(appMap['conx'])
    conx=cx.create_image(0,0,image=xim,anchor=NW)
    appMap['conx']=conx
    cx.imgref=xim
 #   cx.create_image(imagesize,imagesize,image=xim)
 #   cx.itemconfig(conx,xim)
 #   cx.update_idletasks()
    yim=PhotoImage(file=(dir+"\YFrame"+str(yfr)+".gif"))
#    cy.delete(appMap['cony'])
    cony=cy.create_image(0,0,image=yim,anchor=NW)
    appMap['cony']=cony
    cy.imgref=yim
#    cy.create_image(imagesize,imagesize,image=yim)
#    cy.itemconfig(cony,yim)
#    cy.update_idletasks()
    zim=PhotoImage(file=(dir+"\ZFrame"+str(zfr)+".gif"))
#    cz.delete(appMap['conz'])
    conz=cz.create_image(0,0,image=zim,anchor=NW)
    appMap['conz']=conz
    cz.imgref=zim
#    cz.create_image(imagesize,imagesize,image=zim)
    app.update_idletasks()


refreshButton=Button(fr22,text="Refresh",command=update_frames)
boxXFrame.pack()
boxYFrame.pack()
boxZFrame.pack()
refreshButton.pack()
fr22.grid(row=2,column=2)
app.mainloop()
#x=xmin
#y=ymin
#z=zmin
#while (x<xmax):
#    y=ymin
#    while (y<ymax):
#        z=zmin
#        while (z<zmax):
#            c=field(x,y,z)
#            zz=field(0,0,0)
#            count=0
#            while (count<100) and (zz.mag()<100):
#                zz=zz*zz+c
#                print(z)
#                count+=1
#            if count==100:
#                print ("*",end='')
#            elif count>80:
#                print("^",end='')
#            elif count>50:
#                print("%",end='')
#            elif count>30:
#                print('$',end='')
#            else:
#                print("o",end='')
#            z=z+step
#        print("")
#        y=y+step
#    print("--------------------------------")
#    x=x+step



