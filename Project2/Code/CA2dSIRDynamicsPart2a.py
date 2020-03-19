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
        self.board = board

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

        if (r < 0 or r > rowLim or c < 0 or c > colLim):
            return False
        
        return True

    def permuteToBuildInitialRules(self):
        print("Hello\n")
        # rules (str, char).
        # permute 9 (#rule_bits) letter string with SIR combinations.
        # XXXSXXX for edge cases.
        # Based on the center character, do the mapping:
        #   if it is R, always map the value to R.
        #   if it is I, only goes to R if all neighbors are I. Otherwise, map to stay I.
        #   if it is S, only go to I if atleast one neighbor is I. Otherwise, maps to S. 
        self.rule = {}
        dynamics = "SIR"
        # finds all permutation with repitition of chars.
        # generates all possible 3 letter (SIR) strings for length 9 neighbors (rule_bits).
        # The outcomes can be 3 possibilities for all the 9 neighbors, so,
        # the rule map has 3^9 entries = 19683.
        mapEntries = itertools.product(dynamics, repeat = self.rule_bits)

        for j in list(mapEntries):
            centerOfKey = j[int(self.rule_bits/2)]
            print(j[int(self.rule_bits/2)])

def main():
    board = CABoard.CABoard()
    ca = CA2dSIRDeterministicDynamics(board)

if __name__ == '__main__':
    main()       