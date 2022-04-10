import sys
from PyQt5 import QtWidgets

from task_5.monkey_Game.menu import Menu


def application():
    app = QtWidgets.QApplication(sys.argv)
    m = Menu()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
