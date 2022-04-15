# menu.pu
import sys

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QGridLayout
from PyQt5.QtCore import Qt

from settings import Settings
from task_5.monkey_Game.tableGame import TableGame
from info_table import InfoTable
from task_5.monkey_Game.timer import Time


class Game(QMainWindow):
    def __init__(self, ai_settings: Settings):
        super().__init__()
        self.ai_settings = ai_settings
        self.initializeUI()

    def initializeUI(self):
        """ Initialize the window and display its contents to the screen (Menu window) """
        # size : cell-50px * count-13 = 650
        # self.setFixedSize(732, 652)
        self.setWindowTitle("Game")
        screen_game_height = self.ai_settings.count_rows * self.ai_settings.size_cell + 20
        self.setFixedHeight(screen_game_height)

        self.widget = QWidget()
        self.box = QGridLayout()
        self.display()
        self.widget.setLayout(self.box)

        screen_game_wight = self.ai_settings.count_columns * self.ai_settings.size_cell + self.info_table.width() + self.time.width() * 2
        self.setFixedWidth(screen_game_wight)

        with open("style.css", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.setCentralWidget(self.widget)
        self.show()


    def display(self):
        """ Display game """
        # self.box.setAlignment(Qt.AlignHCenter)

        self.info_table = InfoTable(self.ai_settings)

        self.tableGame = TableGame(self.ai_settings, self.info_table)

        self.info_table.tableGame = self.tableGame

        self.time = Time(self.ai_settings, self)

        self.box.addWidget(self.info_table, 0, 0)
        self.box.addWidget(self.tableGame, 0, 1)
        self.box.addWidget(self.time, 0, 2)

    def keyPressEvent(self, e):
        """ keyboard events """

        # Closes the window when you click on the escape button
        if e.key() == Qt.Key_Escape:
            self.close()

        # The game will start when you press the enter button
        # elif e.key() == Qt.Key_Return:
        #     self.event_sign_in()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ai_setting = Settings()
    m = Game(ai_setting)
    m.show()
    sys.exit(app.exec_())