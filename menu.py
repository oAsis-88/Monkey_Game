# menu.pu

from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt

from task_5.monkey_Game.game import Game
from task_5.monkey_Game.instructions import Instructions
from task_5.monkey_Game.options import Options
from task_5.monkey_Game.settings import Settings


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai_settings = Settings()
        self.initializeUI()

    def initializeUI(self):
        """ Initialize the window and display its contents to the screen (Menu window) """
        self.setFixedSize(600, 560)
        self.setWindowTitle("Game")

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignHCenter)

        self.displayButton()

        self.widget = QWidget()
        self.widget.setLayout(self.vbox)

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.setCentralWidget(self.widget)
        self.show()


    def displayButton(self):
        """ Display Button (play, exit) """
        self.btn_play = QPushButton('play')
        self.btn_play.clicked.connect(self.event_play)
        self.btn_play.setObjectName("MenuButton")
        self.vbox.addWidget(self.btn_play)

        self.btn_instructions = QPushButton('instructions')
        self.btn_instructions.clicked.connect(self.event_instructions)
        self.btn_instructions.setObjectName("MenuButton")
        self.vbox.addWidget(self.btn_instructions)

        self.btn_options = QPushButton('options')
        self.btn_options.clicked.connect(self.event_options)
        self.btn_options.setObjectName("MenuButton")
        self.vbox.addWidget(self.btn_options)

        self.btn_exit = QPushButton('exit')
        self.btn_exit.clicked.connect(self.event_exit)
        self.btn_exit.setObjectName("MenuButton")
        self.vbox.addWidget(self.btn_exit)

    def event_play(self):
        self.game = Game(self.ai_settings)
        self.game.show()
        self.hide()

    def event_instructions(self):
        """ Open window instructions """
        self.instructions = Instructions()
        self.instructions.show()
        # self.hide()

    def event_options(self):
        """ Open window options """
        self.options = Options(self.ai_settings)
        self.options.show()
        # self.hide()

    def event_exit(self):
        """ When asking the user will close the window authorization"""
        self.close()

    def keyPressEvent(self, e):
        """ keyboard events """

        # Closes the window when you click on the escape button
        if e.key() == Qt.Key_Escape:
            self.close()

        # The game will start when you press the enter button
        elif e.key() == Qt.Key_Return:
            self.event_play()
