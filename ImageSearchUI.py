#!user/bin/python
# -*- coding:utf-8 -*-
"""
功能包括
1、识别图片中包含的文字
2、根据文字 搜索图片
3、识别图中物品
4、根据物品类型搜图
5、根据人脸搜图
6、拍照
7、视频录制
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QListView, QSplitter, QStackedWidget, QHBoxLayout, QListWidget

import TextPic
from ObjImgSearch import ObjImgSearchDlg
from ObjectIdentify import ObjectIdentifyDlg
from OcrIdentify import OcrIdentifyDlg
from OcrImgSearch import OcrImgSearchDlg
from PcCamera import CameraDlg
from PcVideo import VideoDlg
from PersonSearch import PersonSearchDlg


class ImageSearchDlg(QDialog):
    def __init__(self):
        super(ImageSearchDlg, self).__init__()

        self.lw_function = None
        self.videoDlg = None
        self.cameraDlg = None
        self.personSearchDlg = None
        self.objImgSearchDlg = None
        self.objIdentifyDlg = None
        self.ocrImageSearchDlg = None
        self.ocrImageSearch = None
        self.ocrIdentifyDlg = None
        self.sw_function = None
        self.s_mainSplitter = None
        self.lv_function = None

        self.functions = ['识别图片文字', '根据文本搜图', '识别图中物品', '根据物品搜图', '根据人脸搜图', '拍照', '视频']
        self.appNameCN = '图像搜索'
        self.appNameCN = 'ImageSearch'
        self.appVersion = '1.00'

        self.InitUIPart()
        self.UILayout()
        self.ConnectSignalSlot()
        self.InitUIData()
        self.InitDialog()
        self.LoadQss()
        self.LoadSettings()

    def InitUIPart(self):
        # splitter
        self.s_mainSplitter = QSplitter()
        # 方向
        self.s_mainSplitter.setOrientation(Qt.Orientation.Horizontal)
        # 分割透明
        self.s_mainSplitter.setOpaqueResize(True)

        # 过窄不隐藏
        self.s_mainSplitter.setChildrenCollapsible(0)
        # 设置分界线宽度
        self.s_mainSplitter.setHandleWidth(2)

        # 功能列表
        self.lw_function = QListWidget()

        # 窗口stack
        self.sw_function = QStackedWidget()

        # 功能窗口
        self.ocrIdentifyDlg = OcrIdentifyDlg()
        self.ocrImageSearchDlg = OcrImgSearchDlg()
        self.objIdentifyDlg = ObjectIdentifyDlg()
        self.objImgSearchDlg = ObjImgSearchDlg()
        self.personSearchDlg = PersonSearchDlg()
        self.cameraDlg = CameraDlg()
        self.videoDlg = VideoDlg()

        # 添加功能窗口
        self.sw_function.addWidget(self.ocrIdentifyDlg)
        self.sw_function.addWidget(self.ocrImageSearchDlg)
        self.sw_function.addWidget(self.objIdentifyDlg)
        self.sw_function.addWidget(self.objImgSearchDlg)
        self.sw_function.addWidget(self.personSearchDlg)
        self.sw_function.addWidget(self.cameraDlg)
        self.sw_function.addWidget(self.videoDlg)

    def UILayout(self):
        self.s_mainSplitter.addWidget(self.lw_function)
        self.s_mainSplitter.addWidget(self.sw_function)

        hBox = QHBoxLayout()
        hBox.addWidget(self.s_mainSplitter)

        self.setLayout(hBox)

    def ConnectSignalSlot(self):
        pass

    def InitUIData(self):
        # 添加列表功能
        for (idx, name) in enumerate(self.functions):
            self.lw_function.insertItem(idx, name)

        # 列表宽度
        self.lw_function.setMaximumWidth(100)
        # self.s_mainSplitter.setStretchFactor(2, 4)
        # self.s_mainSplitter.setSizes([200, 400])

        # splitter 不可调整
        self.s_mainSplitter.handle(1).setDisabled(True)

    def InitDialog(self):
        # 窗口标题s
        self.setWindowTitle(self.appNameCN + self.appVersion)

        # 窗口风格
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

        # 标题栏图标
        img = QImage.fromData(TextPic.PicData.AppPic())
        # img = QImage.fromData(self.picData.appPic())
        pixMap = QPixmap.fromImage(img)
        icon = QIcon(pixMap)
        self.setWindowIcon(icon)

        # 窗口大小
        self.resize(600, 600)

    def LoadQss(self):
        pass

    def LoadSettings(self):
        pass
