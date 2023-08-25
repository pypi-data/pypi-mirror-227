#!/usr/bin/env python3

# there is tuning of the size------

# import the necessary packages

# -----this is some repair of avi?
#  ls zen_192.168.0.91_20211105_* |
# while read line; do echo file \'$line\'; done |
# ffmpeg -protocol_whitelist file,pipe -f
# concat -i - -c copy zen_192.168.0.91_20211105_.avi
#
#

from flashcam.version import __version__

# from imutils.video import VideoStream
import socket
import time
import signal
from contextlib import contextmanager

# import argparse

import cv2
import datetime

# import datetime as dt

import os


from fire import Fire

# import imutils

import urllib.request
import numpy as np

# user pass
import base64

import getpass

import sys

from flashcam.stream_enhancer import Stream_Enhancer
import webbrowser

import math

import requests  # crosson=CROSSON

# ------------------problem with SHIFT
# from pynput.keyboard import Key, Listener


global SHIFT, CTRL
SHIFT = CTRL = False

global centerX1, centerY1
global FILE_USERPASS
global FILE_REDCROSS
# ---------- files:
FILE_USERPASS = "~/.config/flashcam/.flashcam_upw"  # will extend
FILE_REDCROSS = "~/.config/flashcam/crossred"  # will extend


global local_gamma, integrate
local_gamma = 1  # adjust_gamma
integrate = 1  # call accum

# automatic tuning histogram
global countdownpause, optimgain, optimexpo, optim_histo, countdown_gain
countdownpause = 5
optimgain = -1
optimexpo = -1
optim_histo = 49  # we try middle of the range in %
countdown_gain = False  # Sonix USB 0c45:62c0 has broken expo, but gain ok

jpgkompr2 = [100, 95, 90, 80, 70, 60, 50, 40, 30,20,10, 5]
jpgkompr1 = [x for x in jpgkompr2]


# i needed a warning before 't'
global allow_tracker, allow_tracker_demand
allow_tracker = False
allow_tracker_demand = False

global show_help
show_help = False


# x ... expand 2x ... buggy
HELPTEXT = """ a/A ... AVI/stop (~/DATA/) (ctl-a PNG stream)
 s/S ... save 1 JPG (PNG) (to ~/DATA/) (C-p remote PNG)

 z ... cycle zoom 2x (mouse click fixes the center)
 Z ... zoom 1x
 r/R ... rotate by +-1; Ctl-r= 180 degrees

 c/C ... red cross on/off (save when off)
 hjkl ... move the red/green* cross (HJKL)
 t/u ... tracker 1 (cross sync, speed)
 T/u ... tracker 2 (more steady, but fragile)

 m/M ... measure/not distance,  (-v 110,1.2)
 n/N ... inc/decrease distance
 f/F ... inc/dec Field Of View (-v FOV,dist)

 v/V* ... green cross ON/OFF
 b/f* ... substract BG, mix FG
 B/F* ... SAVE BG/ SAVE FG

 egy* ...  expo/gain/gm (+ shift or ctl)
 d   ...  gamma (local) (+shift or ctl)
 o/O ... autotune expo / break tuning
 i/I* ... accumulate images

 w ... open web browser
 q ... quit           ? ... HELP
ctl: t=kompr  h=histo  j=direct  k=detect
       * with remote flashcam server """





def rotate_image(image, angle):
    if angle is None:     return image
    if abs(angle)<0.1:     return image
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    # print( "rotate", image_center, angle )
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    #print(rot_mat)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    #print("rotated by ", angle)
    return result



# NOT IN UBUNTU22
def kb_on_press(key):
    global SHIFT, CTRL
    print("                                              =v=")
    try:
        a = key.char
        # print('alphanumeric key {0} pressed'.format( key.char))
        # CTRL  = False
    except AttributeError:
        print('special key {0} pressed'.format(  key))
    if key == Key.alt:
        CTRL = True
    if key == Key.shift:
        SHIFT = True
    return

# NOT ON UBUNTU22
def kb_on_release(key):
    global SHIFT, CTRL
    print("                                              =^=")
    if key == Key.alt:
        CTRL = False
    if key == Key.shift:
        SHIFT = False
    print('{0} released'.format( key))
    if key == Key.esc:
        # Stop listener
        return False


def remap_keys(key):
    """
    Problem - THIS TABLE WORKS ON  gigajm
        , while zen : 65505
    """
    global CTRL
    CTRL=False
    print(f" ... remap_keys()  KEY==/{key}/", CTRL)
    if key>=262241 and key<=262266:CTRL=True  # zen
    if key>=1310817 and key<=1310842:CTRL=True # zaba

    print(f" ... remap_keys()  KEY==/{key}/ ", CTRL)
    table = {
        262241: "a", # zen ctrl
        262242: "b", # zen ctrl
        262243: "c", # zen ctrl
        262244: "d", # zen ctrl
        262245: "e", # zen ctrl
        262246: "f", # zen ctrl
        262247: "g", # zen ctrl
        262248: "h", # zen ctrl
        262249: "i", # zen ctrl
        262250: "j", # zen ctrl
        262251: "k", # zen ctrl
        262252: "l", # zen ctrl
        262253: "m", # zen ctrl
        262254: "n", # zen ctrl
        262255: "o", # zen ctrl
        262256: "p", # zen ctrl
        262257: "q", # zen ctrl
        262258: "r", # zen ctrl
        262259: "s", # zen ctrl
        262260: "t", # zen ctrl
        262261: "u", # zen ctrl
        262262: "v", # zen ctrl
        262263: "w", # zen ctrl
        262264: "x", # zen ctrl
        262265: "y", # zen ctrl
        262266: "z", # zen ctrl


        1310817: "a", #ctrl zaba
        1310818: "b", #ctrl zaba
        1310819: "c", #ctrl zaba
        1310820: "d", #ctrl
        1310821: "e", #ctrl
        1310822: "f", #ctrl zaba
        1310823: "g", #ctrl zaba
        1310824: "h", #ctrl zaba
        1310825: "i", #ctrl zaba
        1310826: "j", #ctrl zaba
        1310827: "k", #ctrl zaba
        1310828: "l", #ctrl zaba
        1310829: "m", #ctrl zaba
        1310830: "n", #ctrl zaba
        1310831: "o", #ctrl zaba
        1310832: "p", #ctrl zaba
        1310833: "q", #ctrl zaba
        1310834: "r", #ctrl zaba
        1310835: "s", #ctrl zaba
        1310836: "t", # ctrl
        1310837: "u", # ctrl
        1310838: "v", # ctrl
        1310839: "w", # ctrl
        1310840: "x", # ctrl
        1310841: "y", # ctrl
        1310842: "z", # ctrl

        1114175: "?", # zaba
        65599: "?", # zen

        1048673: "a",
        1048674: "b",
        1048675: "c",
        1048676: "d",
        1048677: "e",
        1048678: "f",
        1048679: "g",
        1048680: "h",
        1048681: "i",
        1048682: "j",
        1048683: "k",
        1048684: "l",
        1048685: "m",
        1048686: "n",
        1048687: "o",
        1048688: "p",
        1048689: "q",
        1048690: "r",
        1048691: "s",
        1048692: "t",
        1048693: "u",
        1048694: "v",
        1048695: "w",
        1048696: "x",
        1048697: "y",
        1310841: "y", #ctrl
        1048698: "z",
        1114177: "A",
        1114178: "B",
        1114179: "C",
        1114180: "D",
        1114181: "E",
        1114182: "F",

        65601: "A", # zen
        65602: "B", #zen
        65603: "C", # zen
        65604: "D",
        65605: "E",
        65606: "F", # zen
        65607: "G",
        65608: "H",
        65609: "I",
        65610: "J",
        65611: "K",
        65612: "L",
        65613: "M",
        65614: "N",
        65615: "O",
        65616: "P",
        65617: "Q",
        65618: "R",
        65619: "S",
        65620: "T",
        65621: "U",
        65622: "V",
        65623: "W",
        65624: "X",
        65625: "Y",
        65626: "Z",

        1114183: "G",
        1114184: "H",
        1114185: "I",
        1114186: "J",
        1114187: "K",
        1114188: "L",
        1114189: "M",
        1114190: "N",
        1114191: "O",
        1114192: "P",
        1114193: "Q",
        1114194: "R",
        1114195: "S",
        1114196: "T",
        1114197: "U",
        1114198: "V",
        1114199: "W",
        1114200: "X",
        1114201: "Y",
        1114202: "Z",
    }
    # 1.  I deactivate ALL above keys to avoid duplicity for arrows etc...
    #
    #
    # 2. I use these ctrl-
    # ctrle     1310821:''
    # (key == 1310823): # ctrlg
    #         1310841): #ctrly
    # ctrla

    # ####return table[key]
    if key in table:
        key = ord(table[key])
        # keynew = table[key]
        # #print(f"in remaping {key} - {keynew}")
        # #return keynew
    return key


# -------------------- DISPLAY MULTITEXT ---------------------
def disp_mutext(lena, wrapped_text_o):
    lena = np.array(lena)  # I turn to np.array
    lena = lena / 255

    size = lena.shape
    wrapped_text = wrapped_text_o.split("\n")

    img = np.zeros(size, dtype="uint8")
    img = img + 0.0  # +0.9 # whitish
    # print("npzero",img.shape, img)

    height, width, channel = img.shape

    # never used text_img = np.ones((height, width))
    # print(text_img.shape)
    font = cv2.FONT_HERSHEY_SIMPLEX

    x, y = 10, 40
    font_size = 0.4
    font_thickness = 1

    i = 0

    textsize1 = 1
    textsize0 = 1

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        if textsize[0] > textsize0:
            textsize0 = textsize[0]
        if textsize[1] > textsize1:
            textsize1 = textsize[1]

    #    wrapped_text.append( " "*textsize1+"[OK]" )
    # print(    wrapped_text )

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        if textsize[0] > textsize0:
            textsize0 = textsize[0]
        if textsize[1] > textsize1:
            textsize1 = textsize[1]
    # ----- after finding the text sizes; define gap

    gap = textsize1 + 6

    nlines = len(wrapped_text)
    offx = 0 + int((img.shape[1] - textsize0) / 2)
    offy = 0 + int((img.shape[0] - gap * (nlines - 1)) / 2)

    pad = 10
    start_point = (offx - pad, offy - pad - textsize1)
    start_point2 = (offx - pad, offy - pad - textsize1 + int(pad / 2))
    end_point = (pad + offx + textsize0, offy + gap * len(wrapped_text))
    end_point2 = (pad + offx + textsize0, offy + gap * len(wrapped_text) - int(pad / 2))

    img = cv2.rectangle(img, start_point, end_point, (0.2, 0.2, 0.2), -1)

    img = cv2.rectangle(img, start_point, end_point, (-1, -1, -1), 1)  # trick
    img = cv2.rectangle(img, start_point2, end_point2, (-1, -1, -1), 1)

    for line in wrapped_text:
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        # print(textsize)
        # gap = textsize[1] + 5
        # gap = textsize1 # gap define earlier

        y = int((img.shape[0] + textsize[1]) / 2) + i * gap
        x = 10  # for center alignment => int((img.shape[1] - textsize[0]) / 2)
        x = offx
        y = offy + i * gap

        cv2.putText(
            img,
            line,
            (x, y),
            font,
            font_size,
            #                (255,255,255),
            (-1, -1, -1),  # BIG TRICK
            font_thickness,
            lineType=cv2.LINE_AA,
        )
        i += 1

    # -------------------- howto merge with frame........
    img = lena - img

    # print("min", img.min()  , "max=",img.max()  )
    img = np.clip(img, 0.0, 1.0, None)  # for dark img values, clip to 0
    # img = img / img.max()
    # print("min", img.min()  , "max=",img.max()  )

    img = img * 255  # i dont know how to make int
    img = img.astype(np.uint8)  # this makes negative to positive
    # print(img)
    return img


@contextmanager
def timeout(atime):
    # register a function to raise a TimeoutError on the signal
    signal.signal(signal.SIGALRM, raise_timeout)
    # schedule the signal to be sent after 'time'
    signal.alarm(atime)
    # print("D... timeout registerred")

    try:
        # tok = False
        # print("D... yielding timeout")
        yield
    finally:
        # tok = True
        # unregister the signal so it wont be triggered
        # if the timtout is not reached
        # print("D... timeout NOT!  unregisterred")
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def img_estim(img, thrshld=127):
    res = np.mean(img)
    return res
    is_light = res > thrshld
    return "light" if is_light else "dark"
    # 40 -> 2.2


# ------------------------------------------------------------------------ 3
# ================================================================================================

# ================================================================================================


def display2(
    videodev,
    save=False,
    passfile="~/.pycamfw_userpass",
    rotate=0,
    vof="99,2",
    savepngcont=False,
    XY=None,
):
    """ """
    # sname,sfilenamea,sme,sfilenamea,sfilenamea,sfourcc,saviout

    sme = socket.gethostname()
    # frame = None  #  gigavg a vaio have strange behaviour

    global jpgkompr1, jpgkompr2
    global CTRL, SHIFT
    global centerX1, centerY1, clicked
    global FILE_USERPASS, FILE_REDCROSS
    global show_help
    global allow_tracker, allow_tracker_demand
    global local_gamma, integrate
    global countdown_gain
    centerX1, centerY1, clicked = 0, 0, True  # center zoom ion start

    filesource = False

    # ==========================  I fire here the listener from pynput !!!
    # NOT ON UBUNTU22 ############################################################
    #listener = Listener(on_press=kb_on_press, on_release=kb_on_release)
    #listener.start()
    # ------------------------------------------------------ let;s see

    def MOUSE(event, x, y, flags, param):
        global centerX1, centerY1, clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked = not clicked
        if event == cv2.EVENT_MOUSEMOVE:
            if not (clicked):
                centerX1, centerY1 = x, y
            # print('({}, {})'.format(x, y))
            # imgCopy = frame.copy()
            # cv2.circle(imgCopy, (x, y), 5, (255, 0, 0), -1)
            # cv2.imshow('image', imgCopy)

    """


{
“avi” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v”, “XVID” ],
“mov” : [ “avc1”, “DIVX”, “mp4v”, “XVID” ],
“mp4” : [ “avc1”, “mp4v” ],
“mkv” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v”, “XVID” ],
“mkv” : [ “avc1”, “DIVX”, “H264”, “X264”, “V264”, “IYUV”, “MJPG”, “MPEG”, “MP42”, “mp4v” ],
“3gp” : [ “avc1”, “mp4v” ]
}


Notes:
– avc1 is equivalent/identical to H264, X264, V264
– mp4v is the same as DIVX, XVID

File size & compression
– most compact format: avc1
– least compact format is IYUV (by a long shot), followed by MPJPG/MPEG
– middle/similar: MP42, mp4v

Recommendation:
– use avi or mkv for best compatibility across all codecs for the maximum flexibility
– use mp4 (avc1, mp4v) for compatibility across players with most/reasonable compression

"""

    def setupsave(resolution=(640, 480)):
        sname = "rec"
        sname = videodev
        sname = sname.replace("http", "")
        sname = sname.replace("//", "")
        sname = sname.replace(":", "")
        sname = sname.replace("5000/video", "")
        sname = sname.replace("8000/video", "")

        sfilenamea = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        sme = socket.gethostname()
        sfilenamea = f"{sme}_{sname}_{sfilenamea}"
        #
        # DEFINE EXTENSION : avi+xvid     mov  mp4 mpg
        #   avi+x264
        #
        # sfilenamea = f"{sfilenamea}.mp4"
        # sfilenamea = f"{sfilenamea}.mp4"
        sfilenamea = f"{sfilenamea}.mkv"

        # XVID-works     LAGS   X264    MP4V? mp4v-new,ubu22    IYUV-huge
        CODEC = "mp4v"

        dir2create = os.path.expanduser("~/DATA/")
        if not os.path.isdir(os.path.expanduser(dir2create)):
            print(f"D... trying to create directory {dir2create} for saving")
            # result = False
            os.mkdir(os.path.expanduser(dir2create))

        sfilenamea = os.path.expanduser("~/DATA/" + sfilenamea)
        # codec
        # sfourcc = cv2.VideoWriter_fourcc(*'XVID')
        # ### sfourcc = cv2.VideoWriter_fourcc(*'LAGS') # lossless NOT mkv,avi
        # sfourcc = cv2.VideoWriter_fourcc(*'X264') # +avi small NOTubu22
        # sfourcc = cv2.VideoWriter_fourcc(*'mp4v') # works on UBU22 clean inst
        # ####sfourcc = cv2.VideoWriter_fourcc(*'MP4V')
        # ####sfourcc = cv2.VideoWriter_fourcc(*'IYUV') # huge + avi

        sfourcc = cv2.VideoWriter_fourcc(*f"{CODEC}")  #

        #  25 FPS
        saviout = cv2.VideoWriter(sfilenamea, sfourcc, 25.0, resolution)
        for i in range(4):
            print(f"SAVE={sfilenamea} ---  FOURCC={CODEC}")
        return sfilenamea, saviout

    def get_stream():
        global CTRL, SHIFT
        # localuser
        global FILE_USERPASS, FILE_REDCROSS
        stream = None  # i return
        u, p = getpass.getuser(), "a"

        # this is bug.... never find passfile
        if "passfile" in locals():
            if passfile is None:
                print(f"i... nO passfile...trying {videodev} , {passfile}")
                passfile = videodev.strip("http://")
                print("i... TRYING", passfile)
        else:
            passfile = videodev.strip("http://")
            passfile = passfile.strip("/video")
            passfile = passfile.split(":")[0]

            # WITH A HACK  -  I REDEFINE REDCROSS too
            FILE_REDCROSS = f"{FILE_REDCROSS}_{passfile}.txt"

            passfile = f"{FILE_USERPASS}_{passfile}"
            print(f"i... TRYING {videodev} PASS: {passfile}")

        try:
            with open(os.path.expanduser(passfile)) as f:
                print("YES---> PASSWORD FILE  ", passfile)
                w1 = f.readlines()
                u = w1[0].strip()
                p = w1[1].strip()
        except:
            print("NO PASSWORD FILE (gs) ")

        print("D... capturing from: /{}/".format(videodev))
        # cam = cv2.VideoCapture( videodev )
        # stream = urllib.request.urlopen( videodev )

        request = urllib.request.Request(videodev)
        print("D... USER/PASS", u, p)
        base64string = base64.b64encode(bytes("%s:%s" % (u, p), "ascii"))
        print("D... stream ok1", base64string)
        request.add_header("Authorization", "Basic %s" % base64string.decode("utf-8"))

        # request.add_header("Authorization", "Basic %s" % base64string)
        print("D... stream ok2 - request.urlopen (disp)")
        ok = False
        try:
            stream = urllib.request.urlopen(
                request, timeout=3
            )  # timeout to 7 from 5 sec.
            ok = True
            filesource = True
            print("D... stream ok3")
        except urllib.error.HTTPError as e:
            print("Server Offline1? ", e)
            print(videodev)
            # do stuff here
        except urllib.error.URLError as e:
            print("Server Offline2? ", e)
            print(videodev)
            # do stuff here
        except:
            ok = False
            stream = None
            print("X.... Timeouted on URLOPEN")

        return stream, u, p

    # ********************************************************** main loop
    io_none = 0  # to reset stream
    sfilename = ""  # move up to limi # of AVI files.... tst?
    sfilenamea = ""

    stream_length = 1024 * 50  # i had 50k all the time from 1st working versn
    stream_length = 1024 * 15  #

    if save:
        sfilenamea, saviout = setupsave()
    while True:  # ==================== MAIN LOOP =================
        mjpg = False

        # #===================== OPENCV START CAPTURE==========================

        bytex = b""  # stream
        rpi_name = videodev
        frame_num = 0

        if (str(videodev).find("http://") == 0) or (
            str(videodev).find("https://") == 0
        ):
            # infinite loop for stream authentication
            stream = None
            while stream is None:
                print("D... waiting for stream")
                # ## HERE PUT BWIMAGE
                # cv2.imshow(rpi_name, frame) # 1 window for each RPi
                if "frame" in locals():
                    print("D... frame in locals() ")
                    if frame is not None:
                        print("D.... graying")
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                        (w, h, c) = frame.shape

                        for i in range(0, w, 10):
                            x1, y1 = 0, i
                            x2, y2 = h, i
                            line_thickness = 1
                            cv2.line(
                                gray,
                                (x1, y1),
                                (x2, y2),
                                (111, 111, 111),
                                thickness=line_thickness,
                            )
                        cv2.imshow(rpi_name, gray)  # 1 window for each RPi
                        key = cv2.waitKey(1)

                time.sleep(1)
                stream, u, p = get_stream()
        else:
            print("X... use http:// address")
            print("i... or this may be a file?...")
            # sys.exit(0)

        if (str(videodev).find("http://") == 0) or (
            str(videodev).find("https://") == 0
        ):
            ret_val = 0
            oi = 0
            while ret_val == 0:
                oi += 1

                # with timeout(2):
                print("D... IN 1st TIO..", end="")
                try:
                    # THIS CAN TIMEOUT #######################################
                    print("D... try ...", end="")
                    bytex += stream.read(stream_length)  # must be long enou?
                except:
                    print("X... exception - timout in 1.st stream.read, ")
                    # bytex+=b"\x00\x00\x00"
                    bytex = b""

                a = bytex.find(b"\xff\xd8")  # frame starting
                b = bytex.find(b"\xff\xd9")  # frame ending
                if a != -1 and b != -1:
                    io_none = 0
                    jpg = bytex[a: b + 2]
                    bytex = bytex[b + 2:]
                    # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                    # cv2.CV_LOAD_IMAGE_COLOR)
                    if len(jpg) > 1000:  # was crash here
                        frame = cv2.imdecode(
                            np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR
                        )
                        ret_val = 1
                        io_none = 0
                        stream_length = int((b + 2 - a) / 2)  # expected length
                    else:
                        ret_val = 0
                        # print("D...              ok frame http",oi,len(bytex) )
                else:
                    ret_val = 0
                    print(
                        "D...                        frame set None http",
                        oi,
                        len(bytex),
                        end="\r",
                    )
                    # it can count to milions here.... why? need to check
                    #          stream ## OTHER CRASHES
                    #  i try two things now:
                    # bytex+=b""
                    time.sleep(0.2)
                    io_none += 1
                    if io_none > 50:
                        stream = None
                        print(
                            "X... ---------------  too many unseen frames",
                            io_none,
                            "breaking",
                        )
                        io_none = 0
                        break

                    # frame = None
        if "stream" in locals():
            if stream is None:
                continue
        else:  # from file ---- 1st moment open
            # replay video from file
            ret_val = 0
            stream = cv2.VideoCapture(videodev)
            filesource = True
            print("i... FILE open  = ", stream.isOpened())
            ok, frame = stream.read()
            frame_num += 1
            # pause = True too early.... defined later
            print(f"X... {ok}, frame from {videodev}")
            # print("i... stream in locals() == ", 'stream' in locals() )
            # print("i... stream is None     == ", stream is None, stream )
            print("i...   PAUSED: press SPACE to play")

        # ----------------------------------------------------------------

        first = True

        timestamp_of_last_socket_refresh = time.time()

        i = 0
        fps = 0
        resetfps = True
        lastminu = 88
        motion_last = "999999"

        i7 = 0
        artdelay = 0.05

        connection_ok = True

        # ---- bytes per second.  strange looks like 7MB/s
        BPS = 0
        BPSlast = 0
        BPStag = datetime.datetime.now()
        FPS = 0
        FPSlast = 0
        frames_total = 0
        frame_num = 0

        senh = Stream_Enhancer()
        saved_jpg = 0  # 0, 1jpg, 2png

        zoomme = 1
        centerX1, centerY1 = 320, 240
        expande = 1
        rorate180 = False

        # measurements (distance)
        measure = 0  # 1.7

        #print(vof, type(vof))
        #print(vof)
        #print(vof)
        if type(vof) is list: # never happened
             measure_fov, measure  = vof[0], vo[1]
        elif str(vof).find(",") > 0: # this happens
            vof = str(vof).strip("(")
            vof = str(vof).strip(")")
            vof = str(vof).strip("[") # when cfg from memory does this
            vof = str(vof).strip("]")
            measure_fov, measure  = (float(vof.split(",")[0]), float(vof.split(",")[1]) ) # ??? BUG?
            print("D... measure == ", measure )
            float(vof.split(",")[1])
        else:
            measure_fov = float(vof)  # config.CONFIG['vof'] #

        cross = None
        greencross = False  # just tell if on/off

        print(" ... ... reset of all trackers/zoom/measure etc..")

        tracker1 = None
        tracker2 = None
        tracker1_fname = None  # change filename for tracking
        tracker2_fname = None  # change filename for tracking
        tracker_list = []
        cropped = None  # created during tracking1
        orb = None  # i dont use

        # file - pause
        pause = True  # FOR FILE but not for CAM
        if filesource is False:
            pause = False
        frame_from_file = None  # backup the frame: for effects + for CAMER

        # -see the values sent from the webpy - i can use in track,
        #   but not in savejpg,saveavi!
        webframen = ""  # frame number from web.py()
        webframetime = ""

        save_decor = False # save with decor or original... save is def in call...

        while connection_ok:  # ===============================================
            # read the frame from the camera and send it to the server
            # time.sleep(0.05)

            # while True:
            if (str(videodev).find("http://") == 0) or (
                str(videodev).find("https://") == 0
            ):
                print("-", end="")
                artdelay = 0
                ret_val = 0
                try:
                    with timeout(4):
                        while ret_val == 0:
                            for i8 in range(1):  # I decimate and remove delay
                                # print("1-", flush=True,end="")
                                bytex += stream.read(stream_length)
                                a = bytex.find(b"\xff\xd8")  # frame starting
                                b = bytex.find(b"\xff\xd9")  # frame ending
                                ttag = bytex.find(
                                    "#FRAME_ACQUISITION_TIME".encode("utf8")
                                )  # frame ending
                                webframen = " " * 7
                                webframetime = " " * 23
                                if ttag != -1:
                                    # print(f"i... FRACQT: /{ttag}/ \
                                    # /{bytex[ttag:ttag+32]}/----------------")
                                    webframen = bytex[ttag: ttag + 32 + 23].decode(
                                        "utf8"
                                    )
                                    webframen = webframen.split("#")
                                    # print(len(webframen), webframen)
                                    webframen, webframetime = webframen[2], webframen[3]

                                    # print( webframen )
                                    # print( webframetime)

                                if a != -1 and b != -1:
                                    jpg = bytex[a: b + 2]
                                    BPS += len(jpg) / 1024
                                    if len(jpg) > 0:
                                        FPS += 1
                                    bytex = bytex[b + 2:]
                                    # just a test.... if I can append
                                    # jpg = jpg+b'#FRAME_ACQUISITION_TIME#'+
                                    # f"a".encode("utf8")
                                    frame = cv2.imdecode(
                                        np.frombuffer(jpg, dtype=np.uint8),
                                        cv2.IMREAD_COLOR,
                                    )

                                    # ----taken for pause
                                    if (not pause) or (frame_from_file is None):
                                        frame_from_file = frame
                                        frame_num += 1
                                    else:
                                        frame = frame_from_file
                                        # ret_val = 1
                                        # frame_num+=1 # ??? I keep this stopped or better not?

                                    # stream_length = b+2-a
                                    stream_length = int(
                                        (b + 2 - a) * 0.9
                                    )  # expected length

                                    ret_val = 1
                                    #print( f"{stream_length/1024:.1f}k #{frame_num:06d}/{webframen} {BPSlast*8/1024:4.1f}Mb/s {FPSlast:2d}fps" , end = "\r" )
                                    print( f"{stream_length/1024:.1f}k #{frame_num:06d}/{webframen} {BPSlast*8/1024:4.1f}Mb/s {FPSlast:2d}fps cap={webframetime} now={str(datetime.datetime.now())[11:-4]}  {sfilenamea.replace('/home/', '')}", end = "\r" )
                                        # "{:.1f}k #{:06d}/{} {:4.1f}Mb/s {:2d}fps {} w{} {} ".format(
                                        #     # len(bytex)/1024,
                                        #     stream_length / 1024,
                                        #     frame_num,
                                        #     webframen,
                                        #     BPSlast * 8 / 1024,
                                        #     FPSlast,
                                        #     str(datetime.datetime.now())[11:-4],
                                        #     webframetime[11:],
                                        #     sfilenamea.replace("/home/", ""),

                                        # ),
                                        # end="\r",               )

                                else:
                                    ret_val = 0
                                    # frame = None
                                    # print("Non  sizE={:6.0f}kB ".format(len(bytex)/1024), end = "\r" )
                                    # print("Non", end = "\r" )
                except:
                    print("X... exception - connection lost, ")
                    ret_val = 0
                    # frame = None
                    print("RDE  siZe={:6.0f}kB ".format(len(bytex) / 1024), end="\n")
                    connection_ok = False

                # print("-2", flush=True,end="")
                if (datetime.datetime.now() - BPStag).total_seconds() > 1:
                    BPStag = datetime.datetime.now()
                    BPSlast = BPS
                    BPS = 0
                    FPSlast = FPS
                    FPS = 0

                # while

            else:  # from file 2nd point
                if (not pause) or (frame_from_file is None):
                    ret_val, frame = stream.read()
                    frame_from_file = frame
                    frame_num += 1
                else:
                    frame = frame_from_file
                    ret_val = 1
                if ret_val == 0:
                    sys.exit(0)
            if connection_ok:
                if (ret_val == 0) or (type(frame) == "NoneType"):
                    print("Not a good frame", type(frame), end="\r")
                    continue
                frame = frame
                (w, h, c) = frame.shape
                frame_area = w * h
                motion_det = False

                # print(".", end="")
                # print("RPINAME=",rpi_name)
                # print(frame)

                wname = videodev

                frames_total += 1

                # ======================================== GAMES WITH FRAMES
                #   hack-expand;  tracker; zoom; rotate; save; measure

                # cv2.namedWindow( wname, cv2.WINDOW_KEEPRATIO ,cv2.WINDOW_GUI_EXPANDED)
                #
                # cv2.WINDOW_KEEPRATIO 2 may allow resize on gigavg
                # but troja...
                #
                # https://stackoverflow.com/a/43497012
                #

                # cv2.namedWindow( wname , cv2.WINDOW_KEEPRATIO ) #
                # QT cv2.namedWindow( wname , cv2.WINDOW_GUI_NORMAL + cv2.WINDOW_OPENGL  ) #
                # try this
                # cv2.namedWindow( wname , cv2.WINDOW_KEEPRATIO ) # 2 may allow resize on gigavg
                # NEW IN 1.1.8
                cv2.namedWindow(wname, cv2.WINDOW_GUI_NORMAL)  #
                # cv2.namedWindow( wname , 2 ) # 2 may allow resize on gigavg
                if frames_total < 2:
                    # cv2.namedWindow(wname,cv2.WND_PROP_FULLSCREEN)
                    # ?https://stackoverflow.com/questions/62870031/pixel-coordinates-and-colours-not-showing
                    # TRICK !!!!!!!!!!!!
                    # https://stackoverflow.com/a/52776376
                    #  remove bars....  BUT IN UBUNTU 22 - I remove this and all is fine
                    #cv2.setWindowProperty( wname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN  )

                    #cv2.setWindowProperty( wname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN  )
                    bit_fs = 0
                    if sme in [
                        "gigavg",
                        "vaio",
                    ]:  # strange behavior on some PC concerning resize...(checked in MS with vadim)
                        bit_fs = 1
                    cv2.setWindowProperty(wname, cv2.WND_PROP_FULLSCREEN, bit_fs)
                    cv2.resizeWindow(wname, frame.shape[1], frame.shape[0])
                    if XY is not None:
                        xy1, xy2 = XY.split("x")
                        cv2.moveWindow(wname, int(xy1), int(xy2))

                # -------- i tried all---no help for csrt tracking-------
                # -------- i tried all---no help for csrt tracking-------
                # -------- i tried all---no help for csrt tracking-------
                # frame = cv2.bilateralFilter(frame,5,100,20) # preserve edges
                # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                # (T,frame) = cv2.threshold(frame,  100, 255,
                #                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                # frame = cv2.blur( frame, (6,6) ) # doesnt help

                # ======================== track before zoom
                if (tracker1 is not None) and (not pause):
                    # print("tracking",tracker1)
                    ok, bbox = tracker1.update(frame)
                    if not ok:
                        continue
                    bbox = [round(i * 10) / 10 for i in bbox]
                    (x, y, w, h) = [v for v in bbox]
                    cx, cy = round(10 * (x + w / 2)) / 10, round(10 * (y + h / 2)) / 10
                    # print("tracking",ok,bbox," ->", cx,cy)
                    with open(tracker1_fname, "a") as f:
                        f.write(f"{webframetime} {webframen} {cx} {cy}\n")
                        #   f.write( f"{webframetime[11:]} {webframen} {cx} {cy}\n" )

                    # there is time sent from server... by a trick
                    #
                    # if from file(or elsewhere) it is int or nothing...
                    #
                    if (type(webframen) == int) or (webframen.strip(" ") == ""):
                        # no acq timestamp info from server
                        webframen = frame_num
                        ttime = int(webframen)
                    else:
                        # better this, fractions are kept...
                        ttime = datetime.datetime.strptime(
                            webframetime, "%Y-%m-%d %H:%M:%S.%f"
                        )

                    tracker_list.append((round(cx), round(cy), ttime))
                    colmax = 255
                    colmaxb = 0
                    for i in reversed(tracker_list):
                        x2, y2, ttime = i
                        frame[y2, x2] = (colmaxb, 255 - colmax - colmaxb, 255)
                        if colmax > 1:
                            colmax -= 1
                        elif (colmaxb < 255) and (colmaxb > 1):
                            colmaxb += 1

                    # ------------ play on cropping -- may further stabilize
                    cropped = frame[round(y) : round(y + h), round(x) : round(x + w)]
                    # normalize region-   problems/crashes on pause
                    # resu = np.zeros((640,480))
                    # cropped = cv2.normalize(cropped, resu,0,255,cv2.NORM_MINMAX)
                    #    gray
                    # #cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
                    # #cropped = cv2.blur( cropped, (2,2) )
                    # #(T,cropped) = cv2.threshold(cropped,  100, 255,  cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    # merge back to BGR
                    # #cropped = cv2.merge([cropped,cropped,cropped] )

                    # # return cropped to main image -------------- problem on pause+normalize
                    # frame[round(y):round(y+h), round(x):round(x+w)] = cropped

                    # ---ORB feature matching...
                    # cropped = frame[round(y):round(y+h), round(x):round(x+w)]
                    # kp,des = orb.detectAndCompute(cropped,None)
                    # frame[round(y):round(y+h), round(x):round(x+w)] = cv2.drawKeypoints(cropped,kp,None)

                    # --- ups
                    # if not( (x<0)or(y<0)or(x+w>=frame.shape[1])or(y+h>=frame.shape[0]) ):
                    # print("rect")

                    # # - the other part HSV histo ---- HISTO TRACKING
                    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    # dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
                    # ret, track_window = cv2.meanShift(dst,track_window, term_crit)
                    # xh,yh,wh,hh = track_window

                    cv2.rectangle(
                        frame,
                        (round(x), round(y)),
                        (round(x + w), round(y + h)),
                        (0, 255, 0),
                        1,
                        1,
                    )
                    cv2.line(
                        frame,
                        (round(cx), round(cy)),
                        (round(cx), round(cy)),
                        (0, 255, 0),
                        2,
                        1,
                    )

                    # cv2.rectangle(frame, (xh,yh), (xh+wh,yh+hh), (0,0,255),1,1)
                    # cxh,cyh= round( 10*(xh+wh/2))/10, round(10*(yh+hh/2))/10
                    # cv2.line(frame,(round(cxh),round(cyh)),(round(cxh),round(cyh)),
                    #          (0,0,255),2,1)

                # ================= track2
                if tracker2 is not None:
                    # print("tracking",tracker)
                    # frame = cv2.blur( frame, (4,4) )
                    ok2, bbox2 = tracker2.update(frame)
                    bbox2 = [round(i * 10) / 10 for i in bbox2]
                    # print("\ntracking2",ok2,bbox2)
                    (x2, y2, w2, h2) = [v for v in bbox2]
                    # if not( (x<0)or(y<0)or(x+w>=frame.shape[1])or(y+h>=frame.shape[0]) ):
                    # print("rect")
                    cv2.rectangle(
                        frame,
                        (int(x2), int(y2)),
                        (int(x2 + w2), int(y2 + h2)),
                        (0, 255, 255),
                        1,
                        1,
                    )
                    cx2, cy2 = (
                        round(10 * (x2 + w2 / 2)) / 10,
                        round(10 * (y2 + h2 / 2)) / 10,
                    )
                    cv2.line(
                        frame,
                        (int(cx2), int(cy2)),
                        (int(cx2), int(cy2)),
                        (0, 255, 255),
                        2,
                        1,
                    )
                    with open(tracker2_fname, "a") as f:
                        if webframen == "":
                            webframen = frame_num
                        f.write(f"{webframetime} {webframen} {cx2} {cy2}\n")

                # framelo = np.clip(frame, 60, None )
                # framelq = np.less_equal( frame, framelo)
                # frame = np.where( framelo<=60, 0  , framelo )
                # print(frame) # 255 levels

                # ------------------------redcross here: before zoom--------------------------------------
                # print(f" ... cross == {cross}")
                if not (cross is None):
                    if senh.add_frame(frame):
                        w, h, c = frame.shape
                        # print(w-centerY1, h-centerX1)
                        # print(f" ... cross {w} {h} /2")
                        senh.crosson(cross[0], cross[1], color="r")  # dx dy
                        # senh.setbox(f"CROS",  senh.jpg)
                        frame = senh.get_frame()
                    else:
                        print("X... senh did not accept frame (in redcross)")

                # =========================== ZOOM ME and OTHERS =======

                if (
                    zoomme > 1
                ):  # FUNNY - it continues to zoom where the mouse pointer is !!!!
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox(f"z {zoomme}", senh.scale)
                        w, h = frame.shape[0], frame.shape[1]
                        # print(w-centerY1, h-centerX1)
                        senh.zoom(zoomme, int(centerX1 - h / 2), int(centerY1 - w / 2))
                        frame = senh.get_frame()

                # ---------------------------------------------------- rotate ------------------
                # if rotate180:
                #     if senh.add_frame(frame):
                #         senh.setbox(f"ROT",  senh.rot)
                #         # w,h,c = frame.shape
                #         # print(w-centerY1, h-centerX1)
                #        senh.rotate180( 180 )
                #        frame = senh.get_frame(  )
                if rotate == 180:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)
                    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                elif rotate != 0:
                    frame = rotate_image( frame , rotate )

                # I just need to put local gamma before avisave...
                # else astroimage shows nothing..
                if local_gamma != 1:
                    frame = adjust_gamma(frame, local_gamma)

                if savepngcont:
                    sfilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sname = "snapshot"
                    sfilename = f"{sme}_{sfilename}_{sname}.png"
                    sfilename = os.path.expanduser("~/DATA/" + sfilename)
                    print(f"i... PNGcontinuous {sfilename}")

                    cv2.imwrite(sfilename, frame)
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("png", senh.jpg)
                        frame = senh.get_frame()

                if save:
                    if not save_decor:
                        saviout.write(frame)
                    if senh.add_frame(frame):
                        # print("avi..")
                        if save_decor:
                            senh.setbox("AVId", senh.avi)
                        else:
                            senh.setbox("AVI", senh.avi)
                        frame = senh.get_frame()

                if saved_jpg == 1:
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("JPG", senh.jpg)
                        frame = senh.get_frame()
                if saved_jpg == 2:
                    if senh.add_frame(frame):
                        # print("avi..")
                        senh.setbox("PNG", senh.jpg)
                        frame = senh.get_frame()

                if show_help:
                    # show_help = True
                    frame = disp_mutext(frame, HELPTEXT)

                if (allow_tracker_demand) and not (allow_tracker):
                    TRACKERHELP = """
u ... return back

t ... use tracker1
T ... use tracker2
  ...  ENTER or SPACE to accept region
  ...  c cancel
"""
                    frame = disp_mutext(frame, TRACKERHELP)

                # MEASUREMENT ==================================

                if measure > 0:
                    h, w = frame.shape[0], frame.shape[1]
                    # measure_fov = 110.5 # notebook

                    # approximative, not precise... 5%
                    radians_per_pixel = (measure_fov / 180 * math.pi) / w

                    # rad per pix * unit distance * better
                    # worked with zoom cameras????
                    radians_per_pixel2 = math.tan(measure_fov / 180 * math.pi / 2 / w)

                    # works with my 101deg camera---------------- and 55deg builtin ntbcam
                    #           ..... for 0.5 tan and alpha have 10% diff (tan vs. atan)
                    # measure_fov is TOTAL ANGLE
                    # radians_per_pixel2 =  math.atan(measure_fov /180*math.pi/(2*w) )*2
                    radians_per_pixel2 = math.atan(measure_fov / 180 * math.pi / w)
                    # print( radians_per_pixel2 ) # GOOD .... 0.00275

                    # radians_per_pixel2 =

                    radians_per_pixel2 /= zoomme  # process with zoom

                    # print(f"RPPX {radians_per_pixel}  {radians_per_pixel2} ")

                    # now arbitrarily define 1 meter..like.. 100px =>
                    # alpha = 100*radians_per_pixel
                    # b = 1m / math.tan( alpha )

                    def get_order(dist=1.7):  # determine order that fits
                        # list of marks on the ruler
                        wide = 0.001
                        notfulrng = 1.0 # notfulrng==0.8; I want full range now..
                        while True:
                            wide *= 10
                            pixwid = math.atan(wide / dist) / radians_per_pixel2
                            alpha = pixwid * radians_per_pixel2
                            if pixwid > w / 2 * notfulrng:  # not full rANGE
                                wide /= 10
                                pixwid = math.atan(wide / dist) / radians_per_pixel2
                                alpha = pixwid * radians_per_pixel2
                                break
                        order = wide

                        row = []

                        while True:
                            wide += order
                            pixwid = math.atan(wide / dist) / radians_per_pixel2
                            alpha = pixwid * radians_per_pixel2
                            if pixwid > w / 2 * notfulrng:  # not full rANGE:
                                wide -= order
                                pixwid = math.atan(wide / dist) / radians_per_pixel2
                                # neverused alpha = pixwid * radians_per_pixel2
                                break
                            else:
                                row.append(wide)
                        # -----
                        # -----
                        row.append(order)
                        row = sorted(row)
                        row = row[::-1]  # revert - we want Big to small
                        # print( "TICKS... max:", row[0]  )

                        base = 10**math.floor( math.log10( row[0]) )
                        if row[0]/base<4:
                            base = 10**math.floor( math.log10( row[0]/4) )

                        minors = np.arange( base, row[0], base)
                        minors = minors[::-1]
                        #print(minors)
                        if len(row) <= 2:
                            in0 = row[0] / 2
                            row.append(in0)
                            in1 =  row[0] / 4
                            row.append(in1)
                        #     in2 = row[0] / 4 *3
                        #     in3 = row[0] / 5
                        #     #in2 = row[-1]/10
                        #     row.append(in2)
                        #     # row.append( in2 )
                            # print("   > ",row)
                        return row,minors  # Big to small


                    def one_mark(dist=1.7, wide=[1, 2], speed=0, dispnumb = True):
                        #  wide ...  # Big to small
                        # h,w = frame.shape[0], frame.shape[1]
                        # pixel distance of halfwidth

                        # alpha = pixwid * radians_per_pixel2
                        # dist = wide/math.tan( alpha)
                        # I need to calculate 1m
                        level = 0
                        # print("XXXXX",wide)
                        for iwide in wide:

                            # multiply and round to one digit..before pixel calc
                            for ix in range(4):
                                if iwide*10**ix > 1:
                                    iwide = round( iwide* 10**ix)/10**ix
                                    break

                            pixwid = math.atan(iwide / dist) / radians_per_pixel2
                            # neverused alpha = pixwid * radians_per_pixel2

                            # print(f" {radians_per_pixel}radpp {pixwid}   {wide}m <- {dist} ")
                            step = 0
                            mX, mY = int(w / 2), int(h / 2)
                            if not (cross is None):
                                mX += cross[0]
                                mY += cross[1]
                            # here I addd the red cross position

                            mY = mY + level * step

                            yA, yB = mY, mY

                            xA = mX
                            xB = mX + int(pixwid)

                            yC = mY - int(pixwid) # up

                            color = (0, 255, 0)  # BGR
                            color = (55, 0, 255)  # BGR same as the red cross
                            colos = (255, 0, 55)  # BGR same as the red cross
                            if level == 0:
                                # line - horiznotal
                                cv2.line(
                                    frame,
                                    (int(xA), int(yA)),
                                    (int(xB), int(yB)),
                                    color,
                                    1,
                                )
                                cv2.line( # left
                                    frame,
                                    (int(xA), int(yA)),
                                    (int(2*xA-xB), int(yB)),
                                    color,
                                    1,
                                )


                                cv2.line( # probably central  mark
                                    frame,
                                    (int(xA), int(yA + 8)),
                                    (int(xA), int(yA - 8)),
                                    color,
                                    1,
                                )

                            # vert bars on horiz axis
                            cv2.line(  # ticks right
                                frame,
                                (int(xB), int(yB + 3)),
                                (int(xB), int(yB - 3)),
                                color,
                                1,
                            )
                            cv2.line( # ticks left
                                frame,
                                (int(2*xA-xB), int(yB + 3)),
                                (int(2*xA-xB), int(yB - 3)),
                                color,
                                1,
                            )

                            if yC>0:
                                # horz bars on vertic axis
                                cv2.line( # up
                                    frame,
                                    (int(xA), int(yA)),
                                    (int(xA), int(yC)),
                                    color,
                                    1,
                                )
                                cv2.line(
                                    frame,
                                    (int(xA-3), int(yC )),
                                    (int(xA+3), int(yC )),
                                    color,
                                    1,
                                )

                            unit = "m"
                            # --- check the biggest to set the unit [0] is biggest
                            if wide[0] <= 0.001:
                                iwide = round(iwide * 1000 * 1000) / 1000
                                unit = "mm"
                            elif wide[0] <= 0.01:
                                iwide = round(iwide * 100 * 1000) / 1000
                                unit = "cm"
                            elif wide[0] <= 0.1:
                                iwide = round(iwide * 100 * 100) / 100
                                unit = "cm"
                            elif wide[0] < 1:
                                iwide = round(iwide * 10 *100) / 100
                                unit = "dm"
                            else:
                                iwide = round(iwide * 10) / 10

                            # only properly round whatever unit
                            if iwide <= 0.001:
                                iwide = round(iwide * 10000) / 10000
                            elif iwide <= 0.01:
                                iwide = round(iwide * 1000) / 1000
                            elif iwide <= 0.1:
                                iwide = round(iwide * 100) / 100
                            elif iwide < 1:
                                iwide = round(iwide * 10) / 10
                            else:
                                iwide = round(iwide)


                            if level > 0:
                                unit = ""  # no unit during the scale
                            unit2 = "m"

                            if str(iwide)[:2] == "0.":
                                iwide = str(iwide)[1:]

                            if dispnumb:
                                # width on scale - scale values
                                cv2.putText(
                                    frame,
                                    f"{iwide}",
                                    (int(xB - 10), int(mY - 7)),  # little rightx a bit up y
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35,
                                    color,
                                    1,
                                )
                                cv2.putText(
                                    frame,
                                    f"{iwide}",
                                    (int(2*xA-xB - 10), int(mY - 7)),  # little rightx a bit up y
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35,
                                    color,
                                    1,
                                )

                                cv2.putText(  # up
                                    frame,
                                    f"{iwide}{unit}",
                                    (int(xA + 10), int(yC)),  # little rightx a bit up y
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35,
                                    color,
                                    1,
                                )



                                if level==0 and unit!="":
                                    cv2.putText(
                                        frame,
                                        f"  unit ... {unit}",
                                        (
                                            int(xA - 130),
                                            int(mY - 5 -40),
                                        ),  # little rightx a bit up y
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.35,
                                        color,
                                        1,
                                    )


                            if level >= 0:
                                # distance - only at first mark
                                cv2.putText(
                                    frame,
                                    f"  at {dist} {unit2}",
                                    (
                                        int(xA - 130),
                                        int(mY + 5 -40),
                                    ),  # little rightx a bit up y
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35,
                                    color,
                                    1,
                                )
                                cv2.putText(
                                    frame,
                                    f"  FOV {measure_fov:.1f}deg",
                                    (
                                        int(xA - 130),
                                        int(mY + 15 -40),
                                    ),  # little rightx a bit up y
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.35,
                                    color,
                                    1,
                                )
                                # I add velocity
                                if (level == 0) and not (tracker1 is None):
                                    cv2.putText(
                                        frame,
                                        f"speed {speed:6.2f}m/s",
                                        (
                                            int(xB - 50),
                                            int(mY + 15),
                                        ),  # little rightx a bit up y
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.35,
                                        color,
                                        1,
                                    )
                            level += 1

                    # main part of the ruler making---------------

                    order,minorticks = get_order(dist=measure)
                    # print(minorticks)

                    # speed computation
                    if not (tracker1 is None) and len(tracker_list) > 2:
                        b = tracker_list[-1]
                        try:
                            v_from = -2
                            a = tracker_list[v_from]
                            while True:
                                dt = (b[2] - a[2]).total_seconds()
                                if dt > 1.0:
                                    break
                                else:
                                    v_from -= 1
                                if len(tracker_list) < abs(v_from):
                                    break
                                a = tracker_list[v_from]
                        except:
                            dt = 100000  # velocity 0
                        c = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
                        v = c / dt * radians_per_pixel2
                        v = round(100 * math.tan(v) * measure) / 100
                        # print(f"i... speed = {v} m/s  {dt:.2}==dt " )
                    else:
                        v = 0
                    # plot ruler
                    one_mark(dist=measure, wide=minorticks, speed=v, dispnumb = False)
                    one_mark(dist=measure, wide=order, speed=v)

                    # ----------- THERE IS A MISTAKE countdown_s not known here
                #                 if "countdown" in locals() and len(countdown) > 0:
                #                     now = datetime.datetime.now()
                #                     delta = now - datetime.datetime(1970, 1, 1)
                #                     if delta < countdown_s:
                #                         TEXT = """scanning exposure
                # in progress"""
                #                         frame = disp_mutext(frame, TEXT)

                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW


                apply_distortion = False
                if apply_distortion:
                    # Assuming no distortion
                    #dist = np.zeros((5,1))
                    dist = np.array([[ -8e-7, 4e-11, 0.0, 0.0, 0.0]])

                    #mtx = np.eye(3)
                    scale = 1.0
                    mtx = np.array([[scale, 0, h/2], [0, scale, w/2], [0, 0, 1]])

                    h, w = frame.shape[:2]

                    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
                    # undistort
                    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
                    ## crop the image
                    #x, y, w, h = roi
                    frame = dst#[y:y+h, x:x+w]



                cv2.imshow(rpi_name, frame)  # 1 window for each RPi
                # ======================================================== IMSHOW
                if save_decor:
                    saviout.write(frame)
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # ======================================================== IMSHOW
                # this may be useful?
                if False:
                    if not (cropped is None):
                        cropped = cv2.resize(cropped, (640, 480))
                        cv2.imshow("tracking1", cropped)  # ZOOM ON TRACK
                        # cv2.resizeWindow(

                if expande > 1:
                    cv2.resizeWindow(
                        rpi_name,
                        int(expande * frame.shape[1]),
                        int(expande * frame.shape[0]),
                    )
                    # print(frame.shape)
                # cv2.setWindowProperty(rpi_name, cv2.WND_PROP_TOPMOST, 1)
                # cv2.namedWindow(rpi_name, cv2.WINDOW_GUI_EXPANDED)
                # time.sleep(0.2)
                cv2.setMouseCallback(rpi_name, MOUSE)
                #
                #  waitkeyex sometimes sees shift and ctrl... but not on zen...
                #########################################################################
                #########################################################################
                #########################################################################
                #key = cv2.waitKey(1)  # same problem with shift on ubu22 as ex
                #########################################################################
                #########################################################################
                #########################################################################
                #
                key = cv2.waitKeyEx(1) # this may work in ubuntu 22 - let us check....

                c = s = "     "
                # non-ubuntu22 version makes sense with Listener
                #if CTRL:  c = "ALT  "
                #if SHIFT: s = "SHIFT"
                # print(f" {c} x {s} ...      ", end = "       \n")

                #
                # UBUNTU 22 - ctrl and alt give 227 and 233 resp
                #
                if key != -1:
                    print(f" *key== {key}   /{chr(0xFF&key)}/  .. {c} : {s}  >>>.      ")
                    key = remap_keys(key) # make compatible with waitKey()
                    print(f" ... --------------------------------------------- remapped {key}")
                    # if SHIFT: key = ord(chr(key).upper())

                # i will not use the translation,,
                # key = remap_keys(key) # make compatible with waitKey()
                # print(f"remapped {key}")

                # print(f"{centerX1} {centerY1}")
                if (cross is None) and not greencross:
                    if (frame is not None) and (rpi_name != "") and (key == ord("?") and not CTRL):
                        print("h PRESSED! - ")
                        show_help = not (show_help)
                        print(HELPTEXT)

                # -----------------------------------------------------rotate zoom

                if (frame is not None) and \
                   (rpi_name != "") and \
                   (key == ord("r") and not (CTRL)):
                    print("r PRESSED! - rotate change")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate+=1

                if (frame is not None) and \
                   (rpi_name != "") and \
                    (key == ord("R") and not (CTRL)):
                    print("r PRESSED! - rotate change")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate-=1

                if (frame is not None) and \
                   (rpi_name != "") and \
                    (key == ord("r") and  (CTRL)):
                    print("r PRESSED! - reset rotate")
                    if rotate is None:
                        rotate = 0
                    if rotate == 180:
                        rotate = 0
                    else:
                        rotate = 180


                if (frame is not None) and (rpi_name != "") and (key == ord("z")):
                    print(f"z PRESSED! - ZOOM {zoomme}x")
                    zoomme *= 2
                    if zoomme > 16:
                        zoomme = 1
                    sfilenamea = ""

                if (frame is not None) and (rpi_name != "") and (key == ord("Z")):
                    print("Z PRESSED! - ZOOM ended")
                    zoomme = 1
                    sfilenamea = ""

                # ------------------------------------------ web  pause quit expa---------------

                if (frame is not None) and (rpi_name != "") and (key == ord("w")):
                    print("w PRESSED! - openning web browser")
                    webbrowser.open(videodev.replace("/video", ""))  # BRUTAL

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and ((key == 1048608) or (key == ord(" ")))
                ):
                    print("SPC PRESSED! - pause/play")
                    pause = not pause
                    print(f" ... pause = {pause}")

                if (frame is not None) and (rpi_name != "") and (key == ord("q")):
                    print("q PRESSED!")
                    print("i... it was version:", __version__)
                    sys.exit(1)

                if (frame is not None) and (rpi_name != "") and (key == ord("x")):
                    print("x PRESSED! - expand 2")

                    if expande == 2:
                        expande = 1
                    else:
                        expande = 2

                # -----------------------------------------------------save s a

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("a") and not CTRL)
                ):
                    if save:
                        print("a PRESSED! - STOPPING AVI ... decor==",save_decor)
                        sfilenamea = ""
                        savepngcont = False
                        save = False
                    else:
                        print("a PRESSED! - saving AVI WITHOUT DECOR (mkv)")
                        save = True
                        save_decor = False

                        height, width, channel = frame.shape

                        sfilenamea, saviout = setupsave((width, height))
                        print(">>>", sfilenamea)



                if (frame is not None) and \
                   (rpi_name != "") and \
                   (key == ord("A") and not CTRL):  # not with ctl
                    if save:
                        print("A PRESSED! - STOPPING AVI (mkv)  decor ==", save_decor)
                        sfilenamea = ""
                        savepngcont = False
                        save = False
                    else:
                        print("A PRESSED! - WITH DECOR saving AVI (mkv)")
                        save = True
                        save_decor = True
                        height, width, channel = frame.shape

                        sfilenamea, saviout = setupsave((width, height))
                        print(">>>", sfilenamea)



                if ( (frame is not None) and \
                     (rpi_name != "") and \
                     (key == ord("a"))  and (CTRL) ):  # (key == 1310817):
                    if savepngcont:
                        savepngcont = False
                    else:
                        print("ctl-a PRESSED! - LOCALY saving PNG continuosly !!!")  # ctrla
                        savepngcont = True



                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and ((key == ord("p"))  and  CTRL)
                ):
                    print("Ctrl - s pressed  ... calling remote save of Full Quality PNG")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savepn": "SAVEPN"}
                    post_response = requests.post(url=post_addr, data=post_data)


                saved_jpg = 0
                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and ((key == ord("s")) or (key == ord("S")) and not CTRL)
                ):
                    print("s or S PRESSED!  - ")
                    print("      ... not the internal save_image...")
                    sname = "snapshot"
                    sfilename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    # defined above # sme = socket.gethostname()
                    if key == ord("s"):
                        sfilename = f"{sme}_{sfilename}_{sname}.jpg"
                        saved_jpg = 1 #JPG
                    if key == ord("S"):
                        sfilename = f"{sme}_{sfilename}_{sname}.png"
                        saved_jpg = 2 # PNG

                    dir2create = os.path.expanduser("~/DATA/")
                    if not os.path.isdir(os.path.expanduser(dir2create)):
                        print(
                            f"D... trying to create directory {dir2create} for saving"
                        )
                        # result = False
                        os.mkdir(os.path.expanduser(dir2create))

                    sfilename = os.path.expanduser("~/DATA/" + sfilename)
                    # sfourcc = cv2.VideoWriter_fourcc(*'XVID')
                    # saviout = cv2.VideoWriter( sfilename , sfourcc , 25.0, (640,480))
                    isWritten = cv2.imwrite(sfilename, frame)
                    if isWritten:
                        print("Image is successfully saved as file.", sfilename)


                # ------------------------- measure and cross -------------------------------

                if (frame is not None) and (rpi_name != ""):
                    if key == ord("C"):
                        print(
                            f"c PRESSED! - cross = {cross} OFF; saving {FILE_REDCROSS}"
                        )
                        if (cross is None) or (len(cross) != 2):
                            break
                        with open(os.path.expanduser(FILE_REDCROSS), "w") as f:
                            f.write(f"{cross[0]}\n{cross[1]}\n")
                            cross = None
                    if key == ord("c"):
                        if cross is None:
                            cross = [0, 0]
                            if os.path.exists(os.path.expanduser(FILE_REDCROSS)):
                                try:
                                    with open(os.path.expanduser(FILE_REDCROSS)) as f:
                                        cr = f.readlines()
                                        cross = [int(cr[0]), int(cr[1])]
                                except:
                                    print(f"X... problem to open {FILE_REDCROSS}")
                            print(f"c PRESSED! - cross = {cross} ON")

                # --------- redcross manip
                if not (cross is None):
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("h") and not CTRL)
                    ):  # <
                        cross[0] -= 4
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("j") and not CTRL)
                    ):  # v
                        cross[1] += 4
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("k") and not CTRL)
                    ):  # ^
                        cross[1] -= 4
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("l") and not CTRL)
                    ):  # >
                        cross[0] += 4

                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("H") and not CTRL)
                    ):  # <
                        cross[0] -= 17
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("J") and not CTRL)
                    ):  # v
                        cross[1] += 17
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("K") and not CTRL)
                    ):  # ^
                        cross[1] -= 17
                    if (
                        (frame is not None) and (rpi_name != "") and (key == ord("L") and not CTRL)
                    ):  # >
                        cross[0] += 17

                if (
                    (measure > 0)
                    and (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("N"))
                ):
                    print("N PRESSED! - measure distance - far")
                    measure_prev_tmp = measure
                    measure = round(10 * measure / 1.2) / 10
                    if measure_prev_tmp == measure:
                        measure = measure/2
                    if measure < 0.1:
                        measure = 0.1

                if (
                    (measure > 0)
                    and (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("n"))
                ):
                    print("m PRESSED! - measure distance - closer")
                    measure_prev_tmp = measure
                    if measure == 0:
                        measure = 1
                    if measure < 0:
                        measure = -measure
                    measure = round(10 * measure * 1.15) / 10
                    if measure_prev_tmp == measure:
                        measure = measure*2
                    if measure > 20000:
                        measure = 20000

                if (frame is not None) and (rpi_name != "") and (key == ord("m")):
                    print("m PRESSED! - measure distance - ON")
                    print("i... cheap Sonix :  44 deg")
                    print("i... Sony imx    : 101 deg")
                    print("i... zenbook     :  56 deg")
                    if measure < 0:
                        measure = -measure
                    if measure == 0:
                        measure = 1

                if (frame is not None) and (rpi_name != "") and (key == ord("M")):
                    print("M PRESSED! - DEmeasure")
                    measure = -abs(measure)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure > 0)
                    and (key == ord("f"))
                ):
                    print("f PRESSED! - FOV increase", measure_fov)
                    prev_fov_tmp = measure_fov
                    measure_fov = measure_fov * 1.15
                    if measure_fov > 4:
                        measure_fov = round(measure_fov)
                        if measure_fov == prev_fov_tmp:
                            measure_fov = 2* measure_fov
                    else:
                        measure_fov = round(measure_fov * 10) / 10
                        if measure_fov == prev_fov_tmp:
                            measure_fov = 2* measure_fov
                    if measure_fov > 160:
                        measure_fov = 160


                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure > 0)
                    and (key == ord("F"))
                ):
                    print("F PRESSED! - FOV decrease")
                    measure_fov = measure_fov / 1.25
                    if measure_fov > 3:
                        measure_fov = round(measure_fov)
                    else:
                        measure_fov = round(measure_fov * 10) / 10

                    if measure_fov < 0.3:
                        measure_fov = 0.3

                # ---------------- trackers--------------- t T u---------------

                # ------if ALLOWED - first - to have no display help
                # elif to skip one loop
                if (
                    (allow_tracker)
                    and (frame is not None)
                    and (rpi_name != "")
                    # and allow_tracker1
                ):
                    # and (key == ord('t')):
                    # print("t PRESSED! - track" ,tracker1,"\n")
                    print("i ... setting allowed tracker1 \n")
                    allow_tracker = False
                    tracker1 = cv2.TrackerCSRT_create()  # KCF GOTURN MIL
                    bbox = cv2.selectROI(frame)
                    if (len(bbox) < 4) or (bbox[-1] < 10):
                        tracker1 = None
                        print("i... fail init track")
                    else:
                        # bbox = tuple([ i+0.5 for i in bbox ])
                        ok = tracker1.init(frame, bbox)
                        tracker_list = []
                        tracker1_fname = datetime.datetime.now().strftime(
                            "tracker1_%Y%m%d_%H%M%S.dat"
                        )
                        # #------------this is for histotracker
                        # x,y,w,h = bbox
                        # track_window = bbox
                        # # roi = frame[x:x+w, y:y+h]
                        # roi = frame[ y:y+h, x:x+w]
                        # hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                        # mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
                        # roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
                        # cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
                        # term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 0.1 ) #iters, eps

                        # orb = cv2.ORB_create() # I dont use now

                if (
                    (allow_tracker)
                    and (frame is not None)
                    and (rpi_name != "")
                    #                    and allow_tracker2
                ):
                    # and (key == ord('T')):
                    print("t PRESSED! - track", tracker2)
                    print("i ... setting allowed tracker2 \n")
                    allow_tracker = False
                    tracker2 = cv2.TrackerKCF_create()  # KCF GOTURN MIL
                    bbox2 = cv2.selectROI(frame)
                    if (len(bbox2) < 4) or (bbox2[-1] < 10):
                        tracker2 = None
                        print("i... fail init track2")
                    else:
                        # bbox2 = tuple([ i+0.5 for i in bbox2 ])
                        ok2 = tracker2.init(frame, bbox2)
                        tracker2_fname = datetime.datetime.now().strftime(
                            "tracker2_%Y%m%d_%H%M%S.dat"
                        )

                # -----  allow display help, after allow tracker true
                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and ((key == ord("t")) or (key == ord("T")))
                    and not (CTRL)
                    and not (allow_tracker_demand)
                    and not (allow_tracker)
                ):
                    print("i... allow tracker demand\n")
                    allow_tracker_demand = True
                    allow_tracker2 = False
                    allow_tracker1 = False
                    # switch on the menu display

                # --- 2nd 't' press :  is before demand=True, sets allow true
                elif (
                    (frame is not None)
                    and (rpi_name != "")
                    and ((key == ord("t")) or (key == ord("T")) and not (CTRL))
                    and (allow_tracker_demand)
                    and not (allow_tracker)
                ):
                    print("i... allowing tracker, removing tracker_demand\n")
                    allow_tracker = True  # but I need one loop to remove menu
                    # switch off the menudisplay
                    allow_tracker_demand = False
                    allow_tracker2 = False
                    allow_tracker1 = False
                    if key == ord("T"):
                        allow_tracker2 = True
                    if key == ord("t"):
                        allow_tracker1 = True

                if (frame is not None) and (rpi_name != "") and (key == ord("u")):
                    print("u PRESSED! - UNtrack")
                    tracker1 = None
                    tracker2 = None
                    tracker_date = None
                    allow_tracker_demand = False
                    allow_tracker = False

                if (frame is not None) and (rpi_name != "") and (key == ord("v")):
                    print("v PRESSED! - green crosson")
                    greencross = True
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"crosson": "CROSSON"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("V")):
                    print("V PRESSED! - green crossoff")
                    greencross = False
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"crossoff": "CROSSOFF"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("b")):
                    print("b PRESSED! - substrac background")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"subbg": "SUBBG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("B")):
                    print("B PRESSED! - save background")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savebg": "SAVEBG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("f"))
                ):
                    print("f PRESSED! - mix foreground")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"mixfg": "MIXFG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("F"))
                ):
                    print("F PRESSED! - save foreground")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"savefg": "SAVEFG"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("o")):
                    print("o PRESSED! - ")
                    # post_addr = videodev.replace("/video","/cross" )
                    # post_data = {'exposet':'EXPOSET','expovalue':0.3145}
                    # post_response = requests.post(url=post_addr, data=post_data)
                    countdown = [
                        0.0,
                        0.001,
                        0.002,
                        0.004,
                        0.008,
                        0.01,
                        0.02,
                        0.04,
                        0.08,
                        0.1,
                        0.2,
                        0.4,
                        0.8,
                        1.0,
                        -2,
                        0.0,
                        0.001,
                        0.002,
                        0.004,
                        0.008,
                        0.01,
                        0.02,
                        0.04,
                        0.08,
                        0.1,
                        0.2,
                        0.4,
                        0.8,
                        1.0,
                        -97,
                        -98,
                        -99,
                    ]
                    countdown_gain = False
                    # -2, -97 calc. , -98 -99 perform
                    now = datetime.datetime.now()
                    delta = now - datetime.datetime(1970, 1, 1)
                    countdown_s = delta + datetime.timedelta(seconds=countdownpause)
                    countdown_ana_on = False
                    countdown_ana_results = []
                    # sqitch off gain
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain": "GAIN"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if "countdown" in locals() and len(countdown) > 0:
                    now = datetime.datetime.now()
                    delta = now - datetime.datetime(1970, 1, 1)
                    if delta > countdown_s:
                        if "countdown_ana_on" in locals():
                            if countdown_ana_on:
                                # print("   ------ analysing ----------------")
                                countdown_ana_on = False
                                senh.add_frame(
                                    frame[21: frame.shape[0] - 21, 0: frame.shape[1]]
                                )
                                hmean = senh.histo_mean()
                                print(
                                    f"i... histogram mean:{hmean:3d} / pre{countdown[0]:.3f} {len(countdown)*countdownpause:3.0f} sec. remains"
                                )
                                countdown_ana_results.append(hmean)

                                # print( countdown_ana_results )

                                # ------ analyze first batch -   (-2)
                                if (countdown[0] < -1) and (
                                    countdown[0] > -3
                                ):  # without gain
                                    resx = np.array(countdown_ana_results[::2])
                                    resy = np.array(countdown_ana_results[1::2])
                                    # allx = resx
                                    # ally = resy
                                    allx = np.logspace(-4, 1, 400)
                                    ally = np.interp(allx, resx, resy, 100)

                                    # if not good
                                    # if  (np.abs(ally - optim_histo).min()>1): # works for dark
                                    # if good
                                    if (np.abs(ally - optim_histo).min() <= 1) or (
                                        ally - optim_histo
                                    ).min() > 1:  # always brighter:: #
                                        if (
                                            ally - optim_histo
                                        ).min() > 1:  # always brighter:: #
                                            print(
                                                "i... always brighter, I stop here without gain 1"
                                            )
                                        countdown = [-98, -99]
                                        allx_idx = np.abs(ally - optim_histo).argmin()
                                        optimexpo = allx[allx_idx]
                                        optimgain = -1
                                        print(resx)
                                        print(resy)
                                        print(
                                            f"i... best x  {optimexpo} at element {allx_idx}, no gain games"
                                        )
                                    else:
                                        if ally.max() - ally.min() < 3:
                                            print(
                                                "i... there is no effect of EXPO: cheap Sonix cam?"
                                            )
                                            countdown_gain = True
                                        countdown_ana_results = []

                                if countdown[0] == -97:  # final with gain 1
                                    resx = np.array(countdown_ana_results[::2])
                                    resy = np.array(countdown_ana_results[1::2])
                                    allx = resx
                                    ally = resy
                                    allx = np.logspace(-4, 1, 400)
                                    ally = np.interp(allx, resx, resy, 100)

                                    # if  (np.abs(ally - optim_histo).min()>1) and (countdown[0]>-3):
                                    #    break
                                    # elif countdown[0]>-3:
                                    #    countdown=[-98,-99]

                                    # optimexpo = resx[ np.abs(resy - optim_histo).argmin() ]
                                    allx_idx = np.abs(ally - optim_histo).argmin()
                                    optimexpo = allx[allx_idx]
                                    if optimexpo > 1:
                                        optimexpo = 1
                                    optimgain = 1
                                    if countdown_gain:  # when cheap sonix camera:
                                        optimexpo = 20
                                        optimgain = allx[allx_idx]
                                        if optimgain > 1:
                                            optimgain = 1
                                        print(f"i... OPTIMAL GAIN = {optimgain}")
                                    else:
                                        print(f"i... OPTIMAL EXPO = {optimexpo}")
                                        print("i... BUT USE GAIN 1 !")

                                    print("RESULTS:")
                                    print(resx)
                                    print(resy)
                                    print(
                                        f"i... best x  {optimexpo} at element {allx_idx} "
                                    )
                                    # with open(f"expo_calib_{now.strftime('%H%M%S')}.txt",'w') as f:
                                    #    f.write(" ".join( [str(e) for e in countdown_ana_results]))
                        #                                        f.write("\n")

                        # print("   --------- counting down ------: ", len(countdown) )
                        countdown_s = delta + datetime.timedelta(seconds=countdownpause)
                        exnow = float(
                            countdown.pop(0)
                        )  # 0 left way; -1 default  is from right
                        post_addr = videodev.replace("/video", "/cross")
                        if exnow < -98:  # -99 back to default with gain
                            post_data = {"gain": "GAIN"}
                            if optimgain > 0:  # can be only 1 or -1
                                post_data = {
                                    "gainset": "GAINSET",
                                    "gainvalue": optimgain,
                                }
                        elif exnow < -97:  # -99 back to default with expo
                            post_data = {"expo": "EXPO"}
                            if optimexpo >= 0:
                                post_data = {
                                    "exposet": "EXPOSET",
                                    "expovalue": optimexpo,
                                }
                        elif exnow < -1:
                            # exnow = float( countdown.pop(0) )
                            post_data = {"gainset": "GAINSET", "gainvalue": 1.0}
                        else:  # testing data
                            if (
                                countdown_gain
                            ):  # i will play on gain with cheap sonix camera
                                post_data = {"gainset": "GAINSET", "gainvalue": exnow}
                            else:
                                post_data = {"exposet": "EXPOSET", "expovalue": exnow}
                            countdown_ana_on = True
                            countdown_ana_results.append(exnow)
                        post_response = requests.post(url=post_addr, data=post_data)

                # if 'countdown_ana_on' in locals():
                #     if countdown_ana_on:
                #         print("   ------ analysing ----------------")
                #         countdown_ana_on = False
                #         senh.add_frame( frame )
                #         hmean = senh.histo_mean( )
                #         print(hmean)
                #         countdown_ana_results.append(hmean)
                #         print( countdown_ana_results )
                #         if len(countdown)==0:
                #             print( "RESULTS:", countdown_ana_results )

                if (frame is not None) and (rpi_name != "") and (key == ord("O")):
                    print("O PRESSED! - break expo optim")
                    # post_addr = videodev.replace("/video","/cross" )
                    # post_data = {'gainset':'GAINSET','gainvalue':1.}
                    # post_response = requests.post(url=post_addr, data=post_data)
                    if "countdown" in locals():
                        countdown = []

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("e") and not CTRL)
                ):
                    print("e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo2": "EXPO2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("E")):
                    print("e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo05": "EXPO05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # ------------------default expo----------------------
                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("e"))
                    and (CTRL)
                ):  # (key == 1310821 ): # ctrle
                    print("ctl-e PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"expo": "EXPO"}
                    post_response = requests.post(url=post_addr, data=post_data)


                # --------------------------gain ----------------------

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("g") and not CTRL)
                ):
                    print("g PRESSED! -  gain up")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain2": "GAIN2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("G")):
                    print("G PRESSED! - gain down")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain05": "GAIN05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("g"))
                    and (CTRL)
                ):  # and  (key == 1310823): # ctrlg
                    print("ctl-g PRESSED! -  gain reset")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gain": "GAIN"}
                    post_response = requests.post(url=post_addr, data=post_data)


                # --------------------------gamma ----------------------

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("y") and not CTRL)
                ):
                    print("y PRESSED! -  gamm up")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma2": "GAMMA2"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("Y")):
                    print("Y PRESSED! - gain down")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma05": "GAMMA05"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("y"))
                    and (CTRL)
                ):  # and  (key == 1310823): # ctrlg
                    print("ctl-y PRESSED! -  gamma reset")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"gamma": "GAMMA"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # ------------------------------local gamma --------------------------
                if ( (frame is not None)   and (rpi_name != "")
                    and (key == ord("d") and not CTRL)               ):
                    print("d PRESSED! - local gamma+")
                    local_gamma = local_gamma * 1.4

                if (   (frame is not None)  and (rpi_name != "")
                    and (key == ord("D") and not CTRL)   ):
                    print("D PRESSED! - local gamma -")
                    local_gamma = local_gamma / 1.4

                if ( (frame is not None) and (rpi_name != "")
                    and (key == ord("D") and not CTRL)        ):
                    print("ctrl - Y PRESSED! -  no action")

                if (     (frame is not None)  and (rpi_name != "")   and (key == ord("d"))
                    and (CTRL)      ):  # and  (key == 1310841): #ctrly
                    print("ctl-d PRESSED! - reset local gamma")
                    local_gamma = 1



                # -------------------------------------------------------- p fixed live ----------pause

                if (frame is not None) and (rpi_name != "") and (key == ord("p")):
                    print("p PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"fixed": "FIXED"}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (frame is not None) and (rpi_name != "") and (key == ord("P")):
                    print("p PRESSED! - ")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"live": "LIVE"}
                    post_response = requests.post(url=post_addr, data=post_data)

                # --------- greencross manip
                if (cross is None) and greencross:
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {}

                    if (frame is not None) and (rpi_name != "") and (key == ord("h") and not CTRL):  # <
                        post_data = {"left": "LEFT"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("j") and not CTRL):  # v
                        post_data = {"down": "DOWN"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("k") and not CTRL):  # ^
                        post_data = {"up": "UP"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("l") and not CTRL):  # >
                        post_data = {"right": "RIGHT"}

                    if (frame is not None) and (rpi_name != "") and (key == ord("H") and not CTRL):  # <
                        post_data = {"left2": "LEFT2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("J") and not CTRL):  # v
                        post_data = {"down2": "DOWN2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("K") and not CTRL):  # ^
                        post_data = {"up2": "UP2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("L") and not CTRL):  # >
                        post_data = {"right2": "RIGHT2"}

                    if post_data != {}:
                        post_response = requests.post(url=post_addr, data=post_data)

                # --------- pantilthat manip
                if (cross is None) and not greencross:
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {}

                    if (frame is not None) and (rpi_name != "") and (key == ord("h") and not CTRL):  # <
                        post_data = {"left": "LEFT"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("j") and not CTRL):  # v
                        post_data = {"down": "DOWN"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("k") and not CTRL):  # ^
                        post_data = {"up": "UP"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("l") and not CTRL):  # >
                        post_data = {"right": "RIGHT"}

                    if (frame is not None) and (rpi_name != "") and (key == ord("H") and not CTRL):  # <
                        post_data = {"left2": "LEFT2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("J") and not CTRL):  # v
                        post_data = {"down2": "DOWN2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("K") and not CTRL):  # ^
                        post_data = {"up2": "UP2"}
                    if (frame is not None) and (rpi_name != "") and (key == ord("L") and not CTRL):  # >
                        post_data = {"right2": "RIGHT2"}

                    if post_data != {}:
                        post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("i"))
                ):
                    integrate *= 2
                    print(f"i PRESSED! - accum  {integrate} snapshots")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"accum": "ACCUM", "accumtxt": int(integrate)}
                    post_response = requests.post(url=post_addr, data=post_data)

                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (measure <= 0)
                    and (key == ord("I"))
                ):
                    print("i PRESSED! - accum integrate 1")
                    integrate = 1
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"accum": "ACCUM", "accumtxt": 0}
                    post_response = requests.post(url=post_addr, data=post_data)


                # ctrl -- MODES histo direct detect
                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("h") and CTRL)
                ):
                    print("ctl-h PRESSED! - HISTOGRAM BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "HISTOGRAM" }
                    post_response = requests.post(url=post_addr, data=post_data)


                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("j") and CTRL)
                ):
                    print("ctl-j PRESSED! - directmode BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "DIRECT" }
                    post_response = requests.post(url=post_addr, data=post_data)


                if ( (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("k") and CTRL)
                ):
                    print("ctl-k PRESSED! - detectmode BUTTON ---------------------")
                    post_addr = videodev.replace("/video", "/cross")
                    post_data = {"framekind": "DETECT" }
                    post_response = requests.post(url=post_addr, data=post_data)



                if (
                    (frame is not None)
                    and (rpi_name != "")
                    and (key == ord("t") and CTRL)
                ):
                    print("ctl-t PRESSED! - TEST BUTTON ---------------------")
                    print(" ... clears countdown .... ")
                    #print(" try to keep ctl pressed and then press t")
                    post_addr = videodev.replace("/video", "/cross")
                    if len(jpgkompr1)==0:
                        jpgkompr1 = [x for x in jpgkompr2]
                    aaa = jpgkompr1.pop(0)
                    print(" ... available comp",jpgkompr1)
                    print(" ... sets  kompression:", aaa)
                    post_data = {"kompress": "KOMPRESS", "kompressvalue": aaa}
                    post_response = requests.post(url=post_addr, data=post_data)
                    if "countdown" in locals():
                        countdown = []

                # TEST key code
                # if key!=-1:
                #    print(f"\n{key}\n")

        print("i... it was version", __version__)


if __name__ == "__main__":
    Fire(display2)
    # Fire({ "disp":display2,   "disp2":display2    })
