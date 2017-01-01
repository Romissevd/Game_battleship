# -*- coding: utf-8 -*-

"""
Игра 'Морской бой'. Модель игры - компьютер-игрок с полем 10 на 10.
Реализованная на Python 3.
Правила игры:
1. Корабли располагаются только по-вертикали или по-горизонтали;
2. Корабли не могут касаться друг друга.
"""

import random  # модуль генератора случайных чисел
import pygame

# создание игрового поля 10 на 10
field_game = [['0' for row in range(1, 11)] for col in range(1, 11)]
field_player = [['0' for row in range(1, 11)] for col in range(1, 11)]


# функия отображения поля
def print_field(field):
    num = 1
    print("   1 2 3 4 5 6 7 8 9 10")
    for column in field:
        if num < 10:
            print(num, end="  ")
        else:
            print(num, end=" ")
        print(' '.join(column))
        num += 1


lst_sp_coord = []


class Ship():
    def __init__(self, deck):
        self.deck = deck
        self.shot_deck = 1
        self.ship_sost = []

    def coordinate(self, field):
        self.sp_coord = []

        while True:
            self.value = 1
            self.error = 1
            self.string = random.randint(0, (len(field) - 1))
            self.column = random.randint(0, (len(field[0]) - 1))
            self.disposition = random.choice(["vertical+", "vertical-", "horizontal+", "horizontal-"])
            self.sp_coord.append((self.string, self.column))
            while self.value < self.deck:
                if self.disposition == "vertical+":
                    if self.string + self.value > 9:
                        self.sp_coord.append((self.string - self.error, self.column))
                        self.error = self.error + 1
                    else:
                        self.sp_coord.append((self.string + self.value, self.column))
                    self.value = self.value + 1
                elif self.disposition == "horizontal+":
                    if self.column + self.value > 9:
                        self.sp_coord.append((self.string, self.column - self.error))
                        self.error = self.error + 1
                    else:
                        self.sp_coord.append((self.string, self.column + self.value))
                    self.value = self.value + 1
                elif self.disposition == "vertical-":
                    if self.string - self.value < 0:
                        self.sp_coord.append((self.string + self.error, self.column))
                        self.error = self.error + 1
                    else:
                        self.sp_coord.append((self.string - self.value, self.column))
                    self.value = self.value + 1
                elif self.disposition == "horizontal-":
                    if self.column - self.value < 0:
                        self.sp_coord.append((self.string, self.column + self.error))
                        self.error = self.error + 1
                    else:
                        self.sp_coord.append((self.string, self.column - self.value))
                    self.value = self.value + 1
                else:
                    print("Что-то пошло не так.")

            for x, y in self.sp_coord:
                if field[x][y] == "H" or field[x][y] == "*":
                    self.sp_coord = []

            if len(self.sp_coord) == 0:
                continue

            for x, y in self.sp_coord:
                field[x][y] = "H"

            for x, y in self.sp_coord:
                for m, n in [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1),
                             (x, y - 1), (x + 1, y - 1)]:
                    if (-1) < m < 10 and (-1) < n < 10 and field[m][n] != "H":
                        field[m][n] = "*"

            break
        return self.sp_coord

    def shot(self, x, y):
        if (x, y) in self.sp_coord and self.shot_deck == self.deck and (x, y) not in self.ship_sost:
            self.ship_sost.append((x, y))
            return ["Уничтожил!", self.ship_sost]
        elif (x, y) in self.sp_coord:
            if (x, y) not in self.ship_sost:
                self.shot_deck += 1
            self.ship_sost.append((x, y))
            return ["Подбил!"]
        else:
            return ["Мимо!"]

ships = []
def f(x):
    ships.append(Ship(x))

z = 4
for x in range(z):
    for y in range(x+1):
        f(z)
    z -=1


# ship_4_1 = Ship(4)
# ship_3_1 = Ship(3)
# ship_3_2 = Ship(3)
# ship_2_1 = Ship(2)
# ship_2_2 = Ship(2)
# ship_2_3 = Ship(2)
# ship_1_1 = Ship(1)
# ship_1_2 = Ship(1)
# ship_1_3 = Ship(1)
# ship_1_4 = Ship(1)
#
# ships = [ship_4_1, ship_3_1, ship_3_2, ship_2_1, ship_2_2,
#          ship_2_3, ship_1_1, ship_1_2, ship_1_3, ship_1_4]

for ship in ships:
    ship.coordinate(field_game)

def start_game(value):
    st = []
    st.append('Игра началась!')
    st.append('Вам дается %d попыток, чтобы найти корабли.' % (value-1))
    return st

def game(pl_str, pl_col, value, total_shot_ship):

    text = []

    if total_shot_ship == 10:
        print("Поздравляем вы выиграли!")
        #break
        # координаты вводимые пользователем с проверкой ввода типа данных
    try:
        player_string = pl_str + 1
        player_column = pl_col + 1

    except ValueError:
        print("Вы должны вводить цифры!!!")
        #continue

    if not (0 < player_string < 11) or not (0 < player_column < 11):
        print("Эй, таких координат нет!!!")
        print("У вас осталось - %s попыток" % (value - 1))
        #continue
    elif value > 1:  # количество попыток
        text.append("У вас осталось - %d попыток" % (value-1))
        print(text)
        lst_sost = []
        coord_for_ship_in_visual_field = []
        for shot_ship in ships:
            sost = shot_ship.shot((player_string - 1), (player_column - 1))
            lst_sost.append(sost)
        for l in lst_sost:

            if len(l) > 1:
                for (x, y) in l[1]:
                    field_player[x][y] = "I"
                print("Уничтожил!!!")
                text.append("Уничтожил!!!")
                for x, y in l[1]:

                    for m, n in [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1),
                                 (x, y - 1), (x + 1, y - 1)]:
                        if (-1) < m < 10 and (-1) < n < 10 and field_player[m][n] != "I":
                            field_player[m][n] = "*"
                            coord_for_ship_in_visual_field.append((m, n))
                total_shot_ship += 1
                return [text, coord_for_ship_in_visual_field]
        else:
            if field_player[(player_string - 1)][(player_column - 1)] == "I" or \
                            field_player[(player_string - 1)][(player_column - 1)] == "H":
                text.append("Корабль уже подбит. Будь внимателен!!!")
            elif ["Подбил!"] in lst_sost:
                field_player[(player_string - 1)][(player_column - 1)] = "H"
                print("Подбил!!!")
                text.append("Подбил!!!")
            else:
                if field_player[(player_string - 1)][(player_column - 1)] == "0":
                    field_player[(player_string - 1)][(player_column - 1)] = "X"
                elif field_player[(player_string - 1)][(player_column - 1)] == "*":
                    text.append("Сюда можно не стрелять. Тут кораблей не будет!")
                elif field_player[(player_string - 1)][(player_column - 1)] == "X":
                    text.append("Сюда уже стрелял!!!")
                    value += 1
                #print("Мимо!!!")
                text.append("Мимо!!!")
        #print_field(field_player)
        return [text, coord_for_ship_in_visual_field]
    else:
        text.append("К сожалению вы проиграли!!!")
        print("К сожалению вы проиграли!!!")
        print("Расположение кораблей было такое:")
        print_field(field_game)
        return [text, []]

