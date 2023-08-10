import sys

import pygame as pg

import settings
import menu
import tetris
from enum import Enum


# Определение перечисления для состояний игры
class GameState(Enum):
    START_MENU = 1
    GAME = 2


class Game:
    def __init__(self):
        # Инициализация библиотеки Pygame.
        pg.init()
        # Создание экрана для игры согласно настройкам
        self.screen = pg.display.set_mode(settings.WINDOWS)
        # Установка заголовка окна игры.
        pg.display.set_caption('Tetris game')
        # Создание объекта часов для контроля FPS (кадры в секунду).
        self.clock = pg.time.Clock()
        # Инициализация состояния игры "start_menu" (меню начала игры).
        self.game_state = GameState.START_MENU
        # Создание объектов для меню и игры.
        self.menu = menu.Menu()
        self.tetris = tetris.Tetris()

    def run(self):
        """
        Данный метод является основным циклом игры, который выполняется в бесконечном цикле. Он обновляет экран,
        проверяет состояние игры (game_state) и вызывает соответствующие методы для отображения меню или запуска
        игры.
        """
        while True:
            self.handle_events()
            self.update_screen()
            self.tetris.rotate = False
            self.tetris.dx = 0
            self.clock.tick(settings.FPS)

    def handle_events(self):
        """
        Данный метод  отвечает за обработку событий нажатия клавиш и соответствующих действий в игре. Он проверяет
        нажатие клавиши ESC или событие закрытия окна, чтобы завершить игру. Также он реагирует на нажатия клавиш
        LEFT, RIGHT, DOWN и UP, чтобы управлять перемещением и вращением фигур в игре.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.tetris.dx = -1
                elif event.key == pg.K_RIGHT:
                    self.tetris.dx = 1
                elif event.key == pg.K_DOWN:
                    self.tetris.limit = 100
                elif event.key == pg.K_UP:
                    self.tetris.rotate = True

    def update_screen(self):
        """
        Данный метод обновляет экран, в соответствии с состоянием игры.
        """
        self.screen.fill(settings.BACKGROUND)
        if self.game_state == GameState.GAME:
            self.tetris.run()
        elif self.game_state == GameState.START_MENU:
            self.menu.draw_start_menu()

            if pg.key.get_pressed()[pg.K_SPACE]:
                self.game_state = GameState.GAME

        pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
