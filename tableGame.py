# tableGame.py

import random

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem

from task_5.monkey_Game import game_functions as gf
from task_5.monkey_Game.settings import Settings


class TableGame(QTableWidget):
    def __init__(self, ai_settings: Settings, info_table):
        super().__init__()
        self.ai_settings = ai_settings
        self.info_table = info_table
        self.first_row = 0
        self.first_col = 0
        self.last_row = 0
        self.last_col = 0
        self.data = list(['' for _ in range(ai_settings.count_columns)] for _ in range(ai_settings.count_rows))
        self.mapping = list([0 for _ in range(ai_settings.count_columns)] for _ in range(ai_settings.count_rows))
        self.link_color_monkey = ['blue', 'green', 'pink', 'red', 'yellow']

        # Заполнение данных цветами
        self.filling_data()

        # Создание таблицы и ее интерфейса
        self.setupUI()

        self.setFixedWidth(self.ai_settings.count_columns * self.ai_settings.size_cell + 5)

    def setupUI(self):
        """ Создает таблицу с отображением контактов """
        self.setRowCount(self.ai_settings.count_rows)
        self.setColumnCount(self.ai_settings.count_columns)

        # Убирает вертикальный заголовок
        self.verticalHeader().setVisible(False)

        # Убирает горизонтальный заголовок
        self.horizontalHeader().setVisible(False)

        # Удаляет вертикальную полосу прокрутки
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Удаляет горизонтальную полосу прокрутки
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Запрещает выделять ячейки
        self.setSelectionMode(QAbstractItemView.NoSelection)

        # Запрещает изменять содержимое ячейки
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # # Установить таблицу как выделение целой строки
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        #
        # # Установить таблицу как выделение целой колонки
        # self.setSelectionBehavior(QAbstractItemView.SelectColumns)

        # Установите размер картинки
        self.setIconSize(QSize(self.ai_settings.size_cell, self.ai_settings.size_cell))

        for row in range(self.ai_settings.count_rows):
            self.setRowHeight(row, self.ai_settings.size_cell)
            for col in range(self.ai_settings.count_columns):
                self.setColumnWidth(col, self.ai_settings.size_cell)

                icon = QIcon(f'image/{self.data[row][col]}_monkey')
                item_icon = QTableWidgetItem(icon, '')
                self.setItem(row, col, item_icon)

                # label = QLabel()
                # pixmap = QPixmap(f'image/{color}_monkey')
                # _size = QSize(50, 50)
                # label.setPixmap(pixmap.scaled(_size, Qt.KeepAspectRatio))
                # self.setCellWidget(row, col, label)
                # self.data[row][col] = label

    def filling_data(self):
        # Заполнение данных цветами
        for row in range(self.ai_settings.count_rows):
            for col in range(self.ai_settings.count_columns):

                # Исключение цвета 3 в ряд
                link_color = []
                if col > 1:
                    if self.data[row][col - 1] == self.data[row][col - 2]:
                        link_color.append(self.data[row][col - 1])
                        self.link_color_monkey.remove(self.data[row][col - 1])
                if row > 1:
                    if self.data[row - 1][col] == self.data[row - 2][col] and self.data[row - 1][col] in self.link_color_monkey:
                        link_color.append(self.data[row - 1][col])
                        self.link_color_monkey.remove(self.data[row - 1][col])

                # выбираем рандомный цвет из возможно оставшихся
                color = random.choice(self.link_color_monkey)
                self.data[row][col] = color

                for el in link_color:
                    self.link_color_monkey.append(el)


    def mousePressEvent(self, e):
        """ Обработка события нажатия кнопки мыши """
        QTableWidget.mousePressEvent(self, e)  # в начале правильная обработка
        if e.button() == Qt.LeftButton:
            self.first_row = self.currentRow()
            self.first_col = self.currentColumn()

    def mouseReleaseEvent(self, e):
        """ Обработка события отпуская кнопки мыши """
        QTableWidget.mouseReleaseEvent(self, e)  # в начале правильная обработка
        if e.button() == Qt.LeftButton:
            self.last_row = self.currentRow()
            self.last_col = self.currentColumn()

            gf.update_screen(self.ai_settings, self, self.info_table)






    # def function(self):
    #     self.logic()
    #
    #     flag, rows, columns = self.checking_for_match()
    #     while flag:
    #         self.update_game_state(rows, columns)
    #         flag, rows, columns = self.checking_for_match()
    #
    # def update_game_state(self, rows, columns):
    #     print(rows)
    #     print(columns)
    #     print("-----")
    #     self.del_cells(rows, columns)
    #     self.update_cells()
    #     self.update_table()
    #
    # def update_table(self):
    #     """ Обновляет таблицу по двумерному массиву (поле data - хранит color) """
    #     for row in range(6):
    #         for col in range(9):
    #             if self.mapping[row][col]:
    #                 link = f'image/{self.data[row][col]}_monkey_pass'
    #             else:
    #                 link = f'image/{self.data[row][col]}_monkey'
    #             icon = QIcon(link)
    #             item_icon = QTableWidgetItem(icon, '')
    #             self.setItem(row, col, QTableWidgetItem(item_icon))
    #
    # def update_cells(self):
    #     """ Обновляет массив сдвигая все элементы вниз под которыми пустота """
    #     for col in range(self.columnCount()):
    #         step = 0
    #         row = self.rowCount() - 1
    #         while row > -1:
    #             while not self.data[row - step][col]:
    #                 step += 1
    #             if row - step < 0:
    #                 color = random.choice(self.link_color_monkey)
    #                 self.data[row][col] = color
    #
    #                 # self.data[row][col] = ""
    #             else:
    #                 self.data[row][col] = self.data[row - step][col]
    #             row -= 1
    #
    #         for row in range(self.rowCount()):
    #             pass
    #
    #     # # Выводит таблицу
    #     # print("print")
    #     # for row in range(self.rowCount()):
    #     #     for col in range(self.columnCount()):
    #     #         print("%-8s" % self.data[row][col], end=" ")
    #     #     print()
    #     # print("\n---------------\n")
    #
    #
    # def del_cells(self, rows, columns):
    #     """
    #     1) Удаляет одинаковые ячейки 3 или более в ряд.
    #     2) Помечает ячейки которые уже были уничтожены.
    #     """
    #     # Удаляет строки
    #     for row, el in enumerate(rows):
    #         if el:
    #             for col in range(el[0][0], el[0][1]):
    #                 self.data[row][col] = ""
    #                 self.mapping[row][col] = 1
    #
    #     # Удаляет столбцы
    #     for col, el in enumerate(columns):
    #         if el:
    #             for row in range(el[0][0], el[0][1]):
    #                 self.data[row][col] = ""
    #                 self.mapping[row][col] = 1
    #
    #     # Выводит таблицу
    #     # print("print")
    #     # for row in range(self.rowCount()):
    #     #     for col in range(self.columnCount()):
    #     #         print("%-8s" % self.data[row][col], end=" ")
    #     #     print()
    #     # print("\n---------------\n")
    #
    # def checking_for_match(self):
    #     """ Проверяет нет ли 3 в ряд или более одинаковых ячеек
    #     Возвращает:
    #     флаг - есть или нет
    #     rows - массив с индексами для удаления ячеек в строке каждой строки
    #     columns - массив с индексами для удаления ячеек в колонке каждой колонки """
    #     # Находим ряды с 3 или более повторяющимися цветами
    #     rows = []
    #     columns = []
    #     for row in range(self.rowCount()):
    #         colors = self.data[row]
    #         # print(f"-- row[{row}] --")
    #         # print(colors)
    #         line = []
    #         index = 0
    #         for i, el in enumerate(colors):
    #             if colors[index] == el:
    #                 if i + 1 == len(colors) and i + 1 - index > 2:
    #                     line.append((index, i + 1))
    #                 continue
    #             else:
    #                 if i - index > 2:
    #                     line.append((index, i))
    #                 index = i
    #         rows.append(line)
    #         # print(line)
    #     # print("\n-----------------\n")
    #
    #     # Находим столбцы с 3 или более повторяющимися цветами
    #     for col in range(self.columnCount()):
    #
    #         # print(f"-- col[{col}] --")
    #         # print([self.data[row][col] for row in range(6)])
    #         cols = []
    #         index = 0
    #         for row in range(1, self.rowCount()):
    #             if self.data[index][col] == self.data[row][col]:
    #                 if row + 1 == self.rowCount() and row + 1 - index > 2:
    #                     cols.append((index, row + 1))
    #                 continue
    #             else:
    #                 if row - index > 2:
    #                     cols.append((index, row))
    #                 index = row
    #
    #         columns.append(cols)
    #         # print(cols)
    #     # print("\n-----------------\n")
    #
    #     flag = False
    #     for row in rows:
    #         if row:
    #             flag = True
    #             break
    #     for col in columns:
    #         if col:
    #             flag = True
    #             break
    #     return flag, rows, columns
    #
    # def logic(self):
    #     """ Перемещает (в двумерном массиве (поле data), не в самой таблице) строку или столбец со смещением промежуточных ячеек """
    #     # Переносим столбцы
    #     if self.first_row == self.last_row and self.first_col != self.last_col:
    #         if self.first_col < self.last_col:
    #             tmp = self.data[self.first_row][-abs(self.first_col - self.last_col):]
    #             self.data[self.first_row][abs(self.first_col - self.last_col):] = self.data[self.first_row][0: -abs(
    #                 self.first_col - self.last_col)]
    #             self.data[self.first_row][: abs(self.first_col - self.last_col)] = tmp
    #         else:
    #             tmp = self.data[self.first_row][:abs(self.first_col - self.last_col)]
    #             self.data[self.first_row][0: -abs(self.first_col - self.last_col)] = self.data[self.first_row][
    #                                                                                  abs(self.first_col - self.last_col):]
    #             self.data[self.first_row][-abs(self.first_col - self.last_col):] = tmp
    #
    #     # Переносим строки
    #     elif self.first_row != self.last_row and self.first_col == self.last_col:
    #         # difference =
    #         if self.first_row < self.last_row:
    #             tmp = []
    #             for row in range(self.rowCount() - abs(self.first_row - self.last_row), self.rowCount()):
    #                 tmp.append(self.data[row][self.first_col])
    #             for row in range(self.rowCount() - 1, abs(self.first_row - self.last_row) - 1, -1):
    #                 self.data[row][self.first_col] = self.data[row - abs(self.first_row - self.last_row)][
    #                     self.first_col]
    #             for row in range(abs(self.first_row - self.last_row)):
    #                 self.data[row][self.first_col] = tmp[row]
    #         else:
    #             tmp = []
    #             for row in range(abs(self.first_row - self.last_row)):
    #                 tmp.append(self.data[row][self.first_col])
    #             for row in range(0, self.rowCount() - abs(self.first_row - self.last_row)):
    #                 self.data[row][self.first_col] = self.data[row + abs(self.first_row - self.last_row)][
    #                     self.first_col]
    #             for row in range(self.rowCount() - abs(self.first_row - self.last_row), self.rowCount()):
    #                 self.data[row][self.first_col] = tmp[row - self.rowCount() + abs(self.first_row - self.last_row)]
    #
    #     # # Обновляет таблицу по двумерному массиву (поле data - хранит color)
    #     # for row in range(6):
    #     #     for col in range(9):
    #     #         icon = QIcon(f'image/{self.data[row][col]}_monkey')
    #     #         item_icon = QTableWidgetItem(icon, '')
    #     #         self.setItem(row, col, QTableWidgetItem(item_icon))
    #
    #             # self.setItem(row, col, QTableWidgetItem(self.data[row][col]))
    #
    #
    # def logic2(self):
    #     """ Перемещает (в двумерном массиве (поле data), не в самой таблице) строку или столбец со смещением промежуточных ячеек """
    #     # Переносим столбцы
    #     if self.first_row == self.last_row and self.first_col != self.last_col:
    #         step = 1 if self.first_col < self.last_col else -1
    #         for row in range(self.rowCount()):
    #             tmp = self.data[row][self.first_col]
    #             for col in range(self.first_col, self.last_col, step):
    #                 self.data[row][col] = self.data[row][col + step]
    #             self.data[row][self.last_col] = tmp
    #
    #     # Переносим строки
    #     elif self.first_row != self.last_row and self.first_col == self.last_col:
    #         step = 1 if self.first_row < self.last_row else -1
    #         tmp = self.data[self.first_row][:]
    #         for row in range(self.first_row, self.last_row, step):
    #             for col in range(self.columnCount()):
    #                 self.data[row][col] = self.data[row + step][col]
    #         self.data[self.last_row][:] = tmp
    #
    #     self.printTable()
    #     self.printData()
    #
    #     print("\n----- data -> table -----\n")
    #     # Обновляет таблицу по двумерному массиву (поле data)
    #     for row in range(6):
    #         for col in range(9):
    #             print(row, col, self.cellWidget(row, col), end=" - ")
    #             # self.setItem(row, col, QTableWidgetItem(self.data[row][col]))
    #             self.setCellWidget(row, col, self.data[row][col])
    #             print(self.cellWidget(row, col), end="    |    ")
    #         print()
    #     print()
    #
    #     self.printTable()
    #
    #     # Обновляет таблицу по двумерному массиву (поле data)
    #     for row in range(6):
    #         for col in range(9):
    #             self.setCellWidget(row, col, self.data[row][col])
    #
    #     self.printTable()
    #
    #     print("\n------------------\n")
    #
    # def printTable(self):
    #     print("----- table -----\n")
    #     for row in range(6):
    #         for col in range(9):
    #             print(row, col, self.cellWidget(row, col), end="    |    ")
    #         print()
    #     print()
    #
    # def printData(self):
    #     print("\n----- data ------\n")
    #     for row in range(6):
    #         for col in range(9):
    #             print(self.data[row][col], end="    |    ")
    #         print()
    #     print()
