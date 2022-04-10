# info_table.py

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from task_5.monkey_Game import game_functions as gf


class InfoTable(QWidget):
    def __init__(self, ai_settings):
        super().__init__()
        self.setObjectName("InfoTable")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(170)

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.ai_settings = ai_settings
        self.tableGame = None
        self.initializeUI()

    def initializeUI(self):

        """ Initialize the window and display its contents to the screen (info table) """
        self.data_widget = QVBoxLayout()
        self.data_widget.setAlignment(Qt.AlignCenter)


        self.score_name = QLabel("Score")
        self.score_name.setAlignment(Qt.AlignCenter)
        self.score_name.setFixedWidth(self.width() - 20)

        self.score = QLabel(str(self.ai_settings.score))
        self.score.setAlignment(Qt.AlignCenter)

        self.tiles_remaining_name = QLabel("Tiles\nRemaining")
        self.tiles_remaining_name.setAlignment(Qt.AlignCenter)

        self.tiles_remaining = QLabel(str(self.ai_settings.count_of_tiles))
        self.tiles_remaining.setAlignment(Qt.AlignCenter)

        self.btn_shuffle = QPushButton("Shuffle")
        self.btn_shuffle.clicked.connect(self.shuffling)


        self.data_widget.addWidget(self.score_name)
        self.data_widget.addWidget(self.score)
        self.data_widget.addWidget(self.tiles_remaining_name)
        self.data_widget.addWidget(self.tiles_remaining)
        self.data_widget.addWidget(self.btn_shuffle)
        self.setLayout(self.data_widget)

    def shuffling(self):
        """ Перестановка всех ячеек """
        gf.shuffling_table(self.tableGame)

    @property
    def score_title(self):
        return self.score_name

    @property
    def tiles_remaining_title(self):
        return self.tiles_remaining_name