# -*- coding: utf-8 -*-

"""
Игра 'Морской бой'. Модель игры - компьютер-игрок с полем 10 на 10 и 
четырьмя однопалубными кораблями.
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
	num = 1
	print("   1 2 3 4 5 6 7 8 9 10")
	for column in field:
		if num < 10:
			print(num, end ="  ")
		else:
			print(num, end =" ")
		print (' '.join(column))
		num += 1

# функции определения координат корабля случайным образом
def coordinate_string(field):
	return randint(0, (len(field) - 1))

def coordinate_column(field):
	return randint(0, (len(field[0]) - 1))

# координаты корабля (с учетом того, что отсчет начинается с 0 в списках)	
c_string = coordinate_string(field) 
c_column = coordinate_column(field)

def coordinate():
	lst_coordinat = []
	value = 0
	while value < 4:
		c_string = coordinate_string(field) 
		c_column = coordinate_column(field)
		if (c_string, c_column) in lst_coordinat:
			continue
		else:
			lst_coordinat.append((c_string, c_column))
			value += 1
	return lst_coordinat
#print(c_string + 1, c_column + 1) # вывод реальных координат (для отладки)
#field[c_string][c_column] = 'X'    # обозначение корабля на "поле" боя (для отладки)

# функция обозначения выстрела игрока
def shot(x, y):
	if field[x - 1][y - 1] == "X":
		print ("Ты стреляешь в одно и то же место! Будь внимателен!")
	else:
		field[x - 1][y - 1] = "X"
		print_field(field)	

# функция обозначения подбитого корабля		
def shot_ship(x, y):
	if field[x - 1][y - 1] == "H":
		print ("Этот корабль уже был потоплен! Будь внимателен!")
	else:
		print("Поздравляем! Вам удалось потопить корабль!")
		field[x - 1][y - 1] = "H"
		print_field(field)

lst_c = coordinate() # Список, содержащий координаты кораблей
#print(lst_c) # вывод координат кораблей
print("Игра началась!")
print("Вам дается 50 попыток, чтобы найти корабль.")
print("Введите предпологаемые вами координаты корабля!")

choice_ship_shot = 0 # начальное значение подбитых кораблей	
for value in range(1, 51):
    # координаты вводимые пользователем с проверкой ввода типа данных
	if choice_ship_shot == 4:
		print("Вы потопили все корабли!!! Поздравляем с победой!!!")
		break
	try:
		player_string = int(input("Пожалуйста, введите номер строки:"))
		player_column = int(input("Пожалуйста, введите номер столбца:"))
	except ValueError:
		print("Вы должны вводить цифры!!!")
		continue
	if value < 50: # количество попыток
		if (player_string, player_column) in lst_c and choice_ship_shot < 4:
			shot_ship(player_string, player_column)
			choice_ship_shot += 1
			if choice_ship_shot <= 3:
				print("У вас осталось - %s попыток" % (50 - value))
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
			print("Корабли находились на координатах:")
			for s, c in lst_c:
				print (s, c)
		except IndexError:
			print("Нет таких координат! Вы проиграли, исчерпав свои попытки...")
		break
