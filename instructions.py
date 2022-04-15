# instructions.py
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QAction, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QApplication, QMenu, QGridLayout, QLabel, QLineEdit, QScrollArea, QGroupBox, QFormLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QIcon, QPixmap, QPalette, QBrush, QColor, QPainterPath, QFont
from PyQt5.QtCore import Qt


class Instructions(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Instructions) """
        self.setFixedSize(700, 600)
        self.setWindowTitle('Инструкция')
        # Запрещает взаимодействовать с родительским окном
        self.setWindowModality(Qt.ApplicationModal)

        self.widget = QWidget(self)
        self.widget.move(50, 50)
        self.widget.resize(self.width() - 100, self.height() - 100)
        self.widget.setObjectName("Background_Board")

        self.displayLine()
        self.displayInformation()
        self.displayButton()

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
        self.show()

    # def paintEvent(self, e):
    #     off = 10
    #     painter = QPainter()
    #     path = QPainterPath()
    #     drawFont = QFont("Sans", 20)
    #     path.addText(off, drawFont.pointSize() + off, drawFont, text())
    #     painter.setRenderHints(QPainter.Antialiasing)
    #     painter.strokePath(path, QPen(QColor("#FF8C00"), 4))
    #     painter.fillPath(path, QBrush(Qt.black))
    #     resize(path.boundingRect().size().toSize().width() + off * 2, path.boundingRect().size().toSize().height() + off * 2)

    def displayLine(self):
        """ Display Line Edit (information) """
        self.heading = QLabel(self.widget)
        # heading.setAlignment(Qt.AlignCenter)
        self.heading.resize(self.widget.width(), int(self.widget.width() * 1 / 10))
        self.heading.setObjectName("Title")
        self.heading.setText('How To Play')
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setOffset(1, 1)
        # shadow.setBlurRadius(8.0)
        # shadow.setColor(Qt.black)
        # heading.setGraphicsEffect(shadow)

    def displayInformation(self):
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor(0, 0, 0, 0))

        scroll = QScrollArea(self.widget)
        scroll.move(0, self.heading.height())
        scroll.setPalette(pal)
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setFixedHeight(self.widget.height() - self.heading.height() * 2)
        scroll.resize(self.widget.width(), self.widget.height() - self.heading.height())
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        info = self.get_info_with_txt()  # QVBoxLayout
        widget = QWidget()
        widget.setPalette(pal)
        widget.setLayout(info)

        scroll.setWidget(widget)

    def get_info_with_txt(self):
        info = QVBoxLayout()
        # ======================== Текст инструкции ===========================
        with open('info.txt', 'r') as file:
            for i, line in enumerate(file):
                hbox = QHBoxLayout()

                label = QLabel(line)
                label.setObjectName("Text")
                # label.setWordWrap(True)
                labelImage = QLabel()
                pixmap = QPixmap('image/red_monkey.jpg')
                labelImage.setPixmap(pixmap)

                if i % 2 == 0:
                    hbox.addWidget(label, alignment=Qt.AlignLeft)
                    hbox.addWidget(labelImage, alignment=Qt.AlignRight)
                else:
                    hbox.addWidget(labelImage, alignment=Qt.AlignLeft)
                    hbox.addWidget(label, alignment=Qt.AlignRight)

                # scroll.setLayout(hbox)
                info.addLayout(hbox)
        # =====================================================================
        return info

    def displayButton(self):
        """ Display Button (change password, cancel) """
        # self.btn_prev = QPushButton("Prev", self.widget)
        # self.btn_prev.move(10, 10)
        # self.btn_prev.clicked.connect(self.event_btn_btn_prev)
        #
        # self.btn_next = QPushButton("Next", self.widget)
        # self.btn_next.move(self.widget.width() - self.btn_next.width() // 2 - 10, 10)
        # self.btn_next.clicked.connect(self.event_btn_btn_next)

        self.btn_close = QPushButton("Close", self.widget)
        self.btn_close.resize(200, int(self.widget.width() * 1 / 10))
        self.btn_close.move((self.widget.width() - self.btn_close.width()) // 2,
                            self.widget.height() - self.btn_close.height())
        self.btn_close.clicked.connect(self.event_btn_close)

    # def event_btn_btn_prev(self):
    #     """ Event Will send an email with password recovery. """
    #     pass
    #
    # def event_btn_btn_next(self):
    #     """ Event Will send an email with password recovery. """
    #     pass

    def event_btn_close(self):
        """ Event close window password recovery"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Instructions()
    m.show()
    sys.exit(app.exec_())
