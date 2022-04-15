# game_functions.py
import random

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

from settings import Settings
from tableGame import TableGame
from info_table import InfoTable


def shuffling_table(table: TableGame):
    """ Перестановка всех ячеек """
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):

            # Исключение цвета 3 в ряд
            link_color = []
            if col > 1:
                if table.data[row][col - 1] == table.data[row][col - 2]:
                    link_color.append(table.data[row][col - 1])
                    table.link_color_monkey.remove(table.data[row][col - 1])
            if row > 1:
                if table.data[row - 1][col] == table.data[row - 2][col] and table.data[row - 1][
                    col] in table.link_color_monkey:
                    link_color.append(table.data[row - 1][col])
                    table.link_color_monkey.remove(table.data[row - 1][col])

            # выбираем рандомный цвет из возможно оставшихся
            color = random.choice(table.link_color_monkey)
            table.data[row][col] = color

            for el in link_color:
                table.link_color_monkey.append(el)

            if table.mapping[row][col]:
                link = f'image/{color}_monkey_pass'
            else:
                link = f'image/{color}_monkey'

            icon = QIcon(link)
            item_icon = QTableWidgetItem(icon, '')
            table.setItem(row, col, QTableWidgetItem(item_icon))
            table.data[row][col] = color


def update_info_table(ai_settings: Settings, info_table: InfoTable):
    """ Обновление информационной доски """
    # Обновление кол-ва очков
    info_table.score.setText(str(ai_settings.score))
    info_table.tiles_remaining.setText(str(ai_settings.count_of_tiles))


def update_table_by_data(table: TableGame):
    """ Обновляет таблицу по двумерному массиву (поле data - массив хранит color) """
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            if table.mapping[row][col]:
                link = f'image/{table.data[row][col]}_monkey_pass'
            else:
                link = f'image/{table.data[row][col]}_monkey'
            icon = QIcon(link)
            item_icon = QTableWidgetItem(icon, '')
            table.setItem(row, col, item_icon)


def shifting_cells_down(table: TableGame):
    """ Смещение ячеек вниз под которыми пустота (поле date - массив хранит color) """
    for col in range(table.columnCount()):
        step = 0
        row = table.rowCount() - 1
        while row > -1:
            while not table.data[row - step][col]:
                step += 1
            if row - step < 0:
                color = random.choice(table.link_color_monkey)
                table.data[row][col] = color
            else:
                table.data[row][col] = table.data[row - step][col]
            row -= 1


def del_cells(ai_settings: Settings, table: TableGame, rows, columns):
    """
    1) Удаляет одинаковые ячейки 3 или более в ряд.
    2) Помечает ячейки которые уже были уничтожены.
    3) Уменьшение кол-ва оставшихся плиток.
    4) Увеличивает кол-во игровых очков.
    """
    # Удаляет строки
    for row, el in enumerate(rows):
        if el:
            for col in range(el[0][0], el[0][1]):
                del_cell_with_settings(ai_settings, table, row, col)

    # Удаляет столбцы
    for col, el in enumerate(columns):
        if el:
            for row in range(el[0][0], el[0][1]):
                del_cell_with_settings(ai_settings, table, row, col)


def del_cell_with_settings(ai_settings: Settings, table: TableGame, row, col):
    """ del_cells() """
    table.data[row][col] = ""
    if not table.mapping[row][col]:
        table.mapping[row][col] = 1
        ai_settings.count_of_tiles -= 1
        ai_settings.score += ai_settings.points_for_empty_cell
    else:
        ai_settings.score += ai_settings.points_for_non_empty_cell


def find_sequence(table: TableGame):
    """ Находит нет ли 3 в ряд или более одинаковых ячеек
    Возвращает:
    флаг - есть или нет (3 в ряд)
    rows - массив с индексами для удаления ячеек в строке каждой строки
    columns - массив с индексами для удаления ячеек в колонке каждой колонки """
    # Находим ряды с 3 или более повторяющимися цветами
    rows = []
    columns = []
    # Находит строки где есть
    for row in range(table.rowCount()):
        colors = table.data[row]
        line = []
        index = 0
        for i, el in enumerate(colors):
            if colors[index] == el:
                if i + 1 == len(colors) and i + 1 - index > 2:
                    line.append((index, i + 1))
                continue
            else:
                if i - index > 2:
                    line.append((index, i))
                index = i
        rows.append(line)

    # Находит колонки где есть
    for col in range(table.columnCount()):
        cols = []
        index = 0
        for row in range(1, table.rowCount()):
            if table.data[index][col] == table.data[row][col]:
                if row + 1 == table.rowCount() and row + 1 - index > 2:
                    cols.append((index, row + 1))
                continue
            else:
                if row - index > 2:
                    cols.append((index, row))
                index = row
        columns.append(cols)

    flag = False
    for row in rows:
        if row:
            flag = True
            break
    for col in columns:
        if col:
            flag = True
            break
    return flag, rows, columns


def moving_cells(table: TableGame):
    """ Перемещает (в двумерном массиве (поле data - массив хранит color), не в самой таблице) строку или столбец со смещением промежуточных ячеек """
    # Переносим столбцы
    if table.first_row == table.last_row and table.first_col != table.last_col:
        # Вправо
        if table.first_col < table.last_col:
            tmp = table.data[table.first_row][-abs(table.first_col - table.last_col):]
            table.data[table.first_row][abs(table.first_col - table.last_col):] = table.data[table.first_row][0: -abs(table.first_col - table.last_col)]
            table.data[table.first_row][: abs(table.first_col - table.last_col)] = tmp
        # Влево
        else:
            tmp = table.data[table.first_row][:abs(table.first_col - table.last_col)]
            table.data[table.first_row][0: -abs(table.first_col - table.last_col)] = table.data[table.first_row][
                                                                                 abs(table.first_col - table.last_col):]
            table.data[table.first_row][-abs(table.first_col - table.last_col):] = tmp

    # Переносим строки
    elif table.first_row != table.last_row and table.first_col == table.last_col:
        # Вниз
        if table.first_row < table.last_row:
            tmp = []
            for row in range(table.rowCount() - abs(table.first_row - table.last_row), table.rowCount()):
                tmp.append(table.data[row][table.first_col])
            for row in range(table.rowCount() - 1, abs(table.first_row - table.last_row) - 1, -1):
                table.data[row][table.first_col] = table.data[row - abs(table.first_row - table.last_row)][
                    table.first_col]
            for row in range(abs(table.first_row - table.last_row)):
                table.data[row][table.first_col] = tmp[row]
        # Вверх
        else:
            tmp = []
            for row in range(abs(table.first_row - table.last_row)):
                tmp.append(table.data[row][table.first_col])
            for row in range(0, table.rowCount() - abs(table.first_row - table.last_row)):
                table.data[row][table.first_col] = table.data[row + abs(table.first_row - table.last_row)][
                    table.first_col]
            for row in range(table.rowCount() - abs(table.first_row - table.last_row), table.rowCount()):
                table.data[row][table.first_col] = tmp[row - table.rowCount() + abs(table.first_row - table.last_row)]


def update_screen(ai_settings: Settings, table: TableGame, info_table: InfoTable):
    """  """
    # Проверка на окончание игры
    if ai_settings.flag:

        # сдвигает ячейки
        moving_cells(table)

        # Проверка на >= 3 в ряд
        flag, rows, columns = find_sequence(table)

        # Пока существует >= 3 в ряд
        while flag:

            # Удаляет ячейки где >= 3 в ряд
            del_cells(ai_settings, table, rows, columns)

            # Смещает все ячейки вниз после исчезновения >= 3 в ряд
            shifting_cells_down(table)

            # Обновляет таблицу по данным (поле data - массив хранит color)
            update_table_by_data(table)

            # Повторная проверка на >= 3 в ряд
            flag, rows, columns = find_sequence(table)

        # Обновление информационной доски
        update_info_table(ai_settings, info_table)




