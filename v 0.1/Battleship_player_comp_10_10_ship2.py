# -*- coding: utf-8 -*-

"""
Игра 'Морской бой'. Модель игры - компьютер-игрок с полем 10 на 10 и 
одним двупалобным короблем.
Реализованная на Python 3.
"""

import random # модуль генератора случайных чисел

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
	return random.randint(0, (len(field) - 1))

def coordinate_column(field):
	return random.randint(0, (len(field[0]) - 1))

# координаты корабля (с учетом того, что отсчет начинается с 0 в списках)	
c_string = coordinate_string(field) 
c_column = coordinate_column(field)

# функция построения двухпалубного корабля
def coordinate_ship2(x, y):
	coordinate_ship_2 = []
	coordinate_ship_2.append((x, y))
	disposition = random.choice(["vertical", "horizontal"])
	dislocation = random.choice(["plus", "minus"])
	if disposition == "vertical":
		if dislocation == "plus":
			coordinate_deck_2_x = x
			coordinate_deck_2_y = y + 1
			if coordinate_deck_2_y > 10:
				coordinate_deck_2_y = y - 1
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
			else:
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
		else:
			coordinate_deck_2_x = x
			coordinate_deck_2_y = y - 1
			if coordinate_deck_2_y < 0:
				coordinate_deck_2_y = y + 1
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
			else:
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
	else:
		if dislocation == "plus":
			coordinate_deck_2_x = x + 1
			coordinate_deck_2_y = y
			if coordinate_deck_2_x > 10:
				coordinate_deck_2_x = x - 1
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
			else:
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
		else:
			coordinate_deck_2_x = x - 1
			coordinate_deck_2_y = y
			if coordinate_deck_2_x < 0:
				coordinate_deck_2_x = x + 1
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
			else:
				coordinate_ship_2.append((coordinate_deck_2_x, coordinate_deck_2_y))
	return coordinate_ship_2

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
def shot_ship(x, y, z):
	if field[x - 1][y - 1] == "H":
		print ("Будь внимателен! Ты сюда уже стрелял!")
		return ("подбить", z)
	else:
		field[x - 1][y - 1] = "H"
		print_field(field)
		if z < 1:
			z = z + 1
			return ("подбить", z)
		else:
			return ("уничтожить", z) 
		
print("Игра началась!")
print("Вам дается 50 попыток, чтобы найти корабль.")
print("Введите предпологаемые вами координаты корабля!")
ship_2 = coordinate_ship2(c_string, c_column) #создание двухпалубного корабля

for (x, y) in ship_2: # отображение реальных координат корабля (для отладки)
	print((x+1), (y+1))
	
shot_ship_deck = 0

for value in range(1, 51):
    # координаты вводимые пользователем с проверкой ввода типа данных
	try:
		player_string = int(input("Пожалуйста, введите номер строки:"))
		player_column = int(input("Пожалуйста, введите номер столбца:"))
	except ValueError:
		print("Вы должны вводить цифры!!!")
		continue
	if value < 50: # количество попыток
		if ((player_string - 1), (player_column - 1)) in ship_2:
			shotting = shot_ship((player_string), (player_column), shot_ship_deck)
			shot_ship_deck += shotting[1] 
			print("Поздравляем! Вам удалось %s корабль!" % (shotting[0]))
			if shotting[0] == "уничтожить":
				print("Вы выиграли!!!Поздравляем!!!")
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
			s = ""
			for x, y in ship_2:
				s = s + "%s:%s " % (x, y)
			print("Корабль находился на координатах: %s" %(s))
		except IndexError:
			print("Нет таких координат! Вы проиграли, исчерпав свои попытки...")
		break
