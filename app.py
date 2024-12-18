######################################################################
# Imports                                                            #
######################################################################
import math
import colorsys
import numpy
import os
from tkinter import *
import _tkinter
from PIL import ImageTk, Image
from ring import triel, atriel, braid, abraid, chaos, cbraid, dbraid, anarch, zbraid, flatq, bulb3, cbulb3
import multiprocessing
from functools import partial
import shutil

class fractal:
#####################################
# Methods                           #
#####################################
    @staticmethod
    def calcPlane(x, ymin, ymax, zmin, zmax, imagesize,colormap,ringtype,itertype,julia=False,jx=0.0,jy=0.0,jz=0.0,):
        plane=numpy.zeros((imagesize, imagesize, 3),dtype=numpy.uint8)
        for ypix in range(imagesize):
            y=ymin+ypix*(ymax-ymin)/(imagesize-1)
            for zpix in range(imagesize):
                z=zmin+zpix*(zmax-zmin)/(imagesize-1)
                if julia:
                    match ringtype:
                        case "triel":
                            c=triel(jx,jy,jz)
                            zz=triel(x,y,z)
                        case "atriel":
                            c=atriel(jx,jy,jz)
                            zz=atriel(x,y,z)
                        case "braid":
                            c=braid(jx,jy,jz)
                            zz=braid(x,y,z)
                        case "abraid":
                            c=abraid(jx,jy,jz)
                            zz=abraid(x,y,z)
                        case "chaos":
                            c=chaos(jx,jy,jz)
                            zz=chaos(x,y,z)
                        case "cbraid":
                            c=cbraid(jx,jy.jz)
                            zz=cbraid(x,y,z)
                        case "dbraid":
                            c=dbraid(jx,jy.jz)
                            zz=dbraid(x,y,z)
                        case "anarch":
                            c=anarch(jx,jy.jz)
                            zz=anarch(x,y,z)
                        case "zbraid":
                            c=zbraid(jx,jy,jz)
                            zz=zbraid(x,y,z)
                        case "flatq":
                            c=flatq(jx,jy,jz)
                            zz=flatq(x,y,z)
                        case "bulb3":
                            c=bulb3(jx,jy,jz)
                            zz=bulb3(x,y,z)
                        case "cbulb3":
                            c=cbulb3(jx,jy,jz)
                            zz=cbulb3(x,y,z)
                        case _:
                            c=triel(jx,jy,jz)
                            zz=triel(x,y,z)
                else:
                    match ringtype:
                        case "triel":
                            c=triel(x,y,z)
                            zz=triel(0,0,0)
                        case "atriel":
                            c=atriel(x,y,z)
                            zz=atriel(0,0,0)
                        case "braid":
                            c=braid(x,y,z)
                            zz=braid(0,0,0)
                        case "abraid":
                            c=abraid(x,y,z)
                            zz=abraid(0,0,0)
                        case "chaos":
                            c=chaos(x,y,z)
                            zz=chaos(0,0,0)
                        case "cbraid":
                            c=cbraid(x,y,z)
                            zz=cbraid(0,0,0)
                        case "dbraid":
                            c=dbraid(x,y,z)
                            zz=dbraid(0,0,0)
                        case "anarch":
                            c=anarch(x,y,z)
                            zz=anarch(0,0,0)
                        case "zbraid":
                            c=zbraid(x,y,z)
                            zz=zbraid(0,0,0)
                        case "flatq":
                            c=flatq(x,y,z)
                            zz=flatq(0,0,0)
                        case "bulb3":
                            c=bulb3(x,y,z)
                            zz=bulb3(0,0,0)
                        case "cbulb3":
                            c=cbulb3(x,y,z)
                            zz=cbulb3(0,0,0)
                        case _:
                            c=triel(x,y,z)
                            zz=triel(0,0,0)
                count=0
                match itertype:
                    case "z*z":
                        iterate=lambda z,c:z*z+c
                    case "z*(z*z)":
                        iterate=lambda z,c:z*(z*z)+c
                    case "(z*z)*z":
                        iterate=lambda z,c:(z*z)*z+c
                    case _:
                        iterate=lambda z,c:z*z+c
                while (count<255) and (zz.magsq()<5000):
                    zz=iterate(zz,c)
#                    zz=(zz*zz)+c
                    count=count+1
#                    if ypix==100 and zpix==100:
#                        print(zz)
#                if ypix==100 and zpix==100:
#                    print(count)
                plane[ypix][zpix][0]=colormap[count][0]
                plane[ypix][zpix][1]=colormap[count][1]
                plane[ypix][zpix][2]=colormap[count][2]
        return plane

    def calcFractal(self, xmin, xmax, ymin, ymax, zmin, zmax, imagesize, colormap, ringtype, itertype):
        poolsize=multiprocessing.cpu_count() * 2
        pool=multiprocessing.Pool(processes=poolsize)
        plane_part=partial(fractal.calcPlane,ymin=ymin,ymax=ymax,zmin=zmin,zmax=zmax,imagesize=imagesize,colormap=colormap,julia=self.isjulia,jx=self.jx,jy=self.jy,jz=self.jz,ringtype=ringtype,itertype=itertype)
        x=list()
        for xpix in range(imagesize):
            x.append(xmin+xpix*(xmax-xmin)/(imagesize-1))
#            self.shape[xpix]=fractal.calcPlane(x, ymin, ymax, zmin, zmax, imagesize, colormap)
        outputs=pool.map(plane_part,x)
        pool.close()
        pool.join()
        return numpy.stack(outputs,axis=0)

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, imagesize, julia=False, jx=0.0, jy=0.0, jz=0.0, ringtype="triel",itertype="z*z"):
        self.colormap=numpy.zeros((256,3),dtype=numpy.uint8)
        self.shape=numpy.zeros((imagesize,imagesize,imagesize,3),dtype=numpy.uint8)
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.zmin=zmin
        self.zmax=zmax
        self.imagesize=imagesize
        self.isjulia=julia
        self.jx=jx
        self.jy=jy
        self.jz=jz
        for c in range(256):
            h=(math.sin(4.0*c/255.0*math.pi))
            s=(math.sin(1.5*c/255.0*math.pi/2.0))
            v=(math.cos(1.0*c/255.0*math.pi/2.0))
            rgb=colorsys.hsv_to_rgb(h,s,v)
            self.colormap[c][0]=int(abs(rgb[0]*255))%255
            self.colormap[c][1]=int(abs(rgb[1]*255))%255
            self.colormap[c][2]=int(abs(rgb[2]*255))%255
        self.shape=self.calcFractal(xmin, xmax, ymin, ymax, zmin, zmax, imagesize, self.colormap, ringtype, itertype)


    def render(self):
        if self.isjulia:
            savedir="julia"+str(self.jx)+str(self.jy)+str(self.jz)+"at"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(self.imagesize)
        else:
            savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(self.imagesize)
        print(savedir)
        os.makedirs(savedir,exist_ok=True)
        os.makedirs(savedir+"\\slicer",exist_ok=True)
        for xpix in range(self.imagesize):
            rawslice=self.shape[xpix,:,:,:].copy()
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(savedir+"\XFrame"+str(xpix)+".jpg")
            for yp in range(self.imagesize):
                for zp in range(self.imagesize):
                    if (rawslice[yp,zp,0]==0 and rawslice[yp,zp,1]==0 and rawslice[yp,zp,2]==0):
                        rawslice[yp,zp,0]=255
                        rawslice[yp,zp,1]=255
                        rawslice[yp,zp,2]=255
                    else:
                        rawslice[yp,zp,0]=0
                        rawslice[yp,zp,1]=0
                        rawslice[yp,zp,2]=0
            slicer=Image.fromarray(rawslice,mode="RGB")
            slicer.save(savedir+"\\slicer\Frame"+str(xpix)+".jpg")
        for ypix in range(self.imagesize):
            rawslice=self.shape[:,ypix,:,:]
            slice=Image.fromarray(rawslice,mode="RGB").transpose(Image.FLIP_TOP_BOTTOM)
            slice.save(savedir+"\YFrame"+str(ypix)+".jpg")
        for zpix in range(self.imagesize):
            rawslice=self.shape[:,:,zpix,:]
            slice=Image.fromarray(rawslice,mode="RGB").transpose(Image.FLIP_TOP_BOTTOM)
            slice.save(savedir+"\ZFrame"+str(zpix)+".jpg")
        zf=open(savedir+"\zeroes.csv","w")
        for xz in range(self.imagesize):
            for yz in range(self.imagesize):
                for zz in range(self.imagesize):
                    if self.shape[xz][yz][zz][0]==0 and self.shape[xz][yz][zz][1]==0 and self.shape[xz][yz][zz][2]==0:
                        xzf=self.xmin+xz*(self.xmax-self.xmin)/self.imagesize
                        yzf=self.ymin+yz*(self.ymax-self.ymin)/self.imagesize
                        zzf=self.zmin+zz*(self.zmax-self.zmin)/self.imagesize
                        zf.write("{},{},{}\n".format(xzf,yzf,zzf))

class Fractalapp:
    def __init__(self,master):
        appMap=dict()
        imagesize=301
        self.xmin=-1.5
        self.xmax=1.5
        self.ymin=-1.5
        self.ymax=1.5
        self.zmin=-1.5
        self.zmax=1.5
#        zmin=-0.52525
#        zmax=-0.27425
#        xmin=-0.34525
#        xmax=-0.09425
#        ymin=0.3179
#        ymax=0.5689
        clickx=0
        clicky=0
        clickz=0
        self.centerx=0.0
        self.centery=0.0
        self.centerz=0.0
        self.edgex=0.0
        self.edgey=0.0
        self.edgez=0.0
        self.radius=0.0
        self.isjulia=False
        self.firstclick=False
        self.secondclick=False
        self.itertype=StringVar()
        self.itertype.set("z*z")
        self.ringtype=StringVar()
        self.ringtype.set("triel")
        self.jx=0.0
        self.jy=0.0
        self.jz=0.0
#############################################################
# Do Initialization Window                                  #
#############################################################
        setupWindow=Toplevel(master)
        iterOptions= [
            "z*z",
            "z*(z*z)",
            "(z*z)*z"
        ]
        ringOptions= [
            "triel",
            "atriel",
            "braid",
            "abraid",
            "chaos",
            "cbraid",
            "dbraid",
            "anarch",
            "zbraid",
            "flatq",
            "bulb3",
            "cbulb3"
        ]
        iterDrop=OptionMenu(setupWindow,self.itertype,*iterOptions)
        iterDrop.pack()
        ringDrop=OptionMenu(setupWindow,self.ringtype,*ringOptions)
        ringDrop.pack()
        button_close=Button(setupWindow,text="Close",command=setupWindow.destroy)
        button_close.pack()
        setupWindow.focus()
        setupWindow.grab_set()
        master.withdraw()
        master.wait_window(setupWindow)
    #####################################################################
    # End Initialization Window                                         #
    #####################################################################

        self.savedirs=set()
        self.savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
        print(self.savedir)
        self.savedirs.add(self.savedir)
        f=fractal(self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax,imagesize,ringtype=self.ringtype.get(),itertype=self.itertype.get())
        f.render()
        master.deiconify()

        self.xfr=imagesize//2
        self.yfr=imagesize//2
        self.zfr=imagesize//2


        def update_frames():
            self.xfr=int(boxXFrame.get("1.0", 'end-1c'))
            self.yfr=int(boxYFrame.get("1.0", 'end-1c'))
            self.zfr=int(boxZFrame.get("1.0", 'end-1c'))
            xim=ImageTk.PhotoImage(Image.open(self.savedir+"\XFrame"+str(self.xfr)+".jpg"))
            conx=cx.create_image(0,0,image=xim,anchor=NW)
            appMap['conx']=conx
            cx.imgref=xim
            yim=ImageTk.PhotoImage(Image.open(self.savedir+"\YFrame"+str(self.yfr)+".jpg"))
            cony=cy.create_image(0,0,image=yim,anchor=NW)
            appMap['cony']=cony
            cy.imgref=yim
            zim=ImageTk.PhotoImage(Image.open(self.savedir+"\ZFrame"+str(self.zfr)+".jpg"))
            conz=cz.create_image(0,0,image=zim,anchor=NW)
            appMap['conz']=conz
            cz.imgref=zim
            if self.secondclick:
                print("Updating with two points clicked")
                box_xmin=((self.centerx-self.radius)-self.xmin)/(self.xmax-self.xmin)*(imagesize+1)
                box_xmax=((self.centerx+self.radius)-self.xmin)/(self.xmax-self.xmin)*(imagesize+1)
                box_ymin=((self.centery-self.radius)-self.ymin)/(self.ymax-self.ymin)*(imagesize+1)
                box_ymax=((self.centery+self.radius)-self.ymin)/(self.ymax-self.ymin)*(imagesize+1)
                box_zmin=((self.centerz-self.radius)-self.zmin)/(self.zmax-self.zmin)*(imagesize+1)
                box_zmax=((self.centerz+self.radius)-self.zmin)/(self.zmax-self.zmin)*(imagesize+1)
                print((box_xmin,box_xmax,box_ymin,box_ymax,box_zmin,box_zmax))
                print((self.xfr, self.yfr, self.zfr))
                if (self.xfr>=imagesize-box_xmax) and (self.xfr<=imagesize-box_xmin):
#                    print("x visible")
                    print((box_xmin,box_xmax,box_ymin,box_ymax,box_zmin,box_zmax))
                    print(self.xfr, int(box_xmin+(box_xmax-box_xmin)/2))
                    if int(imagesize-self.xfr)==int(box_xmin+(box_xmax-box_xmin)/2):
                        cx.create_rectangle(box_ymin,box_zmin,box_ymax,box_zmax,outline="red",width=1)    
                    else:
                        cx.create_rectangle(box_ymin,box_zmin,box_ymax,box_zmax,outline="white",width=1)    
                if (self.yfr>=box_ymin) and (self.yfr<=box_ymax):
                    print("y visible")
                    if int(self.yfr)==int(box_ymin+(box_ymax-box_ymin)/2):
                        cy.create_rectangle(box_zmin,imagesize-box_xmax,box_zmax,imagesize-box_xmin,outline="red",width=1)
                    else:
                        cy.create_rectangle(box_zmin,imagesize-box_xmax,box_zmax,imagesize-box_xmin,outline="white",width=1)
                if (self.zfr>=box_zmin) and (self.zfr<=box_zmax):
                    print("z visible")
                    if int(self.zfr)==int(box_zmin+(box_zmax-box_zmin)/2):
                        cz.create_rectangle(box_ymin,imagesize-box_xmax,box_ymax,imagesize-box_xmin,outline="red",width=1)
                    else:
                        cz.create_rectangle(box_ymin,imagesize-box_xmax,box_ymax,imagesize-box_xmin,outline="white",width=1)
            master.update_idletasks()
        def decX(event="none"):
            if (self.xfr>0):
                self.xfr=self.xfr-1
                boxXFrame.delete("1.0",END)
                boxXFrame.insert("1.0",str(self.xfr))
                update_frames()
        def incX(event="none"):
            if (self.xfr<imagesize-1):
                self.xfr=self.xfr+1
                boxXFrame.delete("1.0",END)
                boxXFrame.insert("1.0",str(self.xfr))
                update_frames()
        def decY(event="none"):
            if (self.yfr>0):
                self.yfr=self.yfr-1
                boxYFrame.delete("1.0",END)
                boxYFrame.insert("1.0",str(self.yfr))
                update_frames()
        def incY(event="none"):
            if (self.yfr<imagesize-1):
                self.yfr=self.yfr+1
                boxYFrame.delete("1.0",END)
                boxYFrame.insert("1.0",str(self.yfr))
                update_frames()
        def decZ(event="none"):
            if (self.zfr>0):
                self.zfr=self.zfr-1
                boxZFrame.delete("1.0",END)
                boxZFrame.insert("1.0",str(self.zfr))
                update_frames()
        def incZ(event="none"):
            if (self.zfr<imagesize-1):
                self.zfr=self.zfr+1
                boxZFrame.delete("1.0",END)
                boxZFrame.insert("1.0",str(self.zfr))
                update_frames()
        def update_zoom():
            if (self.firstclick):
                self.edgex=self.xcl
                self.edgey=self.ycl
                self.edgez=self.zcl
                self.radius=max((abs(self.edgex-self.centerx),abs(self.edgey-self.centery),abs(self.edgez-self.centerz)))
                self.secondclick=True
            else:
                self.centerx=self.xcl
                self.centery=self.ycl
                self.centerz=self.zcl
                self.firstclick=True
            centertext=("Center:{0:.6f}{1:.6f}{2:.6f}".format(self.centerx,self.centery,self.centerz))
            edgetext=("Edge:{0:.6f}{1:.6f}{2:.6f}".format(self.edgex,self.edgey,self.edgez))
            self.centerTxt.set(centertext)
            self.edgeTxt.set(edgetext)
            update_frames()
#            print(centertext)
#            print(edgetext)
#            print(self.radius)

        def get_positionX(event):
            clickx=imagesize-self.xfr
            clicky=event.x
            clickz=event.y
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/(imagesize-1)
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/(imagesize-1)
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/(imagesize-1)
            print(str(clickx)+","+str(clicky))
            print(triel(self.xcl,self.ycl,self.zcl))
            update_zoom()
        def get_positionY(event):
            clickx=imagesize-event.y
            clicky=self.yfr
            clickz=event.x
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/(imagesize-1)
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/(imagesize-1)
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/(imagesize-1)
            print(str(clickx)+","+str(clicky))
            print(triel(self.xcl,self.ycl,self.zcl))
            update_zoom()
        def get_positionZ(event):
            clickx=imagesize-event.y
            clicky=event.x
            clickz=self.zfr
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/(imagesize-1)
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/(imagesize-1)
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/(imagesize-1)
            print(str(clickx)+","+str(clicky))
            print(triel(self.xcl,self.ycl,self.zcl))
            update_zoom()
        cxf=Frame(master)
        cxf.grid(row=1,column=1)
        cx=Canvas(cxf,height=imagesize,width=imagesize)
        cx.bind("<Button-1>",get_positionX)
        cx.pack()
        xlabeltext=StringVar()
        xlabeltext.set("Frame# "+str(self.xfr)+ "X="+str(self.xmin+self.xfr*(self.xmax-self.xmin)/(imagesize-1)))
        cxlabel=Label(cxf,textvariable=xlabeltext)
        cxlabel.pack()
        xim=ImageTk.PhotoImage(Image.open(self.savedir+"\XFrame"+str(self.xfr)+".jpg"))
        conx=cx.create_image(0,0,image=xim,anchor=NW)
        appMap['conx']=conx
        cyf=Frame(master)
        cyf.grid(row=1,column=2)
        cy=Canvas(cyf,height=imagesize,width=imagesize)
        cy.bind("<Button-1>",get_positionY)
        cy.pack()
        ylabeltext=StringVar()
        ylabeltext.set("Frame# "+str(self.yfr)+ "Y="+str(self.ymin+self.yfr*(self.ymax-self.ymin)/(imagesize-1)))
        cylabel=Label(cyf,textvariable=ylabeltext)
        cylabel.pack()
        yim=ImageTk.PhotoImage(Image.open(self.savedir+"\YFrame"+str(self.yfr)+".jpg"))
        #yim=PhotoImage(file=(dir+"\YFrame50.jpg"))
        cony=cy.create_image(0,0,image=yim,anchor=NW)
        appMap['cony']=cony
        czf=Frame(master)
        czf.grid(row=2,column=1)
        cz=Canvas(czf,height=imagesize,width=imagesize)
        cz.bind("<Button-1>",get_positionZ)
        cz.pack()
        zlabeltext=StringVar()
        zlabeltext.set("Frame# "+str(self.zfr)+ "Z="+str(self.zmin+self.zfr*(self.zmax-self.zmin)/(imagesize-1)))
        czlabel=Label(czf,textvariable=zlabeltext)
        czlabel.pack()
        zim=ImageTk.PhotoImage(Image.open(self.savedir+"\ZFrame"+str(self.zfr)+".jpg"))
        #zim=PhotoImage(file=(dir+"\ZFrame50.jpg"))
        conz=cz.create_image(0,0,image=zim,anchor=NW)
        appMap['conz']=conz
        fr22=Frame(master)
        fr22.grid(row=2,column=2)
        boxXFrame=Text(fr22,height=1,width=5)
        boxXFrame.insert("1.0",str(self.xfr))
        boxYFrame=Text(fr22,height=1,width=5)
        boxYFrame.insert("1.0",str(self.yfr))
        boxZFrame=Text(fr22,height=1,width=5)
        boxZFrame.insert("1.0",str(self.zfr))
        boxSaveDir=Text(fr22,height=1,width=30)
        boxSaveDir.insert("1.0","C:/Fractals")
        self.centerTxt=StringVar()
        self.centerTxt.set("No Center Set")
        zoomcenter=Label(fr22,textvariable=self.centerTxt)
        self.edgeTxt=StringVar()
        self.edgeTxt.set("No Edge Set")
        zoomedge=Label(fr22,textvariable=self.edgeTxt)

        master.bind('j',decX)
        master.bind('k',incX)
        master.bind('i',incY)
        master.bind('m',decY)
        master.bind('o',incZ)
        master.bind('n',decZ)

        def Zoom():
            if (self.secondclick):
                self.xmin=self.centerx-self.radius
                self.xmax=self.centerx+self.radius
                self.ymin=self.centery-self.radius
                self.ymax=self.centery+self.radius
                self.zmin=self.centerz-self.radius
                self.zmax=self.centerz+self.radius
                self.centerx=0.0
                self.centery=0.0
                self.centerz=0.0
                self.edgex=0.0
                self.edgey=0.0
                self.edgez=0.0
                self.radius=0.0
                self.firstclick=False
                self.secondclick=False
                if self.isjulia:
                    self.savedir="julia"+str(self.jx)+str(self.jy)+str(self.jz)+"at"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
                    self.fractalinfo.set("Julia type fractal at x={6:.6f} y={7:.6f} z={8:.6f} {ringtype} {itertype}\n X:{0:.6f}-{1:.6f} Y:{2:.6f}-{3:.6f} Z:{4:.6f}-{5:.6f}".format(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax, self.jx, self.jy, self.jz,ringtype=self.ringtype.get(),itertype=self.itertype.get()))
                else:
                    self.savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
                    self.fractalinfo.set("Mandelbrot type fractal, {ringtype} {itertype}\n X:{0:.6f}-{1:.6f} Y:{2:.6f}-{3:.6f} Z:{4:.6f}-{5:.6f}".format(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax, ringtype=self.ringtype.get(), itertype=self.itertype.get()))
                print(self.savedir)
                self.savedirs.add(self.savedir)
                f=fractal(self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax,imagesize,julia=self.isjulia,jx=self.jx,jy=self.jy,jz=self.jz,ringtype=self.ringtype.get(),itertype=self.itertype.get())
                f.render()
                self.xfr=imagesize//2
                self.yfr=imagesize//2
                self.zfr=imagesize//2                
                self.centerTxt.set("No Center Set")
                self.edgeTxt.set("No Edge Set")
                boxXFrame.delete("1.0",END)
                boxXFrame.insert("1.0",str(self.xfr))
                boxYFrame.delete("1.0",END)
                boxYFrame.insert("1.0",str(self.yfr))
                boxZFrame.delete("1.0",END)
                boxZFrame.insert("1.0",str(self.zfr))
                update_frames()
        def Julia():
            if (self.secondclick) and not self.isjulia:
                self.xmin=-1.5
                self.xmax=1.5
                self.ymin=-1.5
                self.ymax=1.5
                self.zmin=-1.5
                self.zmax=1.5
                self.centerx=0.0
                self.centery=0.0
                self.centerz=0.0
                self.radius=0.0
                self.jx=self.edgex
                self.jy=self.edgey
                self.jz=self.edgez
                self.firstclick=False
                self.secondclick=False
                self.isjulia=True
                self.savedir="julia"+str(self.jx)+str(self.jy)+str(self.jz)+"at"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
                self.fractalinfo.set("Julia type fractal {ringtype} {itertype} at x={6:.6f} y={7:.6f} z={8:.6f}\n X:{0:.6f}-{1:.6f} Y:{2:.6f}-{3:.6f} Z:{4:.6f}-{5:.6f}".format(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax, self.jx, self.jy, self.jz, ringtype=self.ringtype.get(), itertype=self.itertype.get()))
                print(self.savedir)
                self.savedirs.add(self.savedir)
                f=fractal(self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax,imagesize,julia=True,jx=self.jx,jy=self.jy,jz=self.jz,ringtype=self.ringtype.get(),itertype=self.itertype.get())
                f.render()
                self.xfr=imagesize//2
                self.yfr=imagesize//2
                self.zfr=imagesize//2                
                self.edgex=0.0
                self.edgey=0.0
                self.edgez=0.0
                self.centerTxt.set("No Center Set")
                self.edgeTxt.set("No Edge Set")
                boxXFrame.delete("1.0",END)
                boxXFrame.insert("1.0",str(self.xfr))
                boxYFrame.delete("1.0",END)
                boxYFrame.insert("1.0",str(self.yfr))
                boxZFrame.delete("1.0",END)
                boxZFrame.insert("1.0",str(self.zfr))
                update_frames()
        def Save():
            path=boxSaveDir.get("1.0", 'end-1c')
            os.makedirs(path,exist_ok=True)
            shutil.copytree(self.savedir,path+"\\"+self.savedir,dirs_exist_ok=True)
        
        def Reset():
            self.firstclick=False
            self.secondclick=False
            self.centerx=0.0
            self.centery=0.0
            self.centerz=0.0
            self.edgex=0.0
            self.edgey=0.0
            self.edgez=0.0
            self.centerTxt.set("No Center Set")
            self.edgeTxt.set("No Edge Set")    
            update_frames()

        self.fractalinfo=StringVar()
        self.fractalinfo.set("Mandelbrot type fractal, {ringtype} {itertype}\n X:{0:.6f}-{1:.6f} Y:{2:.6f}-{3:.6f} Z:{4:.6f}-{5:.6f}".format(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax, ringtype=self.ringtype.get(), itertype=self.itertype.get()))
        infoLabel=Label(fr22,textvariable=self.fractalinfo)
        refreshButton=Button(fr22,text="Refresh",command=update_frames)
        zoomButton=Button(fr22,text="Zoom",command=Zoom)
        juliaButton=Button(fr22,text="Julia",command=Julia)
        saveButton=Button(fr22,text="Save",command=Save)
        resetButton=Button(fr22,text="Reset",command=Reset)
        infoLabel.pack()
        boxXFrame.pack()
        boxYFrame.pack()
        boxZFrame.pack()
        boxSaveDir.pack()
        refreshButton.pack()
        zoomcenter.pack()
        zoomedge.pack()
        zoomButton.pack()
        juliaButton.pack()
        saveButton.pack()
        resetButton.pack()
        fr22.grid(row=2,column=2)
        def Cleanup(event):
            for oldshape in self.savedirs:
                if os.path.isdir(oldshape):
                    shutil.rmtree(oldshape)
        master.bind("<Destroy>",Cleanup)
        update_frames()
        
def main():
    root=Tk()
    app=Fractalapp(root)
    root.mainloop()

if __name__ == "__main__": main()