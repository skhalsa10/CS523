"""
 Gui version of 2d CA, part 2a.
 Implemented by: Anas Gauba
"""
from p5 import * 
from CA2dSIRDynamicsPart2a import CA2dSIRDeterministicDynamics
from CABoard import *

# global vars.
boardObj = CABoard(isBoardRandom=True)
ca = CA2dSIRDeterministicDynamics(boardObj, diseaseVariants=2, ruleTypeIsDeterministic=False)
y = 0

"""
 size of gui.
"""
def setup():
    size(CABoard._board_row*10,CABoard._board_col*10)
    stroke(0)
    title("CA 2d SIR Dynamics")

def display():
    global y
    board = boardObj.getBoard()

    for x in range(0,CABoard._board_col):
        if board[x][y] == "S":
            fill(0,128,0)
        elif board[x][y] == "I":
            fill(255,0,0)
        elif board[x][y] == "i":
            fill(255,165,0)
        elif board[x][y] == "r":
            fill(0,0,0)
        else:
            fill(0,0,255)
        square((x*10,y*10),10)
    
    y += 1
    if (y >= CABoard._board_row):
        #background(0)
        y = 0 
        board = ca.iterateCABoard().getBoard()

"""
 gets called 60 fps. draws on the canvas.
"""
def draw():
    display()

if __name__ == '__main__':
    run()