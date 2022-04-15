# timer.py

import time

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QAction, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QApplication, QMenu, QGridLayout, QLabel, QProgressBar, QGraphicsScene, QGraphicsView, QGraphicsLinearLayout, \
    QGraphicsWidget
from PyQt5.QtGui import QPainter, QPen, QIcon, QPixmap, QPalette, QBrush, QTransform, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtCore


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(int)

    def __init__(self, ai_settings, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.ai_settings = ai_settings
        self.running = False  # Флаг выполнения

    def run(self):
        self.running = True
        while self.ai_settings.flag:
            self.ai_settings.time_game -= 1
            self.sleep(1)
            self.mysignal.emit(self.ai_settings.time_game)
            if self.ai_settings.time_game == 0:
                self.ai_settings.flag = False
            if self.ai_settings.count_of_tiles == 0:
                self.ai_settings.flag = False


class Time(QWidget):
    """  """
    def __init__(self, ai_settings, parent=None):
        super().__init__()
        self.par = parent
        self.ai_settings = ai_settings
        self.time_game = self.ai_settings.time_game
        self.setFixedWidth(50)

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.initializeUI()

    def initializeUI(self):

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.bar = QProgressBar()
        self.bar.setObjectName("Timer")
        self.bar.setFixedHeight(int(self.par.height() * 8 / 10))
        self.bar.setValue(int(self.ai_settings.time_game * 5 / 3))
        self.bar.setFormat("")
        self.bar.setOrientation(Qt.Vertical)

        self.mythread = MyThread(self.ai_settings)
        self.mythread.start()
        self.mythread.mysignal.connect(self.on_change, Qt.QueuedConnection)

        self.vbox.addWidget(self.bar)
        self.setLayout(self.vbox)

    def on_change(self, s):
        self.bar.setValue(int(s * 100 / self.time_game))
        if not self.ai_settings.flag:
            self.show_popup()

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Game over")
        msg.setText("Конец игры")
        msg.setStandardButtons(QMessageBox.Cancel)
        bttn = msg.exec_()

        if bttn == QMessageBox.Cancel:
            self.par.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.rotate(90)
        painter.setPen(Qt.blue)
        painter.setFont(QFont("Arial", 14))
        painter.drawText(0, int(-self.width() / 2 + 7), "Time")

