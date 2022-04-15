# settings.py

class Settings():
    def __init__(self):

        # Размер ячейки в игре
        self.size_cell = 100  # 50 x 50

        # Размер поля
        self.count_rows = 6
        self.count_columns = 9

        # Время игры
        self.time_game = 100  # в секундах

        # Кол-во оставшихся плиток
        self.count_of_tiles = self.count_rows * self.count_columns

        # Кол-во очков
        self.score = 0

        # Кол-во очков за разбитую ячейку
        self.points_for_empty_cell = 30

        # Кол-во очков за не разбитую ячейку
        self.points_for_non_empty_cell = 20

        # Флаг окончания игры
        self.flag = True

        # Максимальный и минимальный размер
        self.min_count_rows = 4
        self.min_count_columns = 6
        self.max_count_rows = 9
        self.max_count_columns = 12
