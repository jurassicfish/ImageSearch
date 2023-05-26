#!user/bin/python
# -*- coding:utf-8 -*-
import os
import sys


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
