import multiprocessing
from ultralytics import YOLO
from tkinter import *
import numpy as np
import cv2
import os.path
from mss import mss
from PIL import Image, ImageTk
multiprocessing.freeze_support()


wdw = Tk()
run = False
sharpenOn = False
nightVis = False
acudef = 640
confdef = 25/100
ioudef = 70/100

infostatus = "IDLE"

wdw.title(".:: FinApp ::.")
wdw.wm_iconbitmap("appneed/assets/appicon.ico")
screen_width = wdw.winfo_screenwidth()
screen_height = wdw.winfo_screenheight()
w = screen_width/2
h = screen_height
x = w-5
y = 0
hl = screen_height/1.5
w = int(w)
h = int(h)
hl = int(hl)
datCount = 0

# --
sct = mss()

# --
model = YOLO('appneed/last.pt')

wdw.geometry("%dx%d+%d+%d" % (w, h, x, y))
wdw['background'] = '#353a61'


desc = 'Screen Capture App with YOLOv8 \n  tkinter, ultralystic, cv2, numpy, mss, PIL'


def detect():
    if run:
        global statusUpdate, updateImg, data
        # --
        monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
        img = Image.frombytes("RGB", (w, h), sct.grab(monitor).rgb)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        if sharpenOn is False and nightVis is False:
            statusUpdate = "DETECTING : NORMAL"
            labelInfo.config(text=f"{statusUpdate}")

            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is False and nightVis is True:
            statusUpdate = "NIGHTVISION NORMAL"
            labelInfo.config(text=f"{statusUpdate}")

            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated_frame = cv2.cvtColor(result[0].plot(), cv2.COLOR_BGR2HLS)
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is True and nightVis is False:
            statusUpdate = "DETECTING : SHARPEN"
            labelInfo.config(text=statusUpdate)

            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated = result[0].plot()
            annotated_frame = cv2.filter2D(annotated, -1, kernel*1.5)
            data = Image.fromarray(annotated_frame)

        else:
            statusUpdate = "NIGHTVISION SHARPEN"
            labelInfo.config(text=statusUpdate)

            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated = cv2.cvtColor(result[0].plot(), cv2.COLOR_BGR2HLS)
            annotated_frame = cv2.filter2D(annotated, -1, kernel*1.5)
            data = Image.fromarray(annotated_frame)

        updateImg = ImageTk.PhotoImage(data)
        label.config(image=updateImg)
        wdw.after(1, detect)


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
    wdw.after(1, detect)


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
    global run, statusUpdate, datCount
    run = False
    datCount = datCount + 1
    path = f'appneed/result/{datCount}.png'
    if os.path.isfile(path):
        wdw.after(1, saveimg)
    else:
        data.save(f'appneed/result/{datCount}.png')
        statusUpdate = f"SAVED:appneed/result/{datCount}.png"
        labelInfo.config(text=statusUpdate)
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "disabled"
    btnSharpened["state"] = "disabled"
    startbtn["state"] = "active"
    btnNight["state"] = "disabled"


def update_model():
    global run, acudef, confdef, ioudef, statusUpdate
    run = False
    statusUpdate = "MODEL CONFIG : UPDATED"
    labelInfo.config(text=f"{statusUpdate}")
    upacu = int(acu.get())
    upconf = int(conf.get())
    upiou = int(iou.get())

    if 1 <= upacu <= 25:
        acudef = 640
    elif 26 <= upacu <= 50:
        acudef = 736
    elif 51 <= upacu <= 75:
        acudef = 800
    else:
        acudef = 960

    confdef = upconf / 100
    ioudef = upiou / 100

    btnDisable["state"] = "active"
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "active"
    startbtn["state"] = "active"
    btnSharpened["state"] = "disabled"
    btnNight["state"] = "disabled"


def reset_model():
    global run, acudef, confdef, ioudef, statusUpdate
    run = False
    statusUpdate = "MODEL CONFIG : RESET"
    labelInfo.config(text=f"{statusUpdate}")
    acudef = 640
    confdef = 25 / 100
    ioudef = 70 / 100

    sliderAcu.set(1)
    sliderIoU.set(70)
    sliderConf.set(25)

    btnDisable["state"] = "active"
    stopbtnPause["state"] = "disabled"
    btnSave["state"] = "active"
    startbtn["state"] = "active"
    btnSharpened["state"] = "disabled"
    btnNight["state"] = "disabled"


def quit_tk():
    global statusUpdate, updateImg, run
    run = False
    statusUpdate = ".:: GOODBYE ::."
    labelInfo.config(text=statusUpdate)
    startbtn["state"] = "disabled"
    btnDisable["state"] = "disabled"
    stopbtnPause["state"] = "disabled"
    btnSharpened["state"] = "disabled"
    btnSave["state"] = "disabled"
    btnStop["state"] = "disabled"
    btnNight["state"] = "disabled"
    btnUp["state"] = "disabled"
    btnRes["state"] = "disabled"

    updateImg = ImageTk.PhotoImage(Image.open('appneed/dat/start.png'))
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
desc_label.pack(pady=2)


# --
im = Image.open('appneed/dat/start.png')
updateImg = ImageTk.PhotoImage(im)
label = Label(wdw, width=w, height=hl,
              borderwidth=5,
              relief="sunken",
              image=updateImg)
label.pack()

# --
frameFirst = Frame(wdw, bg='#353a61')
frameFirst.pack(expand=False, anchor="nw")

# --
frameSecond = Frame(wdw, bg='#353a61', highlightbackground="white", highlightthickness=1)
frameSecond.pack(expand=False, anchor="nw")

# --
imgBtnStart = Image.open('appneed/assets/play.png')
resize_imageStart = imgBtnStart.resize((50, 50))
click_btnStart = ImageTk.PhotoImage(resize_imageStart)


# --
startbtn = Button(frameFirst, borderwidth=0, width=50, height=50,
                  image=click_btnStart, background='#353a61',
                  activebackground='#353a61',
                  command=start)
startbtn.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnPause = Image.open('appneed/assets/pause.png')
resize_imagePause = imgBtnPause.resize((50, 50))
click_btnPause = ImageTk.PhotoImage(resize_imagePause)


# --
stopbtnPause = Button(frameFirst, borderwidth=0, width=50, height=50,
                      image=click_btnPause, background='#353a61',
                      activebackground='#353a61',
                      command=stop)
stopbtnPause.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnDisable = Image.open('appneed/assets/disableHome.png')
resize_imageDisable = imgBtnDisable.resize((50, 50))
click_btnDisable = ImageTk.PhotoImage(resize_imageDisable)

# --
btnDisable = Button(frameFirst, borderwidth=0, width=50, height=50,
                    image=click_btnDisable, background='#353a61',
                    activebackground='#353a61',
                    command=disable)
btnDisable.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnSharpened = Image.open('appneed/assets/enhance.png')
resize_imageSharpened = imgBtnSharpened.resize((50, 50))
click_btnSharpened = ImageTk.PhotoImage(resize_imageSharpened)


# --
btnSharpened = Button(frameFirst, borderwidth=0, width=50, height=50,
                      image=click_btnSharpened,
                      background='#353a61', activebackground='#353a61',
                      command=sharpenedimg)
btnSharpened.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnNight = Image.open('appneed/assets/night.png')
resize_imageNight = imgBtnNight.resize((50, 50))
click_btnNight = ImageTk.PhotoImage(resize_imageNight)


# --
btnNight = Button(frameFirst, borderwidth=0, width=50, height=50,
                  image=click_btnNight, background='#353a61',
                  activebackground='#353a61',
                  command=nightvision)
btnNight.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnSave = Image.open('appneed/assets/save.png')
resize_imageSave = imgBtnSave.resize((50, 50))
click_btnSave = ImageTk.PhotoImage(resize_imageSave)


# --
btnSave = Button(frameFirst, borderwidth=0, width=50, height=50,
                 image=click_btnSave, background='#353a61',
                 activebackground='#353a61',
                 command=saveimg)
btnSave.pack(pady=2, padx=2, side=LEFT)


# --
imgBtnStop = Image.open('appneed/assets/stopbutton.png')
resize_imageStop = imgBtnStop.resize((50, 50))
click_btnStop = ImageTk.PhotoImage(resize_imageStop)


# --
btnStop = Button(frameFirst, borderwidth=0, width=50, height=50,
                 image=click_btnStop, background='#353a61',
                 activebackground='#353a61',
                 command=quit_tk)
btnStop.pack(pady=2, padx=2, side=LEFT)

labelInfo = Label(frameFirst, text=f"{infostatus}",
                  background='#000000',
                  fg='#8f9cff',
                  font='System 10 bold',
                  width=50, height=2,
                  borderwidth=5,
                  relief="sunken"
                  )
labelInfo.pack(pady=2, padx=2, side=LEFT)


acu = IntVar()
sliderAcu = Scale(frameSecond, from_=1, to=100,
                  orient=HORIZONTAL, label="Accuracy",
                  bg='#353a61', font='System 10 bold',
                  fg='White', length=150, variable=acu)
sliderAcu.set(1)
sliderAcu.pack(pady=2, padx=2, side=LEFT)


conf = IntVar()
sliderConf = Scale(frameSecond, from_=1, to=80,
                   orient=HORIZONTAL, label="Confidence",
                   bg='#353a61', font='System 10 bold',
                   fg='White', length=150, variable=conf)
sliderConf.set(25)
sliderConf.pack(pady=2, padx=2, side=LEFT)


iou = IntVar()
sliderIoU = Scale(frameSecond, from_=1, to=100,
                  orient=HORIZONTAL, label="IoU",
                  bg='#353a61', font='System 10 bold',
                  fg='White', length=150, variable=iou)
sliderIoU.set(70)
sliderIoU.pack(pady=2, padx=2, side=LEFT)


imgBtnUp = Image.open('appneed/assets/dang.png')
resize_imageUp = imgBtnUp.resize((50, 50))
click_btnUp = ImageTk.PhotoImage(resize_imageUp)


btnUp = Button(frameSecond, borderwidth=0, width=50, height=50,
               image=click_btnUp, background='#353a61',
               activebackground='#353a61',
               command=update_model)
btnUp.pack(pady=2, padx=2, side=LEFT)


imgBtnRes = Image.open('appneed/assets/reset.png')
resize_imageRes = imgBtnRes.resize((50, 50))
click_btnRes = ImageTk.PhotoImage(resize_imageRes)


btnRes = Button(frameSecond, borderwidth=0, width=50, height=50,
                image=click_btnRes, background='#353a61',
                activebackground='#353a61',
                command=reset_model)
btnRes.pack(pady=2, padx=2, side=LEFT)


startbtn["state"] = "active"
btnStop["state"] = "active"
stopbtnPause["state"] = "disabled"
btnDisable["state"] = "disabled"
btnSave["state"] = "disabled"
btnSharpened["state"] = "disabled"
btnNight["state"] = "disabled"

wdw.resizable(False, False)


wdw.mainloop()
