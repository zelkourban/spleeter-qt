#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import sys
import os
import subprocess
from qprocess import Console
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from drag import TestListView


class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.gui = WidgetGallery()
        self.setCentralWidget(self.gui)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.createTitle()

        self.createTopInput()
        self.createRadioButtons()

        self.createButtonGroup()
        self.createDebugWindow()

        topLayout = QHBoxLayout()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.titleLabel, 0, 0, 1, 2)
        mainLayout.addWidget(self.topInput, 1, 0, 1, 2)
        mainLayout.addWidget(self.radioButtons, 2, 0, 1, 2)
        mainLayout.addWidget(self.buttonGroup, 3, 0, 1, 2)
        mainLayout.addWidget(self.debugWindow, 4, 0, 1, 2)
        self.setLayout(mainLayout)

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                fileInfo = QFileInfo(url)
                print(fileInfo)
                iconProvider = QFileIconProvider()
                icon = iconProvider.icon(fileInfo)
                item = QListWidgetItem(url, self.view)
                item.setIcon(icon)
                item.setStatusTip(url)

    def createButtonGroup(self):
        self.buttonGroup = QGroupBox()
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.start)
        layout = QHBoxLayout()
        layout.addWidget(self.startButton)
        self.buttonGroup.setLayout(layout)

    def createTitle(self):
        self.titleLabel = QLabel("Spleeter GUI")
        self.titleLabel.setFont(QFont("Arial", 15))
        self.titleLabel.setAlignment(Qt.AlignCenter)

    def createTopInput(self):
        self.topInput = QGroupBox("Input File")
        # urlLabel = QLabel("URL")
        # urlTextInput = QLineEdit()
        fileLabel = QLabel("Drop audio")
        self.view = TestListView(self)
        self.view.dropped.connect(self.fileDropped)

        fileDialog = self.view
        # url = QHBoxLayout()
        # url.addWidget(urlLabel)
        # url.addWidget(urlTextInput)
        file = QHBoxLayout()
        file.addWidget(fileLabel)
        file.addWidget(fileDialog)
        layout = QVBoxLayout()
        # layout.addLayout(url)
        layout.addLayout(file)
        self.topInput.setLayout(layout)

    def createRadioButtons(self):
        self.radioButtons = QGroupBox("Output format")

        self.radioButton1 = QRadioButton("Instrumental")
        self.radioButton2 = QRadioButton("Vocals")
        self.radioButton3 = QRadioButton("Both")
        self.radioButton1.toggled.connect(lambda: self.radioFormat(self.radioButton1))
        self.radioButton2.toggled.connect(lambda: self.radioFormat(self.radioButton2))
        self.radioButton3.toggled.connect(lambda: self.radioFormat(self.radioButton3))

        self.format = 2
        self.radioButton3.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addWidget(self.radioButton3)
        layout.addStretch(1)
        self.radioButtons.setLayout(layout)

    def radioFormat(self, rButton):
        if rButton.text() == "Instrumental":
            if rButton.isChecked() == True:
                self.format = "instrumental"
                print("instrumental selected")
        if rButton.text() == "Vocals":
            if rButton.isChecked() == True:
                self.format = "vocals"
                print("vocals selected")
        if rButton.text() == "Both":
            if rButton.isChecked() == True:
                self.format = ""
                print("both selected")

    def createDebugWindow(self):
        self.debugWindow = QGroupBox("Debug")
        self.debug = Console()
        self.debug.errorSignal.connect(lambda error: print(error))
        self.debug.outputSignal.connect(lambda output: print(output))
        layout = QVBoxLayout()
        layout.addWidget(self.debug)
        self.debugWindow.setLayout(layout)

    def start(self):
        MYDIR = "audio"
        CHECK_FOLDER = os.path.isdir(MYDIR)

        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(MYDIR)
            print("created folder : ", MYDIR)
        else:
            print(MYDIR, "folder already exists.")

        self.debug.run(
            f"./split_audio_from_file.sh -i {self.view.links[0]} -o audio -f {self.format}"
        )


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    sys.exit(app.exec_())

