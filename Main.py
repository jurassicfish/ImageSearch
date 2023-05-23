#!user/bin/python
# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from ImageSearchUI import ImageSearchDlg


def Main():

    app = QApplication(sys.argv)
    isUI = ImageSearchDlg()
    isUI.show()
    app.exec_()


if __name__ == '__main__':
    Main()
