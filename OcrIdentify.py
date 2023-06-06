#!user/bin/python
# -*- coding:utf-8 -*-
"""
功能包括
1、识别图片中包含的文字 界面
"""
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QShortcut, QApplication
import pytesseract
import cv2
import numpy as np

import CommonFunction
import TextPic
from CommonFunction import GetAppDir


class OcrIdentifyDlg(QDialog):
    def __init__(self):
        super(OcrIdentifyDlg, self).__init__()

        self.shortCut = None
        self.bt_area = None
        self.bt_identify = None
        self.te_text = None
        self.l_showImg = None
        self.bt_select = None
        self.le_img = None
        self.l_img = None

        self.cv2img = None

        self.InitUIPart()
        self.UILayout()
        self.ConnectSignalSlot()
        self.LoadQss()
        self.InitUIData()
        self.InitDialog()
        self.LoadSettings()

    def InitUIPart(self):
        self.l_img = QLabel(self)
        self.l_img.setObjectName("OIImageShow")
        # self.l_img.setScaledContents(True)
        # 组件接受拖拽
        self.l_img.setAcceptDrops(True)

        self.bt_select = QPushButton("选择\n图片")
        self.bt_select.setObjectName("OIImgSelect")
        self.bt_area = QPushButton("区域\n调整")
        self.bt_area.setObjectName("OIArea")
        self.bt_identify = QPushButton("识别\n内容")
        self.bt_identify.setObjectName("OIIdentify")

        self.te_text = QTextEdit()
        self.te_text.setReadOnly(True)

        # 粘贴对象
        self.shortCut = QShortcut(Qt.CTRL + Qt.Key_V,self)

    def UILayout(self):
        vBoxButton = QVBoxLayout()
        vBoxButton.addWidget(self.bt_select)
        vBoxButton.addWidget(self.bt_area)
        vBoxButton.addWidget(self.bt_identify)

        hBoxSelect = QHBoxLayout()
        hBoxSelect.addWidget(self.l_img)
        hBoxSelect.addSpacing(10)
        hBoxSelect.addLayout(vBoxButton)

        vBox = QVBoxLayout()
        vBox.addLayout(hBoxSelect)
        vBox.addWidget(self.te_text)

        self.setLayout(vBox)

    def ConnectSignalSlot(self):
        self.bt_select.clicked.connect(self.SelectImage)
        self.bt_identify.clicked.connect(self.IdentifyContent)

        # 粘贴
        self.shortCut.activated.connect(self.PasteImage)

    def InitUIData(self):
        # 标题栏图标
        img = QImage.fromData(TextPic.PicData.AppPic())
        # img = QImage.fromData(self.picData.appPic())
        pixMap = QPixmap.fromImage(img)
        # print(self.l_img.size())
        pixMap = pixMap.scaled(QSize(300,300))
        icon = QIcon(pixMap)
        self.l_img.setPixmap(pixMap)

    def InitDialog(self):
        pass
        # 窗口接受拖拽
        self.setAcceptDrops(True)

    def LoadQss(self):
        fileName = GetAppDir() + '\\res\\ImageSearch.qss'
        with open(fileName, 'r') as fileObj:
            qssStr = fileObj.read()
            self.setStyleSheet(qssStr)

    def LoadSettings(self):
        pass

    # 选择图片
    def SelectImage(self):
        file = QFileDialog.getOpenFileName(self, "选择图片", CommonFunction.GetAppDir(),
                                           "图片类型(*.webp;*.jpg;*.png);;所有类型(*)")

        print(file)
        fileName = file[0]

        if fileName == '':
            return

        self.cv2img = cv2.imread(fileName)
        imgShow = self.cv2img.copy()
        imgShow = cv2.cvtColor(imgShow, cv2.COLOR_BGR2RGB)

        # 显示
        imgShow = self.ResizeShowImg(imgShow)
        qimg = QImage(imgShow.data, imgShow.shape[1], imgShow.shape[0], imgShow.shape[1] * 3, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        self.l_img.setPixmap(pixmap)

    # 识别图片中文字
    def IdentifyContent(self) -> None:
        # 复制
        img = self.cv2img.copy()
        # 灰度
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # CommonFunction.Cv2Show(img)
        # 二值处理
        img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]

        # CommonFunction.Cv2Show(img)

        result = pytesseract.image_to_string(img, lang='chi_sim')
        print(result)

        self.te_text.setText(result)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        if a0.mimeData().hasImage:
            print("dragEnterEvent")
            a0.accept()
        else:
            a0.ignore()

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        if a0.mimeData().hasImage:
            a0.accept()
        else:
            a0.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        if a0.mimeData().hasImage:

            filePath = a0.mimeData().urls()[0].toLocalFile()
            img = cv2.imread(filePath)
            # CommonFunction.Cv2Show(img)
            img = self.ResizeShowImg(img)
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(qimg)
            # pixmap = QPixmap(filePath)
            self.l_img.setPixmap(pixmap)
            a0.setDropAction(Qt.CopyAction)
            self.cv2img = cv2.imread(filePath)
            a0.accept()
        else:
            a0.ignore()

    # 调整显示图片的大小
    def ResizeShowImg(self, img):
        # print(self.l_img.size())
        h, w = img.shape[:2]
        # 把长的一边 等于self.l_img的边长
        # 按照比例缩放
        if h >= w:
            newH = self.l_img.height()
            newW = newH * (w/h)

        else:
            newW = self.l_img.width()
            newH = newW*(h/w)

        print(newH, newW)
        return cv2.resize(img, (int(newW), int(newH),))

    # 粘贴内存图片
    def PasteImage(self):
        clipBoard = QApplication.clipboard()

        if clipBoard.mimeData().hasImage():
            # 得到剪贴板 QImage
            img = clipBoard.image()
            # QImage 转为 opencv Image
            cvImg = CommonFunction.QImageToCvImage(img)
            # 保存待识别img
            self.cv2img = cvImg.copy()

            # 调整图片大小
            img = self.ResizeShowImg(cvImg)

            # 转回 QImage
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_BGR888)
            # 创建 pixmap
            pixmap = QPixmap.fromImage(qimg)
            # pixmap = QPixmap(filePath)
            self.l_img.setPixmap(pixmap)




