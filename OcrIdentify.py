#!user/bin/python
# -*- coding:utf-8 -*-
"""
功能包括
1、识别图片中包含的文字 界面
"""
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog
import pytesseract
import cv2

import CommonFunction
import TextPic
from CommonFunction import GetAppDir


class OcrIdentifyDlg(QDialog):
    def __init__(self):
        super(OcrIdentifyDlg, self).__init__()

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
        self.InitUIData()
        self.InitDialog()
        self.LoadQss()
        self.LoadSettings()

    def InitUIPart(self):
        self.l_img = QLabel()
        self.l_img.setObjectName("OIImageShow")
        self.l_img.setScaledContents(True)

        self.bt_select = QPushButton("选择\n图片")
        self.bt_select.setObjectName("OIImgSelect")
        self.bt_area = QPushButton("区域\n调整")
        self.bt_area.setObjectName("OIArea")
        self.bt_identify = QPushButton("识别\n内容")
        self.bt_identify.setObjectName("OIIdentify")

        self.te_text = QTextEdit()
        self.te_text.setReadOnly(True)

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

    def InitUIData(self):
        # 标题栏图标
        img = QImage.fromData(TextPic.PicData.AppPic())
        # img = QImage.fromData(self.picData.appPic())
        pixMap = QPixmap.fromImage(img)
        icon = QIcon(pixMap)

        self.l_img.setPixmap(pixMap)

    def InitDialog(self):
        pass

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
        qimg = QImage(imgShow.data, imgShow.shape[1], imgShow.shape[0], imgShow.shape[1] * 3, QImage.Format_BGR888)
        self.l_img.setPixmap(QPixmap.fromImage(qimg))

    # 识别图片中文字
    def IdentifyContent(self):
        # 复制
        img = self.cv2img.copy()
        # 灰度
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        CommonFunction.Cv2Show(img)
        # 二值处理
        img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)[1]

        CommonFunction.Cv2Show(img)

        result = pytesseract.image_to_string(img, lang='chi_sim')
        print(result)

        self.te_text.setText(result)
