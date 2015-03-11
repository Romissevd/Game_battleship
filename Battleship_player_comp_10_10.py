# -*- coding: utf-8 -*-

"""
Игра 'Морской бой'. Модель игры - компьютер-игрок с полем 10 на 10 и 
одним однопалубным короблем.
Реализованная на Python 3.
"""

from random import randint # модуль генератора случайных чисел

# создание игрового поля 10 на 10
field = []
for col in range(1, 11):
	row = []
	for x in range(1, 11):
		row.append('0')
	field.append(row)

# функия отображения поля
def print_field(field):
	for column in field:
		print (' '.join(column))

# функции определения координат корабля случайным образом
def coordinate_string(field):
	return randint(0, (len(field) - 1))

def coordinate_column(field):
	return randint(0, (len(field[0]) - 1))

# координаты корабля (с учетом того, что отсчет начинается с 0 в списках)	
c_string = coordinate_string(field) 
c_column = coordinate_column(field)

#print(c_string + 1, c_column + 1) # вывод реальных координат (для отладки)
#field[c_string][c_column] = 'X'    # обозначение корабля на "поле" боя (для отладки)

# функция обозначения выстрела игрока
def shot(x, y):
	if field[x - 1][y - 1] == "X":
		print ("Ты стреляешь в одно и то же место! Будь внимателен!")
	else:
		field[x - 1][y - 1] = "X"
		print_field(field)

print("Игра началась!")
print("Вам дается 50 попыток, чтобы найти корабль.")
print("Введите предпологаемые вами координаты корабля!")

for value in range(1, 51):
    # координаты вводимые пользователем с проверкой ввода типа данных
	try:
		player_string = int(input("Пожалуйста, введите номер строки:"))
		player_column = int(input("Пожалуйста, введите номер столбца:"))
	except ValueError:
		print("Вы должны вводить цифры!!!")
		continue
	if value < 50: # количество попыток
		if (player_string - 1) == c_string and (player_column - 1) == c_column:
			print("Поздравляем! Вам удалось потопить корабль!")
			break
		elif player_column not in range(1, (len(field) + 1)) or player_string not in range(1, (len(field[0]) + 1)):
			print("Эй, таких координат нет!!!")
			print("У вас осталось - %s попыток" % (50 - value))
		else:
			shot(player_string, player_column)
			print("У вас осталось - %s попыток" % (50 - value))
	else:
		try:
			shot(player_string, player_column)
			print("Вы проиграли, исчерпав свои попытки...")
			print("Корабль находился на координатах: %s : %s" %(c_string + 1, c_column + 1))
		except IndexError:
			print("Нет таких координат! Вы проиграли, исчерпав свои попытки...")
		break
