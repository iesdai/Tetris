import pygame as pg

import settings


class Menu:
    def __init__(self):
        """
        Инициализация класса Menu.

        Создает экран для отрисовки стартового меню.
        """
        pg.init()
        self.screen = pg.display.set_mode(settings.WINDOWS)

    def draw_start_menu(self):
        """
        Данный метод отвечает за отрисовку элементов стартового меню.
        """
        # Очищаем экран и устанавливаем фоновый цвет
        self.screen.fill(settings.BACKGROUND)
        # Отрисовываем заголовок
        title_text = 'Tetris Game'
        title = settings.FONT_MAIN.render(title_text, True, settings.CYAN)
        title_x = settings.GAME_WINDOWS[0] // 2 - title.get_width() // 2
        title_y = settings.GAME_WINDOWS[1] // 2 - title.get_height() // 2
        self.screen.blit(title, (title_x, title_y))

        # Отрисовываем инструкции для начала игры и выхода
        start_text = 'Чтобы начать нажмите пробел'
        start = settings.FONT_MAIN.render(start_text, True, settings.WHITE)
        start_x = settings.GAME_WINDOWS[0] // 2 - start.get_width() // 2
        start_y = settings.GAME_WINDOWS[1] // 2 + start.get_height() // 2
        self.screen.blit(start, (start_x, start_y))
        end_text = 'Чтобы выйти из игры нажмите esc(escape)'
        end = settings.FONT_MAIN.render(end_text, True, settings.RED)
        self.screen.blit(end, (30, 600))

        # Обновляем экран
        pg.display.update()
