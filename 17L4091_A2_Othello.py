import numpy as np
import pygame as pg
import sys
import copy

# Computer is Max, also Human makes the first move
# turn = 1       FOR HUMAN
# turn = -1      FOR COMPUTER


# Global Variables
BLACK = pg.Color(0, 0, 0)
RED = pg.Color(255, 0, 0)
WHITE = pg.Color(255, 255, 255)
GREEN = pg.Color(113, 29, 122)
BROWN = pg.Color(222, 184, 135)
DIFFICULTY = 3
WIN = 0

class State:
    def __init__(self):
        self.size = 8
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
        self.rectangles = []
        self.White = 0
        self.Black = 0


    def update(self):
        Black = 0
        White = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    Black += 1
                elif self.board[i][j] == -1:
                    White += 1
        self.Black = Black
        self.White = White

    def EP(self):
        return self.Black - self.White

class Othello:



    def initial_moves(self):
        half = int(len(self.board.rectangles) / 2)
        self.board.board[half - 1][half - 1] = 1
        self.board.board[half - 1][half] = -1
        self.board.board[half][half - 1] = -1
        self.board.board[half][half] = 1

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.board = State()
        self.screenSize = 720
        self.screen = pg.display.set_mode((self.screenSize, self.screenSize))
        initialDistance = 2.5 * self.board.size
        temp = self.screenSize - initialDistance
        self.blockSize = temp / self.board.size
        self.create_board()
        self.initial_moves()

    def create_board(self):
        global BLACK, RED, GREEN
        for y in range(self.board.size):
            rectangles = []
            for x in range(self.board.size):
                rect = pg.Rect(x * (self.blockSize + 2.5), y * (self.blockSize + 2.5), self.blockSize, self.blockSize)
                rectangles.append(rect)
            self.board.rectangles.append(rectangles)

    def legal_direction(self, r, c,state, turn, x_cord, y_cord):
        foundOpponent = False
        while (r >= 0 and r <= len(state.rectangles) and c >= 0 and c <= len(state.rectangles)):
            r = r + x_cord
            c = c + y_cord
            if (r < 0 or r >= len(state.rectangles) or c < 0 or c >= len(state.rectangles)):
                return False
            if (state.board[r][c] == 0):
                return False
            if (state.board[r][c] == abs(state.board[r][c]) * turn):
                if foundOpponent:
                    return True
                else:
                    return False
            if (state.board[r][c] != abs(state.board[r][c]) * turn):
                foundOpponent = True
        return False

    def legal_ones(self, r, c,state,turn):
        legalDirections = []
        if (state.board[r][c] != 0):
            return legalDirections
        if (self.legal_direction(r, c,state, turn, -1, -1)):
            legalDirections.append((-1, -1))
        if (self.legal_direction(r, c,state, turn, -1, 0)):
            legalDirections.append((-1, 0))
        if (self.legal_direction(r, c,state, turn, -1, 1)):
            legalDirections.append((-1, 1))
        if (self.legal_direction(r, c,state, turn, 0, -1)):
            legalDirections.append((0, -1))
        if (self.legal_direction(r, c,state, turn, 0, 0)):
            legalDirections.append((0, 0))
        if (self.legal_direction(r, c,state, turn, 0, 1)):
            legalDirections.append((0, 1))
        if (self.legal_direction(r, c,state, turn, 1, -1)):
            legalDirections.append((1, -1))
        if (self.legal_direction(r, c,state, turn, 1, 0)):
            legalDirections.append((1, 0))
        if (self.legal_direction(r, c,state, turn, 1, 1)):
            legalDirections.append((1, 1))
        return legalDirections

    def checkIfWin(self):
        for i in range(len(self.board.rectangles)):
            for j in range(len(self.board.rectangles)):
                if self.board.board[i][j] == 0:
                    return False
        return True

    def whoWin(self):
        Black = 0
        White = 0
        for i in range(len(self.board.rectangles)):
            for j in range(len(self.board.rectangles)):
                if self.board.board[i][j] == 1:
                    Black += 1
                else:
                    White += 1

        if (Black > White):
            return Black, "Black"
        elif (White > Black):
            return White, "White"
        else:
            return Black, "Draw"

    def generate_steps(self,state, turn):
        moves = []
        for r in range(self.board.size):
            for c in range(self.board.size):
                move = self.legal_ones(r, c,state,turn)
                if (move != []):
                    moves.append((r, c, move))

        return moves

    def draw_board(self):
        global GREEN, BLACK, WHITE
        for x_count, x in enumerate(self.board.rectangles):
            for y_count, y in enumerate(x):
                if (self.board.board[x_count][y_count] == 0):
                    pg.draw.rect(self.screen, GREEN, y)
                elif (self.board.board[x_count][y_count] == 1):  # Computer, Max Lvel
                    pg.draw.rect(self.screen, BLACK, y)
                elif (self.board.board[x_count][y_count] == -1):
                    pg.draw.rect(self.screen, WHITE, y)

    def minimax(self,rootState, depth, isMax):

        optimalMove = -1
        rootState.update()

        if (rootState.Black + rootState.White == (rootState.size * rootState.size)):
            if (isMax == 1):
                return -99999, -1
            else:
                return 99999, -1

        if (depth <= 0):
            rootState.update()
            return rootState.EP(), optimalMove



        if (isMax == 1):

            max = -99999
            states = []
            moves = self.generate_steps(rootState,1)
            for i, move in enumerate(moves):
                r, c, direction = move
                state = copy.deepcopy(rootState)       #Replica state
                state.board[r][c] = 1  # place move on grid and calculate # no moves
                self.fill(move, 1, state)
                temp, zayaMove = self.minimax(state, depth - 1, isMax * -1)

                if (temp > max):
                    max = temp
                    optimalMove = move

            return max, optimalMove

        else:
            min = 99999
            moves = self.generate_steps(rootState, -1)
            for i, move in enumerate(moves):
                r, c, direction = move
                state = copy.deepcopy(rootState)
                state.board[r][c] = -1  # place move on grid and calculate # no moves
                self.fill(move, -1, state)

                temp, zayaMove = self.minimax(state, depth - 1, isMax * -1)
                if (temp < min):
                    min = temp
                    optimalMove = move
            return min, optimalMove

    def declareWinner(self, moves, name):
        if (name == "Black"):
            print("Black Win")
        elif (name == "White"):
            print("White Win")
        else:
            print("Draw")

    def fill(self, move, turn, state):
        r, c, direction = move
        for tuple in direction:
            t1, t2 = tuple
            i = r
            j = c
            i = i + t1
            j = j + t2
            while (state.board[i][j] != turn):
                state.board[i][j] = turn
                i = i + t1
                j = j + t2


    def run(self):

        global DIFFICILTY
        global WHITE, BLACK, RED, GREEN, BROWN
        global WIN

        # while True:
        #     self.StartingScreen()

        turn = -1
        generated = 0;
        while (True):

            self.clock.tick(60)
            if (generated != 1):
                moves = self.generate_steps(self.board, turn)
                if(moves == []):
                    #White Loses
                    print("Computer Wins")
                    WIN = -1
                generated = 1

            for event in pg.event.get():

                # if human
                if (turn == -1):

                    # if mouse button is pressed
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()

                        # In all rectangles search which one was clicked
                        for x_count, x in enumerate(self.board.rectangles):
                            for y_count, y in enumerate(x):
                                if y.collidepoint(pos):
                                    for move in moves:
                                        r, c, direction = move
                                        if ((x_count, y_count) == (r, c)):
                                            self.board.board[x_count][y_count] = -1
                                            self.fill(move, turn, self.board)
                                            turn = turn * -1
                                            generated = -1



                # Computer
                elif (turn == 1):
                    # check if legal move
                    value, move = self.minimax(self.board, DIFFICULTY, 1)
                    if(move == [] or move == -1):
                        #Computer Lose
                        print("Human Win")
                        WIN = 1
                        break
                    if(WIN == 0):
                        r, c, direction = move
                        self.board.board[r][c] = 1
                        self.fill(move, turn, self.board)
                        turn = turn * -1
                        generated = -1

                # Quit event
                if event == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # Check if Win
            if (self.checkIfWin()):
                moves, name = self.whoWin()
                self.declareWinner(moves, name)

            self.screen.fill(BROWN)
            self.draw_board()
            pg.display.update()  # Making changes to Screen




def main():
    game = Othello()
    game.run()


if __name__ == '__main__':
    main()


