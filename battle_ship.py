# -*- coding: UTF-8 -*-

__author__ = 'Roman Evdokimov'

'''
Реализация игры "Морской бой" в графическом интерфейсе при помощи модуля pygame
логика игры будет взята из ранее написанного для командной строки
'''

import pygame
import Battleship_logic as bs
import random
pygame.init() # инициализация пакета, не знаю нужна она или нет

done = True # значение, при котором игра будет выполняться, пока не изменится на False

LEFT = 1 # значение для определения какая кнопка мыши нажата

# размеры игрового поля
height_field = 500
width_field = 500

screen = pygame.display.set_mode([height_field, width_field]) # отображение игрового поля
pygame.display.set_caption("Battle Ship v. 0.1") # заголовок окна
clock = pygame.time.Clock() # модуль для работы со временем в pygame

# цвета, которые будут использоваться в игре
blue = [0, 0, 255]
black = [0, 0, 0]
green = [0, 255, 0]
red = [255, 0, 0]
grey = [125, 125, 125]

screen.fill(blue) # создание заднего фона

# размеры квадрата
height_circle = height_field//10
width_circle = width_field//10

# толщина линии
line_thickness = 4

# количество попыток
val = 50

# функция создания линий на игровом поле
def line_in_field(horizontal_line, vertical_line, color_line, x_circle, y_circle, line_thickness):
    for x_offset in range(x_circle, vertical_line, x_circle): # горизонтальные линии
        pygame.draw.line(screen, color_line, [0, x_offset], [horizontal_line, x_offset], line_thickness)

    for y_offset in range(y_circle, horizontal_line, y_circle): # вертикальные линии
        pygame.draw.line(screen, color_line, [y_offset, 0], [y_offset, vertical_line], line_thickness)



line_in_field(height_field, # вызываем один раз да бы не рисовать их постоянно
              width_field,
              black,
              height_circle,
              width_circle,
              line_thickness)

bs.start_game(val)

total = 0

while done: # цикл выполнения игры

    for event in pygame.event.get(): # что сделал пользователь
        if event.type == pygame.QUIT: # если нажал закрыть окно
            done=False # больше не выполнять цикл (но в последний раз все равно выполнится весь код может нужно выполнить continue?)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: # реакция на нажатие левой кнопоки мыши
            pos = pygame.mouse.get_pos() # координаты курсора
            val -= 1
            # получение значений,
            pos_x = pos[0]- pos[0]%height_circle
            pos_y = pos[1]- pos[1]%width_circle

            # индексы для отрисовки кораблей созданных ПК
            pos_x_index_for_field_game = int(pos_x/height_circle)
            pos_y_index_for_field_game = int(pos_y/width_circle)

            p = bs.game(pos_y_index_for_field_game, pos_x_index_for_field_game, val, total) # cписок координат вокруг подбитого корабля

            if p:
                total += 1
                for x in p: # производим выстрел по координатам
                    pygame.draw.rect(screen, green,
                                 [x[1]*height_circle+line_thickness,
                                  x[0]*width_circle+line_thickness,
                                  width_circle-line_thickness,
                                  height_circle-line_thickness])



            if bs.field_game[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'H':
                pygame.draw.rect(screen, red,
                             [pos_x+line_thickness,
                              pos_y+line_thickness,
                              width_circle-line_thickness,
                              height_circle-line_thickness])

            if bs.field_game[pos_y_index_for_field_game][pos_x_index_for_field_game] == '0' or \
               bs.field_game[pos_y_index_for_field_game][pos_x_index_for_field_game] == '*' \
                    and list(screen.get_at(pos))[:3] != green:
                pygame.draw.rect(screen, grey,
                             [pos_x+line_thickness,
                              pos_y+line_thickness,
                              width_circle-line_thickness,
                              height_circle-line_thickness])

    if val <= 0:
        screen.fill(blue)
        font = pygame.font.Font(None, 25)
        text = font.render("GAME OVER",True,[random.randint(0,255) for _ in range(3)])
        screen.blit(text, [200, 250])

    if total == 10:
        screen.fill(blue)
        font = pygame.font.Font(None, 25)
        text = font.render("WINNER",True,[random.randint(0,255) for _ in range(3)])
        screen.blit(text, [200, 250])


    pygame.display.flip() # обновление всей облати дисплея
    clock.tick(10) # частота обновлений игрового поля или выполнения цикла в секунду

pygame.quit()