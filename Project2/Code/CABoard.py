"""
 Cellular Automata board. The initial configuration consists of 
 all cells being in Susceptible (S) state with one Infected (I)
 cell in the middle of the board. The board will update every iteration.
 Implemented by: Anas Gauba
"""
class CABoard:
    # class static variables for 2d board specs.
    _board_row = 200
    _board_col = 200

    #constructor
    def __init__(self, input = [[]]):
        # input matrix can be given when we are running iterations of CA.
        # private member var: __inputBoard 
        if (len(input) == CABoard._board_row):
            self.__inputBoard = input
        else:
            self.buildInput()
    
    """
     Utility method to build input. 
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

# test = CABoard()
# print(test)
# anotherMat = test.inputBoard
# anotherMat[0][1] = "I"
# test2 = CABoard(anotherMat)
# print(test2)