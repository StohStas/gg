from Board import Board
import pygame
import sys
from Bot import *
from itertools import product

fig = {
    # размер каждой картинки должен быть 100х100
    'w': pygame.image.load('w.png'),  # белая фишка
    'b': pygame.image.load('b.png'),  # черная фишка
    'W': pygame.image.load('W.png'),  # белая дамка
    'B': pygame.image.load('B.png'),  # черная дамка
    '.': pygame.image.load('brd_w.png'),  # белое поле
    '*': pygame.image.load('brd_b.png')  # черное поле

}
# размер поля 800х800
sc = pygame.display.set_mode((900, 800))

checkers = Board()
mv = [None, None]
clock = pygame.time.Clock()
flag = None
while 1:
    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:
            temp = (7 - ev.pos[1] // 100, ev.pos[0] // 100)
            if not mv[0]:
                mv[0] = temp if temp in checkers.brd.keys() and checkers.brd[temp] in 'wbWB' else None
            else:
                mv[1] = temp
        if ev.type == pygame.QUIT:
            sys.exit()
    # ход сформирован? сделать его(если возможно)
    if mv[1] != None:
        pass
        checkers.move(*mv)
        mv = [None, None]
    if not checkers.have_move():
        checkers.winner = 1 - checkers.order_of_move
    if checkers.winner == -1:
        # Боты
        if checkers.order_of_move == 1:
            botv1(checkers, checkers.order_of_move)

    # Рисуем доску
    pygame.draw.rect(sc, [(255, 255, 255), (0, 0, 0), (127, 127, 127)][checkers.winner if checkers.winner != -1 else 2],
                     (800, 100, 100, 700))
    sc.blit(fig['wb'[checkers.order_of_move]], fig['wb'[checkers.order_of_move]].get_rect(topleft=(800, 0)))  # кто сейчас ходит
    pygame.draw.line(sc, (0, 0, 0), [802, 0], [802, 800], 5)
    for y, x in product(range(8), range(8)):
        if (7 - y, x) in checkers.brd.keys():
            sc.blit(fig[checkers.brd[(7 - y, x)]], fig[checkers.brd[(7 - y, x)]].get_rect(topleft=(x * 100, y * 100)))
        else:
            sc.blit(fig['.'], fig['.'].get_rect(topleft=(x * 100, y * 100)))

    # clock.tick(5)
    pygame.display.update()
