from tkinter import *
import numpy as np
import cv2
from mss import mss
from PIL import Image,ImageTk
#detection
from ultralytics import YOLO

wdw = Tk()
run= True

wdw.title(".:: FinApp ::.")
wdw.wm_iconbitmap("assets/appicon.ico")
screen_width = wdw.winfo_screenwidth()
screen_height = wdw.winfo_screenheight()

# --
sct = mss()

# --
model = YOLO('model/last.pt')  

w=screen_width/2
h=screen_height
x=w-10
y=0
wdw.geometry("%dx%d+%d+%d" % (w,h,x,y))
wdw['background']='#353a61'

w=int(w)
h=int(h)

desc='Screen Capture App with YOLOv8 \n  tkinter, ultralystic, cv2, numpy, mss, PIL'
run= True


def detect():
    if run:
        # -- 
        monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
        img = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


        # --
        result = model(screen)
        annotated_frame = result[0].plot()
        data = Image.fromarray(annotated_frame)
        data.save('dat/result.png') 


        # -- 
        global updateImg
        updateImg = ImageTk.PhotoImage(Image.open('dat/result.png'))
        label.config( image = updateImg)
    wdw.after(50, detect)  # infinite loop

def start():
   global run
   run= True


def stop():
   global run
   run= False
   global startImg
   
def disable():
   global run
   run= False
   global startImg
   startImg = ImageTk.PhotoImage(Image.open('dat/start.png'))
   label.config(image = startImg) 

def quit_tk():
    wdw.destroy()
    exit()


# --
desc_label= Label(wdw, background='#353a61',
                  font='System 18 bold',
                  fg='#8f9cff',
                  text = desc)
desc_label.pack(pady=15)



# -- 
im = Image.open('dat/result.png')
updateImg = ImageTk.PhotoImage(im)
label =  Label(wdw,width=w,height=600, 
               borderwidth=3, 
               relief="sunken",
               image=updateImg)
label.pack()



#--
imgBtnStart= Image.open('assets/play.png')
resize_imageStart =imgBtnStart.resize((50, 50))
click_btnStart = ImageTk.PhotoImage(resize_imageStart)

startbtn = Button(wdw,borderwidth=0,width=50,height=50,
                  image=click_btnStart,background='#353a61',
                  activebackground='#353a61',
                  command=start).pack(anchor='nw', 
                                      pady=25, padx=10,
                                      side=LEFT)


# --
imgBtnPause= Image.open('assets/pause.png')
resize_imagePause =imgBtnPause.resize((50, 50))
click_btnPause = ImageTk.PhotoImage(resize_imagePause)


stopbtnPause = Button(wdw,borderwidth=0,width=50,height=50,
                 image=click_btnPause,background='#353a61',
                 activebackground='#353a61',
                 command=stop).pack(anchor='nw', 
                                    pady=25, padx=10,
                                    side=LEFT)



# --
imgBtnDisable= Image.open('assets/disableHome.png')
resize_imageDisable =imgBtnDisable.resize((50, 50))
click_btnDisable = ImageTk.PhotoImage(resize_imageDisable)

# --
btnDisable = Button(wdw,borderwidth=0,width=50,height=50,
             image=click_btnDisable,background='#353a61'
             ,activebackground='#353a61', 
             command=disable).pack(anchor='nw', 
                                  pady=25, padx=10,
                                  side=LEFT)


# --
imgBtnStop= Image.open('assets/stopbutton.png')
resize_imageStop =imgBtnStop.resize((50, 50))
click_btnStop = ImageTk.PhotoImage(resize_imageStop)

# --
btn= Button(wdw,borderwidth=0,width=50,height=50,
            image=click_btnStop,background='#353a61'
            ,activebackground='#353a61', 
            command=quit_tk).pack(anchor='nw', 
                                  pady=25, padx=10,
                                  side=LEFT)


wdw.after(50,detect)

# program
wdw.mainloop()