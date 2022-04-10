# options.py
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QAction, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QApplication, QMenu, QGridLayout, QLabel, QLineEdit, QGraphicsDropShadowEffect, QTableWidget, QTableView, \
    QTableWidgetItem
from PyQt5.QtCore import Qt, QLine, QPointF
from PyQt5.QtGui import QPainter, QPen, QIcon, QPixmap, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt

from settings import Settings


class Options(QWidget):
    def __init__(self, ai_settings: Settings):
        super().__init__()
        self.ai_settings = ai_settings
        self.initializeUI()

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Options) """
        self.setFixedSize(800, 700)
        self.setWindowTitle('Настройки')
        self.setWindowModality(Qt.ApplicationModal)

        self.widget = QWidget(self)
        self.widget.move(50, 50)
        self.widget.resize(self.width() - 100, self.height() - 100)
        self.widget.setObjectName("Background_Board")


        self.vbox = QVBoxLayout()
        self.titleLayout = QHBoxLayout()
        self.layout = QHBoxLayout()
        self.buttonTableLayout = QVBoxLayout()
        self.settingsLayout = QVBoxLayout()

        self.layout.addLayout(self.buttonTableLayout)
        self.layout.addLayout(self.settingsLayout)
        self.vbox.addLayout(self.titleLayout)
        self.vbox.addLayout(self.layout)
        self.widget.setLayout(self.vbox)

        self.displayLine()
        self.displaySizeTable()
        self.displayButton()

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)
        self.show()

    def displayLine(self):
        """ Display Line Edit (heading) """
        heading = QLabel()
        # heading.setAlignment(Qt.AlignCenter)
        heading.resize(self.widget.width(), int(self.widget.width() * 1 / 10))
        heading.setObjectName("Title")
        heading.setText('Options')
        self.titleLayout.addWidget(heading)


    def displaySizeTable(self):
        """ Display edit size field """

        plus_row = QPushButton("+ row")
        plus_row.setObjectName("ButtonOptions")
        plus_row.clicked.connect(self.event_btn_plus_row)

        minus_row = QPushButton("- row")
        minus_row.setObjectName("ButtonOptions")
        minus_row.clicked.connect(self.event_btn_minus_row)

        plus_column = QPushButton("+ col")
        plus_column.setObjectName("ButtonOptions")
        plus_column.clicked.connect(self.event_btn_plus_column)

        minus_column = QPushButton("- col")
        minus_column.setObjectName("ButtonOptions")
        minus_column.clicked.connect(self.event_btn_minus_column)

        # vbox.addLayout(btn_hbox)
        self.buttonTableLayout.addWidget(plus_row)
        self.buttonTableLayout.addWidget(minus_row)
        self.buttonTableLayout.addWidget(plus_column)
        self.buttonTableLayout.addWidget(minus_column)

        self.table = QTableWidget()
        self.table.resize(100, 100)
        self.table.setRowCount(self.ai_settings.count_rows)
        self.table.setColumnCount(self.ai_settings.count_columns)
        for row in range(self.ai_settings.count_rows):
            self.table.setRowHeight(row, 20)
            for col in range(self.ai_settings.count_columns):
                self.table.setColumnWidth(col, 20)
                self.table.setItem(row, col, QTableWidgetItem(""))
        self.buttonTableLayout.addWidget(self.table)

    def displayButton(self):
        """ Display Button (music, sfx, color_blind, help, reset_scores, back) """
        music = QPushButton("Music")
        music.setObjectName("ButtonOptions")
        music.clicked.connect(self.event_btn_music)

        sfx = QPushButton("Sfx")
        sfx.setObjectName("ButtonOptions")
        sfx.clicked.connect(self.event_btn_sfx)

        color_blind = QPushButton("colorBlind")
        color_blind.setObjectName("ButtonOptions")
        color_blind.clicked.connect(self.event_btn_color_blind)

        help = QPushButton("Help")
        help.setObjectName("ButtonOptions")
        help.clicked.connect(self.event_btn_help)

        reset_scores = QPushButton("Reset Scores")
        reset_scores.setObjectName("ButtonOptions")
        reset_scores.clicked.connect(self.event_btn_reset_scores)

        back = QPushButton("Back")
        back.setObjectName("ButtonOptions")
        back.clicked.connect(self.event_btn_back)

        self.settingsLayout.addWidget(music)
        self.settingsLayout.addWidget(sfx)
        self.settingsLayout.addWidget(color_blind)
        self.settingsLayout.addWidget(help)
        self.settingsLayout.addWidget(reset_scores)
        self.settingsLayout.addWidget(back)


    def event_btn_plus_row(self):
        count_row = self.table.rowCount()
        if count_row < self.ai_settings.max_count_rows:
            self.table.insertRow(count_row)
            self.table.setRowHeight(count_row, 20)
            self.ai_settings.count_rows = self.table.rowCount()
            self.ai_settings.count_of_tiles = self.table.rowCount() * self.table.columnCount()

    def event_btn_plus_column(self):
        count_column = self.table.columnCount()
        if count_column < self.ai_settings.max_count_columns:
            self.table.insertColumn(count_column)
            self.table.setColumnWidth(count_column, 20)
            self.ai_settings.count_columns = self.table.columnCount()
            self.ai_settings.count_of_tiles = self.table.rowCount() * self.table.columnCount()

    def event_btn_minus_row(self):
        count_row = self.table.rowCount()
        if count_row > self.ai_settings.min_count_rows:
            self.table.removeRow(count_row - 1)
            self.ai_settings.count_rows = self.table.rowCount()
            self.ai_settings.count_of_tiles = self.table.rowCount() * self.table.columnCount()

    def event_btn_minus_column(self):
        count_column = self.table.columnCount()
        if count_column > self.ai_settings.min_count_columns:
            self.table.removeColumn(count_column - 1)
            self.ai_settings.count_columns = self.table.columnCount()
            self.ai_settings.count_of_tiles = self.table.rowCount() * self.table.columnCount()

    def event_btn_music(self):
        pass

    def event_btn_sfx(self):
        pass

    def event_btn_color_blind(self):
        pass

    def event_btn_help(self):
        pass

    def event_btn_reset_scores(self):
        pass

    def event_btn_back(self):
        """ Event close window password recovery"""
        self.close()

    # def paintEvent(self, e):
    #     painter = QPainter()
    #     painter.begin(self)
    #     # ======== Начало вставки ===============
    #     # Используйте сглаживание для сглаживания изогнутых краев
    #     painter.setRenderHint(QPainter.Antialiasing)
    #
    #     color = QColor('blue')
    #     pen = QPen(color, 16)
    #     painter.setPen(pen)
    #
    #     painter.drawText(600, 500, "Text")
    #     # ========= Конец вставки ================
    #     painter.end()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Options(Settings())
    m.show()
    sys.exit(app.exec_())