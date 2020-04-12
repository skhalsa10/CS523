"""
 Cellular Automata board. The initial configuration consists of 
 all cells being in Susceptible (S) state with one Infected (I)
 cell in the middle of the board. The board will update every iteration.
 Implemented by: Anas Gauba
"""
import numpy as np

class CABoard:
    # class static variables for 2d board specs.
    _board_row = 50
    _board_col = 50

    #constructor
    def __init__(self, input = [[]], isBoardRandom = False):
        # input matrix can be given when we are running iterations of CA.
        # private member var: __inputBoard 
        if (len(input) == CABoard._board_row):
            self.__inputBoard = input
        elif (isBoardRandom):
            self.randomBoard()
        else:
            self.buildInput()
    
    """
     Utility method to build input board which has 1st variant
     of the disease (I). 
     Returns an initial board configuration with all cells in 
     Susceptible (S) state except one in Infected (I) state.
    """
    def buildInput(self):
        boardRow = CABoard._board_row
        boardCol = CABoard._board_col
        # 2d board matrix (list comprehension).
        self.__inputBoard = [["" for col in range(0,boardCol)] for row in range(0,boardRow)]

        for r in range(0,boardRow):
            for c in range(0,boardCol):
                if r == boardRow/2-1 and c == boardCol/2-1:
                    self.__inputBoard[r][c] = "I"
                else:
                    self.__inputBoard[r][c] = "S"
    
    """
     Utility method to build initial random board which includes
     another variant of disease (I') as well it includes first variant (I).
     Returns an initial board configuration with all cells in Susceptible (S) state
     except for two random positions in the board with both disease variants (I and I').
     NOTE: I' is represented as i because its easy to encode in a string.
    """
    def randomBoard(self):
        boardRow = CABoard._board_row
        boardCol = CABoard._board_col
        rand = np.random

        i = [rand.randint(0,boardRow), rand.randint(0,boardCol)]
        iPrime = [rand.randint(0,boardRow), rand.randint(0,boardCol)]
        
        # choose different random location for i' if i and i' turned out
        # to be in the same spot.
        while(i == iPrime):
            iPrime = [rand.randint(0,boardRow), rand.randint(0,boardCol)]
        
        # 2d board (list comprehension).
        self.__inputBoard = [["" for col in range(0,boardCol)] for row in range(0,boardRow)]

        for r in range(0,boardRow):
            for c in range(0,boardCol):
                # include i in the initial board.
                if (r == i[0] and c == i[1]):
                    self.__inputBoard[r][c] = "I"
                # include i'
                elif (r == iPrime[0] and c == iPrime[1]):
                    self.__inputBoard[r][c] = "i"
                else:
                    self.__inputBoard[r][c] = "S"


    """
     Gets the 2d board for a current instance.
    """
    def getBoard(self):
        return self.__inputBoard
    
    """
     Sets the 2d board for this instance to the provided board as parameter.
    """
    def setBoard(self, board):
        self.__inputBoard = board

    """
     toString() method to print board.
    """
    def __str__(self):
        stringBuilder = ""
        for r in range(0,CABoard._board_row):
            for c in range(0,CABoard._board_col):
                stringBuilder += self.__inputBoard[r][c]
            stringBuilder += "\n"
        return stringBuilder
