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
        if (len(input) == CABoard._board_row):
            self.inputBoard = input
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
        self.inputBoard = [["" for col in range(0,boardCol)] for row in range(0,boardRow)]

        for r in range(0,boardRow):
            for c in range(0,boardCol):
                if r == boardRow/2 and c == boardCol/2:
                    self.inputBoard[r][c] = "I"
                else:
                    self.inputBoard[r][c] = "S"
            
    """
     toString() method to print board.
    """
    def __str__(self):
        stringBuilder = ""
        for r in range(0,CABoard._board_row):
            for c in range(0,CABoard._board_col):
                stringBuilder += self.inputBoard[r][c]
            stringBuilder += "\n"
        return stringBuilder

# test = CABoard()
# print(test)
# anotherMat = test.inputBoard
# anotherMat[0][1] = "I"
# test2 = CABoard(anotherMat)
# print(test2)