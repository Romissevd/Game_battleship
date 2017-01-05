# -*- coding: utf-8 -*-

import random
import copy

"""
Игра 'Морской бой'. Модель игры - компьютер-игрок с полем 10 на 10.
Реализованная на Python 3.
Правила игры:
1. Корабли располагаются только по-вертикали или по-горизонтали;
2. Корабли не могут касаться друг друга.
"""

field_game = [['0' for row in range(1, 11)] for col in range(1, 11)]  # создание игрового поля 10 на 10
field_player = copy.deepcopy(field_game)  # полная копия игрового поля
lst_sp_coord = []
SHIPS = []

def print_field(field):
    """функия отображения поля"""
    num = 1
    print("   1 2 3 4 5 6 7 8 9 10")

    for column in field:
        if num < 10:
            print(num, end="  ")
        else:
            print(num, end=" ")
        print(' '.join(column))
        num += 1


class Ship():

    def __init__(self, deck):

        self.deck = deck
        self.shot_deck = 1
        self.ship_sost = []

    def coordinate(self, field):
        """создание кораблей на игровом поле"""
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
                    if self.string + self.value > (len(field[0]) - 1):
                        self.sp_coord.append((self.string - self.error, self.column))
                        self.error += 1
                    else:
                        self.sp_coord.append((self.string + self.value, self.column))

                elif self.disposition == "horizontal+":
                    if self.column + self.value > (len(field) - 1):
                        self.sp_coord.append((self.string, self.column - self.error))
                        self.error += 1
                    else:
                        self.sp_coord.append((self.string, self.column + self.value))

                elif self.disposition == "vertical-":
                    if self.string - self.value < 0:
                        self.sp_coord.append((self.string + self.error, self.column))
                        self.error += 1
                    else:
                        self.sp_coord.append((self.string - self.value, self.column))

                elif self.disposition == "horizontal-":
                    if self.column - self.value < 0:
                        self.sp_coord.append((self.string, self.column + self.error))
                        self.error += 1
                    else:
                        self.sp_coord.append((self.string, self.column - self.value))

                else:
                    raise RuntimeError("Failed to build ships")

                self.value += 1

            for coord_x, coord_y in self.sp_coord:
                if field[coord_x][coord_y] == "H" or field[coord_x][coord_y] == "*":
                    self.sp_coord = []

            if not self.sp_coord:
                continue

            for x, y in self.sp_coord:
                field[x][y] = "H"

            for x, y in self.sp_coord:
                for m, n in [(x - 1, y + 1), (x, y + 1),
                             (x + 1, y + 1), (x - 1, y),
                             (x + 1, y), (x - 1, y - 1),
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


def make_ships(deck):
    """Создание кораблей"""
    SHIPS.append(Ship(deck))

# порядок создания кораблей и их количество, сперва созается один четырехпалубный, затем 2 трехпалубных и т.д.
number_of_decks = 4
for x in range(number_of_decks):
    for y in range(x+1):
        make_ships(number_of_decks)
    number_of_decks -= 1

for ship in SHIPS:
    ship.coordinate(field_game)


def start_game(value):
    """информация о начале игры"""
    start_message = []
    start_message.append('Игра началась!')
    start_message.append('Вам дается %d попыток, чтобы найти корабли.' % (value-1))
    return start_message


def field_around_destroyed_ship(coordinat):
    """координаты вогруг уничтоженного корабля"""
    result_coordinat_around_destroyed_ship = []
    for x, y in coordinat:
        for m, n in [(x - 1, y + 1), (x, y + 1),
                     (x + 1, y + 1), (x - 1, y),
                     (x + 1, y), (x - 1, y - 1),
                     (x, y - 1), (x + 1, y - 1)]:

            if (-1) < m < len(field_player) and (-1) < n < len(field_player[0]) and field_player[m][n] != "I":
                field_player[m][n] = "*"
                result_coordinat_around_destroyed_ship.append((m, n))

    return result_coordinat_around_destroyed_ship


def game(pl_str, pl_col, value, total_shot_ship):
    """Ход игрового процесса"""
    text_message = []
    player_string = pl_str + 1
    player_column = pl_col + 1

    if total_shot_ship == 10:
        text_message.append("Поздравляем вы выиграли!")
        return [text_message, []]

    if value > 1:
        text_message.append("У вас осталось - %d попыток" % (value-1))
        lst_sost = []

        for shot_ship in SHIPS:
            sost = shot_ship.shot((player_string - 1), (player_column - 1))
            lst_sost.append(sost)

        for l in lst_sost:
            if len(l) > 1:
                for (coord_hit_ship_x, coord_hit_ship_y) in l[1]:
                    field_player[coord_hit_ship_x][coord_hit_ship_y] = "I"
                text_message.append(l[0])
                total_shot_ship += 1
                return [text_message, field_around_destroyed_ship(l[1])]
        else:
            if field_player[(player_string - 1)][(player_column - 1)] == "I" or \
                            field_player[(player_string - 1)][(player_column - 1)] == "H":
                text_message.append("Корабль уже подбит. Будь внимателен!!!")
            elif ["Подбил!"] in lst_sost:
                field_player[(player_string - 1)][(player_column - 1)] = "H"
                text_message.append("Подбил!!!")
            else:
                if field_player[(player_string - 1)][(player_column - 1)] == "0":
                    field_player[(player_string - 1)][(player_column - 1)] = "X"
                elif field_player[(player_string - 1)][(player_column - 1)] == "*":
                    text_message.append("Сюда можно не стрелять. Тут кораблей не будет!")
                elif field_player[(player_string - 1)][(player_column - 1)] == "X":
                    text_message.append("Сюда уже стрелял!!!")
                text_message.append("Мимо!!!")

        return [text_message, []]
    else:
        text_message.append("К сожалению вы проиграли!!!")
        return [text_message, []]
