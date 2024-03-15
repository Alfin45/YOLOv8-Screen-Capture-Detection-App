import multiprocessing
from ultralytics import YOLO
from tkinter import *
import time
import numpy as np
import cv2
from mss import mss
from PIL import Image, ImageTk
multiprocessing.freeze_support()


wdw = Tk()
run = False
sharpenOn = False
nightVis = False

timedata = time.strftime("%Y%m%d-%H%M%S")
infostatus = "IDLE"

wdw.title(".:: FinApp ::.")
wdw.wm_iconbitmap("appneed/assets/appicon.ico")
screen_width = wdw.winfo_screenwidth()
screen_height = wdw.winfo_screenheight()
w = screen_width/2
h = screen_height
x = w-10
y = 0
hl = screen_height/1.5
w = int(w)
h = int(h)
hl = int(hl)

# --
sct = mss()

# --
model = YOLO('appneed/last.pt')

wdw.geometry("%dx%d+%d+%d" % (w, h, x, y))
wdw['background'] = '#353a61'


desc = 'Screen Capture App with YOLOv8 \n  tkinter, ultralystic, cv2, numpy, mss, PIL'


def detect():
    if run:
        global statusUpdate, updateImg
        # -- 
        monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
        img = Image.frombytes("RGB", (w, h), sct.grab(monitor).rgb)

        if sharpenOn is False and nightVis is False:
            statusUpdate = "DETECTING : NORMAL"
            labelInfo.config(text=f"{statusUpdate}")

            screen = np.array(img)
            result = model(screen)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is False and nightVis is True:
            statusUpdate = "NIGHTVISION NORMAL"
            labelInfo.config(text=f"{statusUpdate}")

            screen = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HLS)
            result = model(screen)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is True and nightVis is False:
            statusUpdate = "DETECTING : SHARPEN"
            labelInfo.config(text=statusUpdate)

            screen = np.array(img)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened_image = cv2.filter2D(screen, -1, kernel*1.5)
            result = model(sharpened_image)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        else:
            statusUpdate = "NIGHTVISION SHARPEN"
            labelInfo.config(text=statusUpdate)

            screen = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HLS)
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened_image = cv2.filter2D(screen, -1, kernel*1.5)
            result = model(sharpened_image)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        data.save('appneed/dat/result.png')

        updateImg = ImageTk.PhotoImage(Image.open('appneed/dat/result.png'))
        label.config(image=updateImg)

    wdw.after(1, detect)  # --


def start():
    global run
    run = True
    startbtn["state"] = "disabled"
    btnDisable["state"] = "active"
    stopbtnPause["state"] = "active"
    btnSave["state"] = "active"
    btnSharpened["state"] = "active"
    startbtn["state"] = "disabled"
    btnNight["state"] = "active"


def stop():
    global run, statusUpdate
    run = False
    statusUpdate = "PAUSE"
    labelInfo.config(text=f"{statusUpdate}")
    btnDisable["state"] = "active"
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "active"
    startbtn["state"] = "active"
    btnSharpened["state"] = "disabled"
    btnNight["state"] = "disabled"


def disable():
    global run, startImg, statusUpdate
    run = False
    startImg = ImageTk.PhotoImage(Image.open('appneed/dat/start.png'))
    label.config(image=startImg)
    statusUpdate = "IDLE"
    labelInfo.config(text=f"{statusUpdate}")
    btnDisable["state"] = "disabled"
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "disabled"
    btnSharpened["state"] = "disabled"
    btnNight["state"] = "disabled"
    startbtn["state"] = "active"


def sharpenedimg():
    global sharpenOn
    if sharpenOn:
        sharpenOn = False
    else:
        sharpenOn = True


def nightvision():
    global nightVis
    if nightVis:
        nightVis = False
    else:
        nightVis = True


def saveimg():
    global run, statusUpdate
    run = False
    saverimg = Image.open('appneed/dat/result.png')
    saverimg.save(f'appneed/result/{timedata}.png')
    statusUpdate = f"SAVED:appneed/result/{timedata}.png"
    labelInfo.config(text=statusUpdate)
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "disabled"
    btnSharpened["state"] = "disabled"
    startbtn["state"] = "active"
    btnNight["state"] = "disabled"


def quit_tk():
    global statusUpdate, updateImg, run
    run = False
    statusUpdate = ".:: GOODBYE ::."
    labelInfo.config(text=statusUpdate)
    resetimg = Image.open('appneed/dat/start.png')
    resetimg.save('appneed/dat/result.png')
    startbtn["state"] = "disabled"
    btnDisable["state"] = "disabled"
    stopbtnPause["state"] = "disabled"
    btnSharpened["state"] = "disabled"
    btnSave["state"] = "disabled"
    btnStop["state"] = "disabled"
    btnNight["state"] = "disabled"

    updateImg = ImageTk.PhotoImage(Image.open('appneed/dat/result.png'))
    label.config(image=updateImg)
    wdw.after(3000, exitprog)


def exitprog():
    wdw.destroy()
    exit()


# --
desc_label = Label(wdw, background='#353a61',
                   font='System 18 bold',
                   fg='#8f9cff',
                   text=desc)
desc_label.pack(pady=7)


# --
im = Image.open('appneed/dat/result.png')
updateImg = ImageTk.PhotoImage(im)
label = Label(wdw, width=w, height=hl,
              borderwidth=5,
              relief="sunken",
              image=updateImg)
label.pack()


# --
imgBtnStart = Image.open('appneed/assets/play.png')
resize_imageStart = imgBtnStart.resize((50, 50))
click_btnStart = ImageTk.PhotoImage(resize_imageStart)


# --
startbtn = Button(wdw, borderwidth=0, width=50, height=50,
                  image=click_btnStart, background='#353a61',
                  activebackground='#353a61',
                  command=start)
startbtn.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnPause = Image.open('appneed/assets/pause.png')
resize_imagePause = imgBtnPause.resize((50, 50))
click_btnPause = ImageTk.PhotoImage(resize_imagePause)


# --
stopbtnPause = Button(wdw, borderwidth=0, width=50, height=50,
                      image=click_btnPause, background='#353a61',
                      activebackground='#353a61',
                      command=stop)
stopbtnPause.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnDisable = Image.open('appneed/assets/disableHome.png')
resize_imageDisable = imgBtnDisable.resize((50, 50))
click_btnDisable = ImageTk.PhotoImage(resize_imageDisable)

# --
btnDisable = Button(wdw, borderwidth=0, width=50, height=50,
                    image=click_btnDisable, background='#353a61',
                    activebackground='#353a61',
                    command=disable)
btnDisable.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnSharpened = Image.open('appneed/assets/enhance.png')
resize_imageSharpened = imgBtnSharpened.resize((50, 50))
click_btnSharpened = ImageTk.PhotoImage(resize_imageSharpened)


# --
btnSharpened = Button(wdw, borderwidth=0, width=50, height=50,
                      image=click_btnSharpened,
                      background='#353a61', activebackground='#353a61',
                      command=sharpenedimg)
btnSharpened.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnNight = Image.open('appneed/assets/night.png')
resize_imageNight = imgBtnNight.resize((50, 50))
click_btnNight = ImageTk.PhotoImage(resize_imageNight)


# --
btnNight = Button(wdw, borderwidth=0, width=50, height=50,
                  image=click_btnNight, background='#353a61',
                  activebackground='#353a61',
                  command=nightvision)
btnNight.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnSave = Image.open('appneed/assets/save.png')
resize_imageSave = imgBtnSave.resize((50, 50))
click_btnSave = ImageTk.PhotoImage(resize_imageSave)


# --
btnSave = Button(wdw, borderwidth=0, width=50, height=50,
                 image=click_btnSave, background='#353a61',
                 activebackground='#353a61',
                 command=saveimg)
btnSave.pack(anchor='nw', pady=25, padx=2, side=LEFT)


# --
imgBtnStop = Image.open('appneed/assets/stopbutton.png')
resize_imageStop = imgBtnStop.resize((50, 50))
click_btnStop = ImageTk.PhotoImage(resize_imageStop)


# --
btnStop = Button(wdw, borderwidth=0, width=50, height=50,
                 image=click_btnStop, background='#353a61',
                 activebackground='#353a61',
                 command=quit_tk)
btnStop.pack(anchor='nw', pady=25, padx=2, side=LEFT)


labelInfo = Label(wdw, text=f"{infostatus}",
                  background='#000000',
                  fg='#8f9cff',
                  font='System 10 bold',
                  width=70, height=2,
                  borderwidth=5,
                  relief="sunken"
                  )
labelInfo.pack(anchor='nw', pady=25, padx=2, side=LEFT)


startbtn["state"] = "active"
btnStop["state"] = "active"
stopbtnPause["state"] = "disabled"
btnDisable["state"] = "disabled"
btnSave["state"] = "disabled"
btnSharpened["state"] = "disabled"
btnNight["state"] = "disabled"

wdw.resizable(False, False)

wdw.after(1, detect())
wdw.mainloop()