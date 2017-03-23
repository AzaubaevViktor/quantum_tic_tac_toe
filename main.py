import itertools

from game import *

game = Game()

current_player_i = itertools.cycle((PLAYER_X, PLAYER_O))

while True:
    current_player = next(current_player_i)

    while True:
        positions = [
            int(x)
            for x in
            input(">> Positions (0-9) [Player {}] >>".format(current_player))
            if x.isdigit()
            ]

        if len(positions) < 2:
            print("Need min 2 value")
            continue

        try:
            game.step(current_player, positions)
            break
        except (ValueError, IndexError) as e:
            print(e)

    print("======== TABLES ========")
    tables = [str(table) for table in game.tables]

    for s, e in [(0, 3), (3, 6), (6, 9)]:
        for table in tables:
            print("{} ".format(table[s:e]), end='')
        print()
    print()
    print("======== WIN TABLES ========")
    tables = [str(table) for table in game.win_tables]

    for s, e in [(0, 3), (3, 6), (6, 9)]:
        for table in tables:
            print("{} ".format(table[s:e]), end='')
        print()
    print()
    print("========== FIELD =======")
    for pos, cell in zip(range(9), game.field):
        print(cell, end='')
        if 0 == (pos + 1) % 3:
            print()

    print()
    print("======== WINNERS =======")
    print("{}: {}/{}".format(PLAYER_X, game.winners[PLAYER_X], game.winners['tables']))
    print("{}: {}/{}".format(PLAYER_O, game.winners[PLAYER_O],
                             game.winners['tables']))
    print("{}: {}/{}".format(EMPTY_CELL, game.winners[EMPTY_CELL],
                             game.winners['tables']))
    print("======================================")
