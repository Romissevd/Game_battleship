# -*- coding: UTF-8 -*-

import random
import pygame
import Battleship_logic as bs

'''
Реализация игры "Морской бой" в графическом интерфейсе при помощи библиотеки pygame
логика игры будет взята из ранее написанного кода для командной строки
'''

__author__ = 'Roman Evdokimov'
pygame.init()  # инициализация пакета
DONE = True  # значение, при котором игра будет выполняться, пока не изменится на False
LEFT = 1  # значение для определения какая кнопка мыши нажата
WIDTH = 750
LINE_THICKNESS = 4  # толщина линии
# RGB кодирорвка цвета, используемых в игре
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
GREY = [125, 125, 125]
WHITE = [255, 255, 255]
attempts = 51  # количество попыток
number_of_sunken_ships = 0  # количество потопленных кораблей

icon = pygame.image.load('images/icon.png')  # загрузка изображения иконки
icon.set_colorkey(WHITE)  # сделать задний фон иконки прозрачным
pygame.display.set_icon(icon)  # установить иконку
pygame.display.set_caption("Battle Ship v. 0.3")  # заголовок окна
width_circle = height_circle = int((WIDTH*0.7)//10)  # размеры квадрата
height_field = width_field = height_circle*10  # размеры игрового поля
screen = pygame.display.set_mode([height_field, WIDTH])  # отображение игрового поля
clock = pygame.time.Clock()  # модуль для работы со временем в pygame


class Block(pygame.sprite.Sprite):
    """Этот класс представляет блок. Он наследуется от класса "Sprite" из Pygame"""

    def __init__(self, image_name, width, height, x_rect, y_rect):
        super().__init__()
        self.image_path = 'images/{}'.format(image_name)
        self.image = pygame.image.load(self.image_path).convert()  # загрузить изображение и трансформировать его
        self.image = pygame.transform.scale(self.image, [width, height])  # подогнать изображение под размер квадрата
        self.image.set_colorkey(BLACK)  # задний ченый фон сделать прозрачным
        self.rect = self.image.get_rect()  # привязать изображение к прямогульнику
        self.rect.x = x_rect
        self.rect.y = y_rect
        self.position = 0

    def update(self):
        if self.rect.y < self.position:
            self.rect.y += 1


class BlockLine(pygame.sprite.Sprite):

    def __init__(self, color, x_rect, y_rect, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()  # привязать изображение к прямогульнику
        self.rect.x = x_rect
        self.rect.y = y_rect

    def update(self):
        pass


block_list = pygame.sprite.Group()
block_field_list = pygame.sprite.Group()


def color_change_rect(color, pos_x_rect, pos_y_rect, width_rect, height_rect):
    """установка цвета для прямоугольника по заданным координатам и длинам сторон"""
    pygame.draw.rect(screen,
                     color,
                     [pos_x_rect, pos_y_rect, width_rect, height_rect])


def line_in_field(horizontal_line, vertical_line, color_line, x_circle, y_circle, thickness_line):
    """создание линий на игровом поле"""
    for x_offset in range(0, vertical_line+x_circle, x_circle):  # горизонтальные линии
        block_line = BlockLine(color_line, 0, x_offset, horizontal_line, thickness_line)
        block_list.add(block_line)
    for y_offset in range(0, horizontal_line+y_circle, y_circle):  # вертикальные линии
        block_line = BlockLine(color_line, y_offset, 0, thickness_line, horizontal_line)
        block_list.add(block_line)


def end_game(txt_message):
    """вывод сообщения по окончании игры"""
    color_change_rect(BLUE, 0, 0, height_field, width_field)
    font_style = pygame.font.Font(None, 25)
    message = font_style.render(txt_message, True, [random.randint(0, 255) for _ in range(3)])
    screen.blit(message, [200, 250])


def display_string(text_display):
    """Отображение хода игры (сообщений) в окне"""
    number_displayed_rows = 1
    color_change_rect(WHITE, 0, WIDTH-(WIDTH-width_field), height_field, WIDTH-width_field)
    font_style = pygame.font.SysFont(None, int(WIDTH*0.033))

    for line_message in text_display:
        text_message = font_style.render(line_message, True, BLACK)
        screen.blit(text_message, [int(WIDTH*0.033),
                    (WIDTH-(WIDTH-width_field))+int(WIDTH*0.033*number_displayed_rows)]
                    )
        number_displayed_rows += 1

# поле для отображения текста хода игры
color_change_rect(WHITE, 0, WIDTH-(WIDTH-width_field), height_field, WIDTH-width_field)
# Построение игрового поля
line_in_field(height_field, width_field, BLACK,
              height_circle, width_circle, LINE_THICKNESS
              )
# информация о начале игры и о количестве попыток
font_init = pygame.font.Font(None, int(WIDTH*0.033))
number_of_displayed_rows = 1
for txt in bs.start_game(attempts):
    text = font_init.render(txt, True, BLACK)
    screen.blit(text, [int(WIDTH*0.033), (WIDTH-(WIDTH-width_field))+int(WIDTH*0.033*number_of_displayed_rows)])
    number_of_displayed_rows += 1

block_field = Block('sea.jpg', width_field, height_field, 0, 0)
block_field_list.add(block_field)


while DONE:  # выполнение игры

    for event in pygame.event.get():  # что сделал пользователь

        if event.type == pygame.QUIT:  # если нажал закрыть окно
            DONE = False  # больше не выполнять цикл (но в последний раз все равно выполнится)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and \
           attempts > 1 and number_of_sunken_ships < 10:  # реакция на нажатие левой кнопоки мыши

            pos = pygame.mouse.get_pos()  # координаты курсора

            # координаты x y левого верхнего угла квадрата, по которому произведен выстрел
            pos_x = pos[0] - pos[0] % height_circle
            pos_y = pos[1] - pos[1] % width_circle

            # индексы для определения значения на игровом поле
            pos_x_index_for_field_game = int(pos_x/height_circle)
            pos_y_index_for_field_game = int(pos_y/width_circle)

            if height_field < pos[0] or width_field < pos[1]:  # где кликнули в поле или нет
                break
            # выстрел произведен по свободному полю
            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == '0':
                attempts -= 1

            # результат действий игрока
            result_game_player = bs.game(pos_y_index_for_field_game,
                                         pos_x_index_for_field_game,
                                         attempts,
                                         number_of_sunken_ships
                                         )

            if result_game_player[1]:  # корабль уничтожен
                number_of_sunken_ships += 1

                for x in result_game_player[1]:  # обрисовка уничтоженного корабля

                    block_lifebuoy = Block('lifebuoy.png',
                                           width_circle-LINE_THICKNESS,
                                           height_circle-LINE_THICKNESS,
                                           x[1]*height_circle+LINE_THICKNESS,
                                           x[0]*width_circle+LINE_THICKNESS
                                           )
                    block_list.add(block_lifebuoy)

                display_string(result_game_player[0])

            else:
                display_string(result_game_player[0])
            # корабль подбит
            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'H' or \
               bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'I':

                block_red_ship = Block('explosion.png',
                                       width_circle-LINE_THICKNESS,
                                       height_circle-LINE_THICKNESS,
                                       pos_x+LINE_THICKNESS,
                                       pos_y+LINE_THICKNESS
                                       )

                block_list.add(block_red_ship)
            # выстрел произведен мимо
            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == '0' or \
               bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'X':

                block = Block("bomb.png", width_circle, height_circle, pos_x, -width_circle)
                block.position = pos_y
                block_list.add(block)

    block_field_list.update()
    block_field_list.draw(screen)
    block_list.update()
    block_list.draw(screen)

    if attempts <= 1:
        end_game("GAME OVER")

    if number_of_sunken_ships == 10:
        display_string(bs.game(0, 0, attempts, 10)[0])
        end_game("WINNER")

    pygame.display.flip()  # обновление всей облати дисплея
    clock.tick(30)  # частота обновлений игрового поля или выполнения цикла в секунду

pygame.quit()
