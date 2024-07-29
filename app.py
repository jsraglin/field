import math
import numpy
import os
from tkinter import *
import _tkinter
from PIL import Image
from field import field
import multiprocessing
from functools import partial

class fractal:
    @staticmethod
    def calcPlane(x, ymin, ymax, zmin, zmax, imagesize,colormap):
        plane=numpy.zeros((imagesize, imagesize, 3),dtype=numpy.uint8)
        for ypix in range(imagesize):
            y=ymin+ypix*(ymax-ymin)/imagesize
            for zpix in range(imagesize):
                z=zmin+zpix*(zmax-zmin)/imagesize
                c=field(x,y,z)
#                if ypix==100 and zpix==100:
#                    print(c)    
                zz=field(0,0,0)
                count=0
                while (count<100) and (zz.magsq()<5000):
                    zz=zz*(zz*zz)+c
                    count=count+1
#                    if ypix==100 and zpix==100:
#                        print(zz)
#                if ypix==100 and zpix==100:
#                    print(count)
                if count<100:
                    plane[ypix][zpix][0]=colormap[count][0]
                    plane[ypix][zpix][1]=colormap[count][1]
                    plane[ypix][zpix][2]=colormap[count][2]
        return plane

    def calcFractal(self, xmin, xmax, ymin, ymax, zmin, zmax, imagesize, colormap):
        poolsize=multiprocessing.cpu_count() * 2
        pool=multiprocessing.Pool(processes=poolsize)
        plane_part=partial(fractal.calcPlane,ymin=ymin,ymax=ymax,zmin=zmin,zmax=zmax,imagesize=imagesize,colormap=colormap)
        x=list()
        for xpix in range(imagesize):
            x.append(xmin+xpix*(xmax-xmin)/imagesize)
#            self.shape[xpix]=fractal.calcPlane(x, ymin, ymax, zmin, zmax, imagesize, colormap)
        outputs=pool.map(plane_part,x)
        pool.close()
        pool.join()
        return numpy.stack(outputs,axis=0)

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, imagesize):
        self.colormap=numpy.zeros((256,3),dtype=numpy.uint8)
        self.shape=numpy.zeros((imagesize,imagesize,imagesize,3),dtype=numpy.uint8)
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.zmin=zmin
        self.zmax=zmax
        self.imagesize=imagesize
        for c in range(256):
            self.colormap[c][0]=c*7%255
            self.colormap[c][1]=c*26%255
            self.colormap[c][2]=c*16%255
        self.shape=self.calcFractal(xmin, xmax, ymin, ymax, zmin, zmax, imagesize, self.colormap)


    def render(self):
        savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(self.imagesize)
        print(savedir)
        os.makedirs(savedir,exist_ok=True)
        for xpix in range(self.imagesize):
            rawslice=self.shape[xpix,:,:,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(savedir+"\XFrame"+str(xpix)+".gif")
        for ypix in range(self.imagesize):
            rawslice=self.shape[:,ypix,:,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(savedir+"\YFrame"+str(ypix)+".gif")
        for zpix in range(self.imagesize):
            rawslice=self.shape[:,:,zpix,:]
            slice=Image.fromarray(rawslice,mode="RGB")
            slice.save(savedir+"\ZFrame"+str(zpix)+".gif")
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
        imagesize=300
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
        self.firstclick=False
        self.secondclick=False
        self.savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
        print(self.savedir)
        f=fractal(self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax,imagesize)
        f.render()
        self.xfr=imagesize//2
        self.yfr=imagesize//2
        self.zfr=imagesize//2
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
#            print(centertext)
#            print(edgetext)
#            print(self.radius)

        def get_positionX(event):
            clickx=self.xfr
            clicky=event.x
            clickz=event.y
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/imagesize
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/imagesize
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/imagesize
            print(str(clickx)+","+str(clicky))
            print(field(self.xcl,self.ycl,self.zcl))
            update_zoom()
        def get_positionY(event):
            clickx=event.y
            clicky=self.yfr
            clickz=event.x
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/imagesize
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/imagesize
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/imagesize
            print(str(clickx)+","+str(clicky))
            print(field(self.xcl,self.ycl,self.zcl))
            update_zoom()
        def get_positionZ(event):
            clickx=event.y
            clicky=imagesize-event.x
            clickz=self.zfr
            self.xcl=self.xmin+clickx*(self.xmax-self.xmin)/imagesize
            self.ycl=self.ymin+clicky*(self.ymax-self.ymin)/imagesize
            self.zcl=self.zmin+clickz*(self.zmax-self.zmin)/imagesize
            print(str(clickx)+","+str(clicky))
            print(field(self.xcl,self.ycl,self.zcl))
            update_zoom()

        cxf=Frame(master)
        cxf.grid(row=1,column=1)
        cx=Canvas(cxf,height=imagesize,width=imagesize)
        cx.bind("<Button-1>",get_positionX)
        cx.pack()
        xlabeltext=StringVar()
        xlabeltext.set("Frame# "+str(self.xfr)+ "X="+str(self.xmin+self.xfr*(self.xmax-self.xmin)/imagesize))
        cxlabel=Label(cxf,textvariable=xlabeltext)
        cxlabel.pack()
        xim=PhotoImage(file=(self.savedir+"\XFrame"+str(self.xfr)+".gif"))
        conx=cx.create_image(0,0,image=xim,anchor=NW)
        appMap['conx']=conx
        cyf=Frame(master)
        cyf.grid(row=1,column=2)
        cy=Canvas(cyf,height=imagesize,width=imagesize)
        cy.bind("<Button-1>",get_positionY)
        cy.pack()
        ylabeltext=StringVar()
        ylabeltext.set("Frame# "+str(self.yfr)+ "Y="+str(self.ymin+self.yfr*(self.ymax-self.ymin)/imagesize))
        cylabel=Label(cyf,textvariable=ylabeltext)
        cylabel.pack()
        yim=PhotoImage(file=(self.savedir+"\YFrame"+str(self.yfr)+".gif"))
        #yim=PhotoImage(file=(dir+"\YFrame50.gif"))
        cony=cy.create_image(0,0,image=yim,anchor=NW)
        appMap['cony']=cony
        czf=Frame(master)
        czf.grid(row=2,column=1)
        cz=Canvas(czf,height=imagesize,width=imagesize)
        cz.bind("<Button-1>",get_positionZ)
        cz.pack()
        zlabeltext=StringVar()
        zlabeltext.set("Frame# "+str(self.zfr)+ "Z="+str(self.zmin+self.zfr*(self.zmax-self.zmin)/imagesize))
        czlabel=Label(czf,textvariable=zlabeltext)
        czlabel.pack()
        zim=PhotoImage(file=(self.savedir+"\ZFrame"+str(self.zfr)+".gif"))
        #zim=PhotoImage(file=(dir+"\ZFrame50.gif"))
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
        self.centerTxt=StringVar()
        self.centerTxt.set("No Center Set")
        zoomcenter=Label(fr22,textvariable=self.centerTxt)
        self.edgeTxt=StringVar()
        self.edgeTxt.set("No Edge Set")
        zoomedge=Label(fr22,textvariable=self.edgeTxt)

        def update_frames():
            self.xfr=int(boxXFrame.get("1.0", 'end-1c'))
            self.yfr=int(boxYFrame.get("1.0", 'end-1c'))
            self.zfr=int(boxZFrame.get("1.0", 'end-1c'))
            xim=PhotoImage(file=(self.savedir+"\XFrame"+str(self.xfr)+".gif"))
            conx=cx.create_image(0,0,image=xim,anchor=NW)
            appMap['conx']=conx
            cx.imgref=xim
            yim=PhotoImage(file=(self.savedir+"\YFrame"+str(self.yfr)+".gif"))
            cony=cy.create_image(0,0,image=yim,anchor=NW)
            appMap['cony']=cony
            cy.imgref=yim
            zim=PhotoImage(file=(self.savedir+"\ZFrame"+str(self.zfr)+".gif"))
            conz=cz.create_image(0,0,image=zim,anchor=NW)
            appMap['conz']=conz
            cz.imgref=zim
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
                self.savedir="shape"+str(self.xmin)+str(self.xmax)+str(self.ymin)+str(self.ymax)+str(self.zmin)+str(self.zmax)+str(imagesize)
                print(self.savedir)
                f=fractal(self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax,imagesize)
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
        
        refreshButton=Button(fr22,text="Refresh",command=update_frames)
        zoomButton=Button(fr22,text="Zoom",command=Zoom)
        boxXFrame.pack()
        boxYFrame.pack()
        boxZFrame.pack()
        refreshButton.pack()
        zoomcenter.pack()
        zoomedge.pack()
        zoomButton.pack()
        fr22.grid(row=2,column=2)
        
def main():
    root=Tk()
    app=Fractalapp(root)
    root.mainloop()

if __name__ == "__main__": main()