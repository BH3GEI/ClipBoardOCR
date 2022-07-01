# -*- encoding=utf8 -*-
from PIL import Image, ImageGrab
from aip import AipOcr
import pyperclip
import time
import hashlib
from airtest.core.api import *
from airtest.core.android.adb import *
import subprocess
from pykeyboard import *
from pymouse import *
import sys
import os
import tkinter
import win32gui, win32api

#OCR的相关参数
APP_ID = 'xxx'
API_KEY = 'xxx'
SECRET_KEY = 'xxx'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
fname = 'basicAccurate'
md5_old = ''

def readClipboardOCRAndPaste():
    # 检测到剪切板有新增图片后复制图像内文本到剪切板
    global md5_old, md5_flag
    md5_flag = 0
    #读取剪切板图片，返回图片对象
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        #print(im.size)
        im.save("clipboard.png")
        print("")
        print("[✅成功读取了剪切板最后一张图片，正在识别]")
    elif im:
        for filename in im:
            print("filename:%s" % filename)
            im = Image.open(filename)
    else:
        pass
    with open('clipboard.png', 'rb') as fp:
        temp_img = fp.read()
        md5_new = hashlib.md5(temp_img).hexdigest()
        if md5_new != md5_old:
            results = client.basicAccurate(temp_img)["words_result"]
            textResult = ''
            for result in results:
                text = result["words"]
                textResult = textResult + text
            print("[识别内容：]")
            print("🖤"+textResult+"🖤")
            pyperclip.copy(textResult)
            print("[✅内容已经复制到剪切板了呢ヾ(≧▽≦*)o]")
            md5_old = md5_new
            #textPaste()
        time.sleep(1)
        # md5_current = hashlib.md5(temp_img).hexdigest()

def threadCopy():
    while True:
        readClipboardOCRAndPaste()

threadCopy()
