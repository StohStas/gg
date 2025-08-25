import random
from Board import Board
import copy


def botv1(game: Board, player):
    ff = 1
    if game.order_of_move == player:
        if game.ready_to_attack:
            start = random.choice([el[0] for el in game.ready_to_attack])
        else:
            start = random.choice(list(filter(lambda field: game.brd[field] in ['wW', 'bB'][player], game.brd)))
        while ff < 100:
            ff += 1
            end = random.choice(game.potenitsal_move_from(start, game.brd[start]))
            if game.is_posible_move(start, end):
                game.move(start, end)
                break


def quality(game: Board, player):
    q = 0
    for field in game.brd.keys():
        temp = game.brd[field]
        if temp == '*':
            continue
        q = q + 1 * ([-1, 1][temp in ['wW', 'bB'][player]]) * [1, 4][temp.isupper()]
    return q

#
# def botv2(game: Board, player):
#     mv1 = []
#     print('botv2: ', end='')
#     for start in game.brd.keys():
#         for end in game.potenitsal_move_from(start, game.brd[start]):
#             if game.is_posible_move(start, end):
#                 mv1.append((start, end))
#     X1 = [copy.deepcopy(game) for _ in range(len(mv1))]
#     mv2 = [[] for _ in range(len(mv1))]
#     X2 = [[] for _ in range(len(mv1))]
#     for k in range(len(mv1)):
#         X1[k].move(*mv1[k])
#         for start in game.brd.keys():
#             for end in game.potenitsal_move_from(start, game.brd[start]):
#                 if game.is_posible_move(start, end):
#                     mv2[k].append((start, end))
#         X2[k] = [copy.deepcopy(X1[k]) for _ in range(len(mv2))]
#     max_k = -1
#     min_qlt = 1000
#     for k, X in enumerate(X2):
#         for el in X:
#             if min_qlt >= quality(el, player):
#                 min_qlt = quality(el, player)
#                 max_k = k
#     game.move(*mv1[max_k])
