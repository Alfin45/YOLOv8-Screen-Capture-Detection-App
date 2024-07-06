import multiprocessing
from ultralytics import YOLO
from tkinter import *
import numpy as np
import cv2
import os.path
from mss import mss
from PIL import Image, ImageTk
from random import randrange
multiprocessing.freeze_support()

wdw = Tk()
run = False
sharpenOn = False
nightVis = False
acudef = 640
confdef = 25 / 100
ioudef = 70 / 100

infostatus = "IDLE"
wdw.title(".:: FinApp ::.")
wdw.wm_iconbitmap("appneed/assets/appicon.ico")
screen_width = wdw.winfo_screenwidth()
screen_height = wdw.winfo_screenheight()
w = screen_width // 2
h = screen_height
x = w - 5
y = 0
hl = screen_height / 1.5
hl = int(hl)
datCount = 0

# ScreenCapture
sct = mss()

# Model
model = YOLO('appneed/last.pt')

# Window
wdw.geometry("%dx%d+%d+%d" % (w, h, x, y))
wdw['background'] = '#353a61'
desc = 'Screen Capture App with YOLOv8 \n  tkinter, ultralystic, cv2, numpy, mss, PIL'
imagelocation = ["appneed/assets/play.png",
                 "appneed/assets/pause.png",
                 "appneed/assets/disableHome.png",
                 "appneed/assets/enhance.png",
                 "appneed/assets/night.png",
                 "appneed/assets/save.png",
                 "appneed/assets/stopbutton.png",
                 "appneed/assets/dang.png",
                 "appneed/assets/reset.png"
                 ]
listwidget = []
iou = IntVar()
conf = IntVar()
acu = IntVar()
wdw.withdraw()


def makebuttons(imgname, coms, frames):
    buttons = Button(frames, borderwidth=0, width=50, height=50,
                     image=imgname, background='#353a61',
                     activebackground='#353a61',
                     command=coms)
    buttons.pack(pady=2, padx=2, side=LEFT)
    listwidget.append(buttons)


def makelabelinfo(infos):
    labelinfo = Label(frameFirst, text=f"{infos}", background='#000000',
                      fg='#8f9cff', font='System 10 bold', width=50, height=2,
                      borderwidth=5, relief="sunken")
    labelinfo.pack(pady=2, padx=2, side=LEFT)
    listwidget.append(labelinfo)


def makeslider(targetvar, labelslider, setstart):
    sliders = Scale(frameSecond, from_=1, to=100,
                    orient=HORIZONTAL, label=labelslider,
                    bg='#353a61', font='System 10 bold',
                    fg='White', length=150, variable=targetvar)
    sliders.set(setstart)
    sliders.pack(pady=2, padx=2, side=LEFT)
    listwidget.append(sliders)


def resizeimage(imageloc):
    resimg = Image.open(imageloc)
    resizer = resimg.resize((50, 50))
    return resizer


click_btnStart = ImageTk.PhotoImage(resizeimage(imagelocation[0]))
click_btnPause = ImageTk.PhotoImage(resizeimage(imagelocation[1]))
click_btnDisable = ImageTk.PhotoImage(resizeimage(imagelocation[2]))
click_btnSharpened = ImageTk.PhotoImage(resizeimage(imagelocation[3]))
click_btnNight = ImageTk.PhotoImage(resizeimage(imagelocation[4]))
click_btnSave = ImageTk.PhotoImage(resizeimage(imagelocation[5]))
click_btnStop = ImageTk.PhotoImage(resizeimage(imagelocation[6]))
click_btnUp = ImageTk.PhotoImage(resizeimage(imagelocation[7]))
click_btnRes = ImageTk.PhotoImage(resizeimage((imagelocation[8])))


def splashscreen():
    global splashScr
    splashScr = Tk()
    xsplash = (screen_width - 700) // 2
    ysplash = (screen_height - 450) // 2
    splashScr.geometry(f"{700}x{450}+{xsplash}+{ysplash}")
    splashScr.overrideredirect(True)
    splashScr['background'] = '#353a61'
    pesan = ["Times has changed.",
             "Just do it.",
             "Break the limit.",
             "It's just a beginning.",
             "if you can change your mind,\nyou can change your life."
             ]
    gachapesan = randrange(5)
    splashlabelframe = Frame(splashScr, bg='#353a61',
                             highlightbackground="#8f9cff", highlightthickness=5,
                             width=screen_width, height=screen_height)
    splashlabelframe.pack(expand=True, anchor=CENTER)
    splash_label = Label(splashlabelframe, text=f"\" {pesan[gachapesan]} \"", font="System 34 italic",
                         fg="White", justify=CENTER, background="#353a61",
                         width=screen_width, height=screen_height)
    splash_label.pack()
    splashScr.after(5000, destroysplash)


def destroysplash():
    wdw.deiconify()
    splashScr.destroy()


# --
def detect():
    if run:
        global statusUpdate, updateImg, data
        # --
        monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
        img = Image.frombytes("RGB", (w, h), sct.grab(monitor).rgb)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        # Can change the image(convert or filter) before bring up image data to YOLOv8 plotting.
        # But this change gonna effect on detection.
        # Im not using that thing, because my datasets it's only RGB Images.

        if sharpenOn is False and nightVis is False:
            statusUpdate = "DETECTING : NORMAL"
            listwidget[7].config(text=f"{statusUpdate}")
            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated_frame = result[0].plot()
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is False and nightVis is True:
            statusUpdate = "NIGHTVISION NORMAL"
            listwidget[7].config(text=f"{statusUpdate}")
            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated_frame = cv2.cvtColor(result[0].plot(), cv2.COLOR_BGR2HLS)
            data = Image.fromarray(annotated_frame)

        elif sharpenOn is True and nightVis is False:
            statusUpdate = "DETECTING : SHARPEN"
            listwidget[7].config(text=statusUpdate)
            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated = result[0].plot()
            annotated_frame = cv2.filter2D(annotated, -1, kernel * 1.5)
            data = Image.fromarray(annotated_frame)

        else:
            statusUpdate = "NIGHTVISION SHARPEN"
            listwidget[7].config(text=statusUpdate)
            screen = np.array(img)
            result = model(screen, iou=ioudef, conf=confdef, imgsz=acudef)
            annotated = cv2.cvtColor(result[0].plot(), cv2.COLOR_BGR2HLS)
            annotated_frame = cv2.filter2D(annotated, -1, kernel * 1.5)
            data = Image.fromarray(annotated_frame)

        updateImg = ImageTk.PhotoImage(data)
        label.config(image=updateImg)
        wdw.after(1, detect)


def start():
    global run
    run = True
    for startstate in range(7):
        if startstate == 0:
            listwidget[startstate]["state"] = "disable"
        else:
            listwidget[startstate]["state"] = "active"
    wdw.after(1, detect)


def stop():
    global run, statusUpdate
    run = False
    statusUpdate = "PAUSE"
    listwidget[7].config(text=f"{statusUpdate}")
    listwidget[2]["state"] = "active"
    listwidget[1]["state"] = "disabled"
    listwidget[5]["state"] = "active"
    listwidget[0]["state"] = "active"
    listwidget[3]["state"] = "disabled"
    listwidget[4]["state"] = "disabled"


def disable():
    global run, startImg, statusUpdate
    run = False
    startImg = ImageTk.PhotoImage(Image.open('appneed/dat/start.png'))
    label.config(image=startImg)
    statusUpdate = "IDLE"
    listwidget[7].config(text=f"{statusUpdate}")
    for disablestate in range(1, 6):
        listwidget[disablestate]["state"] = "disabled"
    listwidget[0]["state"] = "active"


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
        listwidget[7].config(text=statusUpdate)
    listwidget[1]["state"] = "disabled"
    listwidget[5]["state"] = "disabled"
    listwidget[3]["state"] = "disabled"
    listwidget[0]["state"] = "active"
    listwidget[4]["state"] = "disabled"


def update_model():
    global run, acudef, confdef, ioudef, statusUpdate
    run = False
    statusUpdate = "MODEL CONFIG : UPDATED"
    listwidget[7].config(text=f"{statusUpdate}")
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
    listwidget[2]["state"] = "active"
    listwidget[1]["state"] = "disabled"
    listwidget[5]["state"] = "active"
    listwidget[0]["state"] = "active"
    listwidget[3]["state"] = "disabled"
    listwidget[4]["state"] = "disabled"


def reset_model():
    global run, acudef, confdef, ioudef, statusUpdate
    run = False
    statusUpdate = "MODEL CONFIG : RESET"
    listwidget[7].config(text=f"{statusUpdate}")
    acudef = 640
    confdef = 25 / 100
    ioudef = 70 / 100
    listwidget[8].set(1)
    listwidget[9].set(25)
    listwidget[10].set(70)
    listwidget[2]["state"] = "active"
    listwidget[1]["state"] = "disabled"
    listwidget[5]["state"] = "active"
    listwidget[0]["state"] = "active"
    listwidget[3]["state"] = "disabled"
    listwidget[4]["state"] = "disabled"


def quit_tk():
    global statusUpdate, updateImg, run
    run = False
    statusUpdate = ".:: GOODBYE ::."
    listwidget[7].config(text=statusUpdate)
    for quitstate in range(7):
        listwidget[quitstate]["state"] = "disabled"
    for quitstate2 in range(11, 13):
        listwidget[quitstate2]["state"] = "disabled"
    updateImg = ImageTk.PhotoImage(Image.open('appneed/dat/start.png'))
    label.config(image=updateImg)
    wdw.after(3000, exitprog)


def exitprog():
    wdw.destroy()
    exit()


# Create Widget
desc_label = Label(wdw, background='#353a61', font='System 18 bold',
                   fg='#8f9cff', text=desc)
desc_label.pack(pady=2)
im = Image.open('appneed/dat/start.png')
updateImg = ImageTk.PhotoImage(im)
label = Label(wdw, width=w, height=hl, borderwidth=5,
              relief="sunken", image=updateImg)
label.pack()
# Frames
frameFirst = Frame(wdw, bg='#353a61')
frameFirst.pack(expand=False, anchor="nw")
frameSecond = Frame(wdw, bg='#353a61', highlightbackground="white", highlightthickness=1)
frameSecond.pack(expand=False, anchor="nw")
makebuttons(click_btnStart, lambda: start(), frameFirst)
makebuttons(click_btnPause, lambda: stop(), frameFirst)
makebuttons(click_btnDisable, lambda: disable(), frameFirst)
makebuttons(click_btnSharpened, lambda: sharpenedimg(), frameFirst)
makebuttons(click_btnNight, lambda: nightvision(), frameFirst)
makebuttons(click_btnSave, lambda: saveimg(), frameFirst)
makebuttons(click_btnStop, lambda: quit_tk(), frameFirst)
makelabelinfo(infostatus)
makeslider(acu, "Accuracy", 1)
makeslider(conf, "Confidence", 25)
makeslider(iou, "IoU", 70)
makebuttons(click_btnUp, lambda: update_model(), frameSecond)
makebuttons(click_btnRes, lambda: reset_model(), frameSecond)
listwidget[0]["state"] = "active"
listwidget[6]["state"] = "active"
for i in range(1, 6):
    listwidget[i]["state"] = "disabled"

wdw.after(1, splashscreen)
wdw.resizable(False, False)
mainloop()
