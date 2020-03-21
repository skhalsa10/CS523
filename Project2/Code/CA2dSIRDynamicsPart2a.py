"""
 This is a 3-state, 2d Cellular Automata (CA) with SIR dynamics to model coronavirus
 epidemic spread using deterministic rules with neighborhood size 1 in all 8 directions of a 
 particular cell/indivual.
 SIR dynamics is: 
   - whether an individual is Susceptible (possiblity of getting infected).
   - whether an individual is Infected.
   - whether an individual has Recovered. 
 Implemented by: Anas Gauba
"""

import numpy as np
import CABoard
import itertools
from copy import deepcopy

class CA2dSIRDeterministicDynamics:    
    #constructor.
    def __init__(self, board, rule_bits = 9, ruleTypeIsDeterministic = True):
        # define any instance variables.
        self.rule_bits = rule_bits
        self.currentBoard = board
        # # create another board for next iteration.
        # self.nextBoard = self.createNextBoard(self.currentBoard.getBoard())

        # use determisitc rule.
        if (ruleTypeIsDeterministic):
            self.permuteToBuildInitialRules()

    """
     Checks whether we are in bounds or not.
     This method is helpful for when we are going to check each cell's 8 neighbors in the board.
    """    
    def isInBounds(self,r,c):
        rowLim = CABoard.CABoard._board_row
        colLim = CABoard.CABoard._board_col

        if (r < 0 or r >= rowLim or c < 0 or c >= colLim):
            return False
        
        return True

    """
     Private method that deterministic rule mapping. 
     Based on the center character from 9 letter long KeyStr, do the mapping:
        if it is R, always map the value to R.
        if it is I, only goes to R if all neighbors are I. Otherwise, map to stay I.
        if it is S, only go to I if atleast one neighbor is I. Otherwise, maps to S. 
    """
    def __populateRuleMap(self, mapKey):
        centerOfKeyStr = mapKey[int(self.rule_bits/2)]
        
        if (centerOfKeyStr == "S"):
            if ("I" in mapKey):
                self.rule[mapKey] = "I"
            else:
                self.rule[mapKey] = "S"
        elif (centerOfKeyStr == "I"):
            # all neighbors are inflected plus the center cell (the cell in question).
            # if thats the case, the cell in question recovers. 
            if (mapKey.count("I") == self.rule_bits):
                self.rule[mapKey] = "R"
            else:
                self.rule[mapKey] = "I"
        else:
            self.rule[mapKey] = "R"

    """
     Private methods that handles in bound permutations scenario of all 9 letters with SIR dynamics where cell follows S->I->R dynamics.
     Finds all in permutation with repitition of chars.
     generates all possible 3 letter (SIR) strings for length 9 neighbors (rule_bits).
     The outcomes can be 3 possibilities for all the 9 neighbors, so,
     the rule map has 3^9 entries = 19683.
    """
    def __normalRuleEntries(self, dynamics):
        regularmMapEntriesToBe = itertools.product(dynamics, repeat=self.rule_bits)

        for mapKey in list(regularmMapEntriesToBe):
            self.__populateRuleMap("".join(mapKey))


    """
      Private method that handles the four corner of the board cases and generates
      permutations of SIR with few neighbors.
      NOTE: The corner cells of the board have three neighbors in bound plus yourself,
      so four cells in bounds and each one of those cells has SIR (len=3) possiblities. 
      There are 4 corners in 2d grid. So, in total, the permutation to account for four corners is 4*(3^4). 
    """
    def __cornerRuleEntries(self, dynamics):
        # generate all permutations for four in bound cells (3^4).
        cornerPerm = itertools.product(dynamics, repeat=4)

        # there are four corners with five neighbors are out of bounds (X)
        # Just need to pad X's in the right place to make a key for rule dictionary/map.
        
        for perm in list(cornerPerm):
            # (0,0) case: 
            topLeftCellKey = "XXXX" + perm[0] + perm[1] + "X" + perm[2] + perm[3]
            # (n,0) case:
            bottomLeftCellKey = "XXX" + perm[0] + perm[1] + "X" + perm[2] + perm[3] + "X"
            # (0,n) case:
            topRightCellKey = "X" + perm[0] + perm[1] + "X" + perm[2] + perm[3] + "XXX"
            # (n,n) case:
            bottomRightCellKey = perm[0] + perm[1] + "X" + perm[2] + perm[3] + "XXXX"

            # add mapping for these in the map.
            self.__populateRuleMap(topLeftCellKey)
            self.__populateRuleMap(bottomLeftCellKey)
            self.__populateRuleMap(topRightCellKey)
            self.__populateRuleMap(bottomRightCellKey)


    """
      Private method that handles the edges of the board cases and generates
      permutations of SIR with few neighbors.
      NOTE: The cells on the edge of the board have five neighbors in bound plus yourself,
      so six cells in bounds and each one of those cells has SIR (len=3) possiblities. 
      The cells on the edges are at four places in 2d grid (leftEdges, topEdges, 
      rightEdges, bottomEdges). So, in total, the permutation to account for four edges is 4*(3^6).
    """
    def __edgesRuleEntries(self, dynamics):
        # generate all permutations for six in bound cells (3^6).
        edgesPerm = itertools.product(dynamics, repeat=6)

        # Pad three out of bound cells with X's.
        for perm in list(edgesPerm):
            leftEdge = "XXX" + "".join(perm)
            #print(leftEdge)
            topEdge = "X" + perm[0] + perm[1] + "X" + perm[2] + perm[3] + "X" + perm[4] + perm[5]
            rightEdge = "".join(perm) + "XXX"
            bottomEdge = perm[0] + perm[1] + "X" + perm[2] + perm[3] + "X" + perm[4] + perm[5] + "X"

            # add mapping for these in the dictionary. 
            self.__populateRuleMap(leftEdge)
            self.__populateRuleMap(topEdge)
            self.__populateRuleMap(rightEdge)
            self.__populateRuleMap(bottomEdge)


    """
      Permutes 9 (#rule_bits) letter string with SIR dynamics. The center cell of the 
      9 letter long string is cell in question on the board when we do the iteration for CA.
      To build rules and create mapping for cells, the model is of a population that doesn't move
      meaning the cells on the boundary (edges,corner) have fewer neighbors. So, the requried rules
      account for normal scenario (3^9 permutations), plus also accounts for cells on the four corners (4*3^4 permutations)
      and cells on the four edges (4*3^6 permutations).
      For more details, see the docs for all helper methods.    
    """
    def permuteToBuildInitialRules(self):
        # map of (str, char).
        self.rule = {}
        dynamics = "SIR"

        # call helper methods to build rules (permutation for each scenario).
        self.__normalRuleEntries(dynamics)
        self.__cornerRuleEntries(dynamics)
        self.__edgesRuleEntries(dynamics)



    """
     Creates instance of the board based on the currentBoard. 
    """
    def createNextBoard(self, board):
        return CABoard.CABoard(board)
    
    """
     Iterating each cell of the board. Building keyStr for each cell
     representing all eight neighbors plus cell itself (center of the keyStr).
     The keyStr representing neighbors are in this order: left, center, right. For example: the cell at (0,0) has neighbors:
        left:(-1,-1),(-1,0),(-1,1) -> All out of bounds (X)
        center:(0,-1),(0,0),(0,1) -> only (0,-1) is out of bounds.
        right:(1,-1),(1,0),(1,1) -> only (1,-1) is out of bounds.
     The inital rules (corner,edges,normal) are built keeping this pattern in mind.
     NOTE: The y's (rowOffSet's) are flipped to account for out of bounds.
           For example: (-1,-1) is upper left of the board. 
    """
    def iterateCABoard(self):
        print("Current board:\n")        
        print(self.currentBoard)
        rows = CABoard.CABoard._board_row
        cols = CABoard.CABoard._board_col
        # next board to be (after a iteration).
        next = [["" for col in range(0,cols)] for row in range(0,rows)]
        for r in range(0,rows):
            for c in range(0,cols):
                ruleKeyStr = ""
                # visits all left neighbors -> center -> right neighbors.
                # NOTE: y vals are flipped in the case of detecting out of bounds.
                for rowOffset in range(-1,2):
                    for colOffset in range(-1,2):
                        if (self.isInBounds(r+rowOffset, c+colOffset)):
                            curr = self.currentBoard.getBoard()
                            ruleKeyStr += curr[r+rowOffset][c+colOffset]
                        else:
                            # the current cell in the board is on the edge.
                            ruleKeyStr += "X"

                # Check now whether a key is already in dictionary.
                if (ruleKeyStr in self.rule):
                    next[r][c] = self.rule[ruleKeyStr]
                else:
                    print("This ruleKey doesn't exist yet: " + ruleKeyStr)
        
        # after one iteration, we now have next board.
        self.nextBoard = self.createNextBoard(next)
        print("Next board:\n")
        print(self.nextBoard)
        self.currentBoard.setBoard(self.nextBoard.getBoard())





def main():
    board = CABoard.CABoard()
    ca = CA2dSIRDeterministicDynamics(board)
    i = 4
    # iterate four times
    while (i > 0):
        ca.iterateCABoard()
        i -= 1


if __name__ == '__main__':
    main()       