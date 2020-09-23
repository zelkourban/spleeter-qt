import sys
import os
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TestListView(QListWidget):
    dropped = pyqtSignal(list)

    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(72, 72))
        self.links = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.links = []
            for url in event.mimeData().urls():
                self.links.append(str(url.toLocalFile()))
            self.dropped.emit(self.links)
        else:
            event.ignore()

