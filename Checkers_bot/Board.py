from itertools import product


class Board:

    def __init__(self, brd=None):
        self.order_of_move = 0  # 0 - белый, 1 - черный
        self.ready_to_attack = []
        self.winner = -1
        if brd:
            self.brd = brd
        else:
            self.brd = {
                (7, 1): 'b', (7, 3): 'b', (7, 5): 'b', (7, 7): 'b',
                (6, 0): 'b', (6, 2): 'b', (6, 4): 'b', (6, 6): 'b',
                (5, 1): 'b', (5, 3): 'b', (5, 5): 'b', (5, 7): 'b',
                (4, 0): '*', (4, 2): '*', (4, 4): '*', (4, 6): '*',
                (3, 1): '*', (3, 3): '*', (3, 5): '*', (3, 7): '*',
                (2, 0): 'w', (2, 2): 'w', (2, 4): 'w', (2, 6): 'w',
                (1, 1): 'w', (1, 3): 'w', (1, 5): 'w', (1, 7): 'w',
                (0, 0): 'w', (0, 2): 'w', (0, 4): 'w', (0, 6): 'w'
            }

    # печать в консоль
    def print_brd(self):
        for y, x in product(range(8), range(8)):
            if (7 - y, x) in self.brd.keys():
                print(self.brd[(7 - y, x)], end='')
            else:
                print('.', end='')
            if x == 7:
                print()

    def is_posible_move(self, start, end):
        if start in self.brd.keys() and end in self.brd.keys():  # выбрать можно только черные клетки поля
            if self.ready_to_attack:  # если возможно взятие, тогда можно только брать
                if (start, end) in self.ready_to_attack:
                    return True
                else:
                    return False
            if self.brd[start] in ['wW', 'bB'][self.order_of_move] and self.brd[
                end] == '*':  # ход начинается с фигуры правильного цвета, а заканчивается пустым полем
                if self.brd[start].islower():  # НЕ дамка
                    if end[0] - start[0] == [1, -1][self.order_of_move] and (end[1] - start[1]) in [1, -1]:
                        return True  # можно ходить только в сторону противника и по диагонали на 1
                else:  # дамка
                    if abs(end[1] - start[1]) == abs(end[0] - start[0]):  # ходим по дагоналям
                        return True

    def move(self, start, end):
        if self.is_posible_move(start, end):
            self.brd[start], self.brd[end] = self.brd[end], self.brd[start]
            if end[0] in [0, 7]:
                self.brd[end] = self.brd[end].upper()
            for k in range(abs(start[0] - end[0])):
                if self.brd[
                    (start[0] + k * (-1 if end[0] - start[0] < 0 else 1),
                     start[1] + k * (-1 if end[1] - start[1] < 0 else 1))] != '*':
                    self.brd[
                        (start[0] + k * (-1 if end[0] - start[0] < 0 else 1),
                         start[1] + k * (-1 if end[1] - start[1] < 0 else 1))] = '*'
                    self.update_ready_to_attack()
                self.brd[
                    (start[0] + k * (-1 if end[0] - start[0] < 0 else 1),
                     start[1] + k * (-1 if end[1] - start[1] < 0 else 1))] = '*'

            if end not in [el[0] for el in self.ready_to_attack]:
                self.order_of_move = 1 - self.order_of_move  # меняем очередность хода
                self.update_ready_to_attack()
        else:
            print(f'Невозможный ход: {start} -> {end}')

    def update_ready_to_attack(self):
        temp = []
        for y, x in self.brd.keys():
            if self.brd[(y, x)] not in ['wW', 'bB'][self.order_of_move]:
                continue
            for j, i in product([1, -1], [1, -1]):
                if 0 <= y + 2 * j <= 7 and 0 <= x + 2 * i <= 7 and (
                        self.brd[(y, x)].lower(), self.brd[(y + j, x + i)].lower(), self.brd[(y + 2 * j, x + 2 * i)].lower()) == (
                        'wb'[self.order_of_move], 'bw'[self.order_of_move], '*'):
                    temp.append(((y, x), (y + 2 * j, x + 2 * i)))
            if self.brd[(y, x)] in 'WB':
                for k in range(2, 8):
                    for j, i in product([1, -1], [1, -1]):
                        if 0 <= y + k * j <= 7 and 0 <= x + k * i <= 7:
                            if (self.brd[(y, x)].lower(), ''.join([self.brd[(y + j * u, x + i * u)] for u in range(1, k) if
                                                                   self.brd[(y + j * u, x + i * u)] != '*']).lower(),
                                self.brd[(y + k * j, x + k * i)].lower()) == (
                                    'wb'[self.order_of_move], 'bw'[self.order_of_move], '*'):
                                temp.append(((y, x), (y + k * j, x + k * i)))

        self.ready_to_attack = temp

    def have_move(self):
        for start in self.brd.keys():
            for end in self.potenitsal_move_from(start, self.brd[start]):
                if self.is_posible_move(start, end):
                    return True
        return False

    def potenitsal_move_from(self, start, piece='A'):
        if piece.isupper():
            return [(start[0] + k * j, start[1] + k * i) for k, i, j in product(range(1, 8), [-1, 1], [-1, 1]) if
                    0 <= start[0] + k * j <= 7 and 0 <= start[1] + k * i <= 7]
        else:
            return [(start[0] + k * j, start[1] + k * i) for k, i, j in product([1, 2], [-1, 1], [-1, 1]) if
                    0 <= start[0] + k * j <= 7 and 0 <= start[1] + k * i <= 7]
