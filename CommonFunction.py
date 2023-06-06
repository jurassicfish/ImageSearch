#!user/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import numpy as np

# 获取当前目录（项目）
import cv2


def GetAppDir():
    myPath = None
    if sys.path[0]:
        myPath = sys.path[0]
    else:
        myPath = sys.path[1]
    if os.path.isdir(myPath):
        pass
    elif os.path.isfile(myPath):
        myPath = os.path.dirname(myPath)

    return myPath


# 调用 opencv 显示图片
def Cv2Show(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# QImage 转为 opencv image对象
def QImageToCvImage(qImage):
    buffer = qImage.bits().asstring(qImage.byteCount())
    width = qImage.width()
    height = qImage.height()
    image = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image
