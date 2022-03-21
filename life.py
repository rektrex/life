from random import random
from os import system
from os.path import exists
from time import sleep
import sys


def initializeBoard(length, breadth, isDead=False):
    '''Returns a random board of given dimensions'''

    if isDead:
        return [[0 for _ in range(breadth)] for _ in range(length)]

    return [[1 if random() > 0.75 else 0 for _ in range(breadth)] for _ in range(length)]


def renderBoard(board):
    '''Renders the board to stdout using ASCII characters'''
    print()
    print('\n'.join(
          [''.join(
           ['@' if col == 1 else ' ' for col in row]) for row in board]))
    print()


def getCoordValueWrapper(board):
    def getCoordValue(row, col):
        try:
            return board[row][col]
        except IndexError:
            return 0

    return getCoordValue


def nextState(board):
    '''Returns the next state of a board'''

    length = len(board)
    breadth = len(board[0])
    newBoard = initializeBoard(length, breadth, isDead=True)
    getCoordValue = getCoordValueWrapper(board)

    for row in range(length):
        for col in range(breadth):
            noOfAliveNbrs = 0
            for rowOffset in [-1, 0, 1]:
                for colOffset in [-1, 0, 1]:
                    if rowOffset == 0 and colOffset == 0:
                        continue
                    noOfAliveNbrs += getCoordValue(row +
                                                   rowOffset, col + colOffset)

            if bool(board[row][col]) and noOfAliveNbrs == 2:
                newBoard[row][col] = 1
            elif noOfAliveNbrs == 3:
                newBoard[row][col] = 1

    return newBoard


def loadFromFile(filename):
    with open(filename, 'r') as f:
        board = f.read().splitlines()
        board = list(map(list, board))
        return [list(map(int, i)) for i in board]


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        length = int(args[1])
        breadth = int(args[2])
        board = initializeBoard(length, breadth)
    elif len(args) == 2:
        patternName = args[1].lower()
        if exists('patterns/' + patternName + '.txt'):
            board = loadFromFile('patterns/' + patternName + '.txt')
        else:
            print('pattern does not exist')
            exit(0)
    else:
        print('1 or 2 arguments expected: python3 life.py pattern | python3 life.py length breadth')
        exit(0)
    while True:
        renderBoard(board)
        board = nextState(board)
        sleep(1)
        system('clear')
