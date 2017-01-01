# -*- coding: UTF-8 -*-

__author__ = 'Roman Evdokimov'

'''
Реализация игры "Морской бой" в графическом интерфейсе при помощи библиотеки pygame
логика игры будет взята из ранее написанного для командной строки
'''

import pygame
import Battleship_logic as bs
import random
pygame.init() # инициализация пакета, не знаю нужна она или нет

done = True # значение, при котором игра будет выполняться, пока не изменится на False

LEFT = 1 # значение для определения какая кнопка мыши нажата

width = 750
# размеры квадрата
width_circle = height_circle = int((width*0.7)//10)

# размеры игрового поля
height_field = width_field = height_circle*10

# толщина линии
line_thickness = 4

screen = pygame.display.set_mode([height_field, width]) # отображение игрового поля
pygame.display.set_caption("Battle Ship v. 0.2") # заголовок окна
clock = pygame.time.Clock() # модуль для работы со временем в pygame

# цвета, которые будут использоваться в игре
blue = [0, 0, 255]
black = [0, 0, 0]
green = [0, 255, 0]
red = [255, 0, 0]
grey = [125, 125, 125]
white = [255, 255, 255]

screen.fill(blue) # создание заднего фона

# установка цвета для прямоугольника по заданным координатам и длинам сторон
def colorChangeRect(color, pos_x_rect, pos_y_rect, width_rect, height_rect):
    pygame.draw.rect(screen, color,
                             [pos_x_rect,
                              pos_y_rect,
                              width_rect,
                              height_rect])

# поле для отображения текста хода игры
colorChangeRect(white, 0, width-(width-width_field), height_field, width-width_field)

# количество попыток
attempts = 51

# количество потопленных кораблей
number_of_sunken_ships = 0

# создание линий на игровом поле
def line_in_field(horizontal_line, vertical_line, color_line, x_circle, y_circle, line_thickness):
    for x_offset in range(0, vertical_line+x_circle, x_circle): # горизонтальные линии
        pygame.draw.line(screen, color_line, [0, x_offset], [horizontal_line, x_offset], line_thickness)

    for y_offset in range(0, horizontal_line+y_circle, y_circle): # вертикальные линии
        pygame.draw.line(screen, color_line, [y_offset, 0], [y_offset, vertical_line], line_thickness)



line_in_field(height_field, # вызываем один раз да бы не рисовать их постоянно
              width_field,
              black,
              height_circle,
              width_circle,
              line_thickness)

# информация о начале игры и о количестве попыток

font = pygame.font.Font(None, int(width*0.033))
number_of_displayed_rows = 1
for txt in bs.start_game(attempts):
    text = font.render(txt, True, black)
    screen.blit(text, [int(width*0.033), (width-(width-width_field))+int(width*0.033*number_of_displayed_rows)])
    number_of_displayed_rows += 1


# функция вывода сообщения о победе или поражении
def end_game(txt):
    colorChangeRect(blue, 0, 0, height_field, width_field)
    font = pygame.font.Font(None, 25)
    text = font.render(txt,True,[random.randint(0,255) for _ in range(3)])
    screen.blit(text, [200, 250])

# отображение хода игры (сообщений) в окне
def displayString(text_display):
    colorChangeRect(white, 0, width-(width-width_field), height_field, width-width_field)
    font = pygame.font.SysFont(None, int(width*0.033))
    number_of_displayed_rows = 1
    for txt in text_display:
        text = font.render(txt, True, black)
        screen.blit(text, [int(width*0.033), (width-(width-width_field))+int(width*0.033*number_of_displayed_rows)])
        number_of_displayed_rows += 1

while done: # цикл выполнения игры

    for event in pygame.event.get(): # что сделал пользователь
        if event.type == pygame.QUIT: # если нажал закрыть окно
            done=False # больше не выполнять цикл (но в последний раз все равно выполнится весь код может нужно выполнить continue?)
        if event.type == pygame.MOUSEBUTTONDOWN and \
           event.button == LEFT and attempts > 1 and \
           number_of_sunken_ships < 10: # реакция на нажатие левой кнопоки мыши

            pos = pygame.mouse.get_pos() # координаты курсора

            # получение значений,
            pos_x = pos[0]- pos[0]%height_circle
            pos_y = pos[1]- pos[1]%width_circle

            # индексы для отрисовки кораблей созданных ПК
            pos_x_index_for_field_game = int(pos_x/height_circle)
            pos_y_index_for_field_game = int(pos_y/width_circle)

            if height_field < pos[0] or width_field < pos[1]: # проверяем где кликнули в поле или нет
                break

            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == '0':
                attempts -= 1

            p = bs.game(pos_y_index_for_field_game, pos_x_index_for_field_game, attempts, number_of_sunken_ships) # cписок координат вокруг подбитого корабля
            #print(p)

            if p[1]: #len(p) > 1:
                number_of_sunken_ships += 1
                for x in p[1]: # обрисовка уничтоженного корабля

                    colorChangeRect(green,
                                    x[1]*height_circle+line_thickness,
                                    x[0]*width_circle+line_thickness,
                                    width_circle-line_thickness,
                                    height_circle-line_thickness
                                    )

                displayString(p[0])

            else:
                displayString(p[0])

            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'H' or \
                bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'I':

                colorChangeRect(red,
                                pos_x+line_thickness,
                                pos_y+line_thickness,
                                width_circle-line_thickness,
                                height_circle-line_thickness
                                )

            if bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == '0' or \
                       bs.field_player[pos_y_index_for_field_game][pos_x_index_for_field_game] == 'X':

                colorChangeRect(grey,
                                pos_x+line_thickness,
                                pos_y+line_thickness,
                                width_circle-line_thickness,
                                height_circle-line_thickness
                                )

    if attempts <= 1:
        end_game("GAME OVER")

    if number_of_sunken_ships == 10:
        end_game("WINNER")

    pygame.display.flip() # обновление всей облати дисплея
    clock.tick(10) # частота обновлений игрового поля или выполнения цикла в секунду

pygame.quit()
