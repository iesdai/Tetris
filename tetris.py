import pygame as pg

import settings

from copy import deepcopy
import random


class Tetris:
    def __init__(self):
        # Инициализация библиотеки Pygame.
        pg.init()
        # Создание экрана игры с использованием настроек
        self.screen = pg.display.set_mode(settings.WINDOWS)
        # Инициализация списка фигур
        self.figures = [[pg.Rect(x + settings.WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos]
                        for fig_pos in settings.FIGURES_POS]
        # Выбор случайной фигуры из списка фигур для текущей игры.
        self.index, self.fig = deepcopy(random.choice(tuple(enumerate(self.figures))))
        # Создание прямоугольника для отображения фигуры.
        self.figure_rect = pg.Rect(0, 0, settings.TILE - 2, settings.TILE - 2)
        # Выбор следующих трех случайных фигур для отображения в правой части экрана.
        self.index_1, self.fig_next_1 = deepcopy(random.choice(tuple(enumerate(self.figures))))
        self.index_2, self.fig_next_2 = deepcopy(random.choice(tuple(enumerate(self.figures))))
        self.index_3, self.fig_next_3 = deepcopy(random.choice(tuple(enumerate(self.figures))))
        # Установка цвета текущей фигуры и следующих фигур.
        self.color = settings.FIGURES_COLOR[self.index]
        self.color_next_1 = settings.FIGURES_COLOR[self.index_1]
        self.color_next_2 = settings.FIGURES_COLOR[self.index_2]
        self.color_next_3 = settings.FIGURES_COLOR[self.index_3]
        # Создание сетки для отображения игрового поля.
        self.grid = [pg.Rect(x * settings.TILE, y * settings.TILE, settings.TILE, settings.TILE)
                     for x in range(settings.WIDTH) for y in range(settings.HEIGTH)]
        # Инициализация переменных для управления фигурами и игровым процессом.
        self.dx, self.count, self.limit, self.speed, self.score = 0, 0, 2000, 60, 0
        self.rotate = False
        self.record = self.get_record()
        self.fig_old = None
        # Создание игрового поля.
        self.field = [[0 for _ in range(settings.GAME_WINDOWS[0])] for _ in range(settings.GAME_WINDOWS[1])]
        # Создание заголовков и счетчика очков.
        self.title = settings.FONT_TITLE.render('TETRIS', True, settings.CYAN)
        self.next_title = settings.FONT_MAIN.render('Next', True, settings.WHITE)
        self.score_title = settings.FONT_MAIN.render('Score: ', True, settings.WHITE)
        self.score_tir = {0: 0, 1: 100, 2: 200, 3: 400, 4: 1000}
        self.record_title = settings.FONT_MAIN.render('Record: ', True, settings.WHITE)

    def run(self):
        """
        Данный метод отображает игровое поле, текущую фигуру, следующие фигуры и сетку. Он также проверяет границы,
        вращает фигуру, останавливает ее при достижении нижней границы или касании другой фигуры, удаляет заполненные
        линии и обновляет счет.
        """
        # Отображение заголовков на экране.
        self.screen.blit(self.title, (400, 50))
        self.screen.blit(self.next_title, (400, 150))
        self.screen.blit(self.score_title, (400, 550))
        self.screen.blit(self.record_title, (400, 650))
        self.screen.blit(settings.FONT_MAIN.render(str(self.record), True, settings.GOLD), (520, 650))
        # Копирование текущей фигуры для проверки границ.
        self.fig_old = deepcopy(self.fig)
        # Перемещение фигуры по оси X.
        for i in range(4):
            self.fig[i].x += self.dx
            if not self.check_borders(i):
                self.fig = deepcopy(self.fig_old)
                break
        self.stopping_shape()
        self.rotation()
        self.deleting_line()
        # Отображение сетки игрового поля.
        [pg.draw.rect(self.screen, settings.GRID, i, 1) for i in self.grid]
        self.draw_figure(self.fig, settings.TILE, 0, 0, self.color)
        self.draw_figure(self.fig_next_1, settings.TILE_SUP, 380, 200, self.color_next_1)
        self.draw_figure(self.fig_next_2, settings.TILE_SUP, 380, 300, self.color_next_2)
        self.draw_figure(self.fig_next_3, settings.TILE_SUP, 380, 400, self.color_next_3)
        # Отображение заполненных ячеек на игровом поле.
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    self.figure_rect.x, self.figure_rect.y = x * settings.TILE, y * settings.TILE
                    pg.draw.rect(self.screen, col, self.figure_rect)

    def draw_figure(self, fig, tile, x, y, color):
        """
        Метод перебирает каждый прямоугольник в списке, вычисляет его позицию на экране и
        рисует его с заданным цветом.
        :param fig: список прямоугольников, представляющих фигуру
        :param tile: размер каждого квадрата
        :param x: координата отображения фигуры
        :param y: координата отображения фигуры
        :param color: цвет фигуры
        """
        for i in range(4):
            self.figure_rect.x = fig[i].x * tile + x
            self.figure_rect.y = fig[i].y * tile + y
            pg.draw.rect(self.screen, color, self.figure_rect)

    def deleting_line(self):
        """
        Данный метод отвечает за удаление заполненных линий на игровом поле. Он перебирает строки игрового поля снизу
        вверх. Если строка полностью заполнена, то она удаляется, а все строки выше сдвигаются вниз. При удалении
        строки увеличивается счетчик удаленных линий и скорость игры увеличивается. Кроме того,
        метод обновляет счет на основе количества удаленных линий.
        """
        line = settings.HEIGTH - 1
        lines = 0
        for row in range(settings.HEIGTH - 1, -1, -1):
            count = 0
            for i in range(settings.WIDTH):
                if self.field[row][i]:
                    count += 1
                self.field[line][i] = self.field[row][i]
            if count < settings.WIDTH:
                line -= 1
            else:
                lines += 1
                self.speed += 5
        self.score += self.score_tir[lines]
        self.screen.blit(settings.FONT_MAIN.render(str(self.score), True, settings.WHITE), (500, 550))

    def rotation(self):
        """
        Данный метод выполняет вращение текущей фигуры. Он использует алгоритм поворота фигуры относительно ее
        центра. Метод получает координаты центрального прямоугольника и создает копию текущей фигуры.
        Затем для каждого прямоугольника в списке, метод вычисляет новые координаты после поворота и проверяет их
        на границы игрового поля и пересечение с другими фигурами. Если проверка не проходит,
        фигура восстанавливается из копии.
        """
        center = self.fig[0]
        fig_old = deepcopy(self.fig)
        if self.rotate:
            for i in range(4):
                x = self.fig[i].y - center.y
                y = self.fig[i].x - center.x
                self.fig[i].x = center.x - x
                self.fig[i].y = center.y + y
                if not self.check_borders(i):
                    self.fig = deepcopy(fig_old)
                    break

    def stopping_shape(self):
        """
        Данный метод отвечает за остановку текущей фигуры при достижении нижней границы или при касании другой
        фигуры. Метод увеличивает счетчик на основе скорости игры. Когда счетчик превышает предельное значение,
        метод сдвигает текущую фигуру вниз и проверяет, достигла ли она нижней границы или коснулась другой фигуры.
        Если это произошло, метод закрепляет фигуру на игровом поле, обновляет следующие фигуры и их цвета,
        и сбрасывает предельное значение для следующей фигуры.
        """
        self.count += self.speed
        if self.count > self.limit:
            self.count = 0
            for i in range(4):
                self.fig[i].y += 1
                self.check_end()
                if not self.check_borders(i):
                    for j in range(4):
                        self.field[self.fig_old[j].y][self.fig_old[j].x] = self.color
                    self.index, self.fig = self.index_1, self.fig_next_1
                    self.index_1, self.fig_next_1 = self.index_2, self.fig_next_2
                    self.index_2, self.fig_next_2 = self.index_3, self.fig_next_3
                    self.index_3, self.fig_next_3 = deepcopy(random.choice(tuple(enumerate(self.figures))))
                    self.color = self.color_next_1
                    self.color_next_1 = self.color_next_2
                    self.color_next_2 = self.color_next_3
                    self.color_next_3 = settings.FIGURES_COLOR[self.index_3]
                    self.limit = 2000
                    break

    def check_end(self):
        """
        Данный метод проверяет, достигла ли текущая фигура верхней границы игрового поля. Если какой-либо
        прямоугольник текущей фигуры находится в верхней строке игрового поля, метод сбрасывает игровое поле,
        счетчик и предельное значение, чтобы начать новую игру.
        """
        for i in range(settings.WIDTH):
            if self.field[0][i]:
                self.set_record()
                self.field = [[0 for _ in range(settings.WIDTH)] for _ in range(settings.HEIGTH)]
                self.count, self.limit, self.score = 0, 2000, 0
                for i_rect in self.grid:
                    pg.draw.rect(self.screen, settings.BACKGROUND, i_rect)
                    pg.display.flip()

    @staticmethod
    def get_record():
        """
        Данный метод получает информацию о рекорде с файла.
        """
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self):
        """
        Данный метод записывает информацию о рекорде в файл и запоминает этот рекорд.
        """
        rec = max(int(self.record), self.score)
        with open('record', 'w') as f:
            f.write(str(rec))
        self.record = rec

    def check_borders(self, i):
        """
        Данный метод проверяет границы для текущей фигуры. Он проверяет, находится ли каждый прямоугольник текущей
        фигуры в пределах игрового поля или касается ли он других фигур на игровом поле. Если хотя бы одно из этих
        условий не выполняется для любого прямоугольника, метод возвращает False, указывая на неправильное положение
        фигуры. В противном случае метод возвращает True, указывая на правильное положение фигуры.
        """
        if self.fig[i].x < 0 or self.fig[i].x > settings.WIDTH - 1 or self.fig[i].y > settings.HEIGTH - 1 or \
                self.field[self.fig[i].y][self.fig[i].x]:
            return False
        return True
