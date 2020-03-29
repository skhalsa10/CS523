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
import random as rand
import CABoard
import itertools
from fractions import Fraction

class CA2dSIRDeterministicDynamics:    
    #constructor.
    # 1st variant can either be deterministic or non-deterministic. 2nd disease variant will be non-deterministic.
    def __init__(self, board, diseaseVariants = 1, rule_bits = 9, ruleTypeIsDeterministic = True):
        # define any instance variables.
        self.rule_bits = rule_bits
        self.currentBoard = board
        self.isDeterministic = ruleTypeIsDeterministic
        self.variants = diseaseVariants

        # probability of S->I' and I'->R' (I' and R' represented in code as i and r)
        self.__sToIPrimeProb = rand.uniform(0,1)
        self.__iPrimeToRPrimeProb = rand.uniform(0,1)
        print("s to i prime probability is: " + str(self.__sToIPrimeProb))
        print("i prime to r prime probability is: " + str(self.__iPrimeToRPrimeProb))
        
        # now permute rules.
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

    def transitionCellState(self, centerCell, variant):
        if (variant == 2):
            if (centerCell == "S"):
                return "i"
            elif(centerCell == "i"):
                return "r"
        elif(variant == 1):
            if (centerCell == "S"):
                return "I"
            elif (centerCell == "I"):
                return "R"

    """
     Private method that uses non-deterministic rules for 
     transitioning between S, I, R states using this probability
     function. This is for 1st variant of the disease where the 
     probability P(S->I) is based on the numbers of infected neighbors
     and P(I->R) is fixed to be 25%.
    """
    def __probabilityFunc(self, mapKey):
        centerOfKeyStr = mapKey[int(self.rule_bits/2)]

        if (centerOfKeyStr == "S"):
            # calculate the probability based on the numbers of neighbors
            # infected, the more infected, the higher the probability is for
            # this cell to become infected.
            numerator = mapKey.count("I")
            denominator = self.rule_bits - 1
            self.ruleFor1stVariant[mapKey] = numerator/denominator

        elif (centerOfKeyStr == "I"):
            # fixed probability, 10% => 1/10. 
            self.ruleFor1stVariant[mapKey] = 1/10
        else:
            # its R, so 0% probability that it will change, hence, it will remain R when __prob() is called in iterateCABoard().
            self.ruleFor1stVariant[mapKey] = 0
    
    """
     Private method to build initial probability to uniformly random chosen
     values between [0,1]. This is needed for GA so that the second
     variant can evolve with first variant. This will be called only initially when
     CA initializes.
    """
    def __initialProbForSecondVariant(self, mapKey):
        centerOfKeyStr = mapKey[int(self.rule_bits/2)]
        
        # handle the case of mapKey being all XSSSS.., etc. The probability should be 0 if there are no i neighbors.
        if (mapKey.count("i") == 0):
            self.ruleFor2ndVariant[mapKey] = 0
        # if there are infected neighbors, then the initial random prob is used.
        elif (centerOfKeyStr == "S"):
            self.ruleFor2ndVariant[mapKey] = self.__sToIPrimeProb
        elif (centerOfKeyStr == "i"):
            self.ruleFor2ndVariant[mapKey] = self.__iPrimeToRPrimeProb
        # its r, 0% probability it will change.
        else:
            self.ruleFor2ndVariant[mapKey] = 0


    """
     Private helper method to return True/False based on the uniform distribution
     of how likely an event is likely to occur based on the fraction
     P = numerator/denominator.
    """
    def __prob(self, percent):
        #print("Goin in prob function to calculate percent probability")
        probFrac = Fraction(percent).limit_denominator()
        randNum = np.random.randint(1,probFrac.denominator+1)

        if (randNum <= probFrac.numerator):
            return True
        return False

    """
     Private method that uses deterministic rule mapping. 
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
            if (not self.isDeterministic):
                if (self.variants == 2):
                    self.__probabilityFunc("".join(mapKey))
                    self.__initialProbForSecondVariant("".join(mapKey))
                else:
                    self.__probabilityFunc("".join(mapKey))
            else:
                # for deterministic rules, we will just use 1st variant of disease only for now.
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
            if (not self.isDeterministic):
                if (self.variants == 2):
                    self.__initialProbForSecondVariant(topLeftCellKey)
                    self.__initialProbForSecondVariant(bottomLeftCellKey)
                    self.__initialProbForSecondVariant(topRightCellKey)
                    self.__initialProbForSecondVariant(bottomRightCellKey)

                    self.__probabilityFunc(topLeftCellKey)
                    self.__probabilityFunc(bottomLeftCellKey)
                    self.__probabilityFunc(topRightCellKey)
                    self.__probabilityFunc(bottomRightCellKey)
                else:
                    self.__probabilityFunc(topLeftCellKey)
                    self.__probabilityFunc(bottomLeftCellKey)
                    self.__probabilityFunc(topRightCellKey)
                    self.__probabilityFunc(bottomRightCellKey)
            else:
                # for deterministic rules, we will just use 1st variant of disease only for now.
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
            if (not self.isDeterministic):
                if (self.variants == 2):
                    self.__initialProbForSecondVariant(leftEdge)
                    self.__initialProbForSecondVariant(topEdge)
                    self.__initialProbForSecondVariant(rightEdge)
                    self.__initialProbForSecondVariant(bottomEdge)

                    self.__probabilityFunc(leftEdge)
                    self.__probabilityFunc(topEdge)
                    self.__probabilityFunc(rightEdge)
                    self.__probabilityFunc(bottomEdge)
                else:
                    self.__probabilityFunc(leftEdge)
                    self.__probabilityFunc(topEdge)
                    self.__probabilityFunc(rightEdge)
                    self.__probabilityFunc(bottomEdge)
            else:
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
        # map of (str, char), thats for deterministic rules (part 2a) for 1st variant of disease.
        self.rule = {}
        # non-deterministic rule of mapKeys of str for a cell with probability number (for 1st variant), this map will not be 
        # modified.
        self.ruleFor1stVariant = {}
        # the initial rule of mapKeys with uniform random probability values between [0,1] for both s->i' and i-> r'.
        # after each run (the whole CA board is fully recovered), the GA will evolve both s->i' and i->r' probabilities in this
        # map for a given CA. 
        self.ruleFor2ndVariant = {}
        firstVariantDynamics = "SIR"
        # i and r are I' and R' here for a second variant of disease.
        secondVariantDynamics = "Sir"

        # call helper methods to build rules (permutation for each scenario).
        # for 2nd variant, we need S,I',R' dynamics (encoded as "Sir").
        if (self.variants >= 2):
            # add both dynamics.
            self.__normalRuleEntries(firstVariantDynamics)
            self.__cornerRuleEntries(firstVariantDynamics)
            self.__edgesRuleEntries(firstVariantDynamics)

            self.__normalRuleEntries(secondVariantDynamics)
            self.__cornerRuleEntries(secondVariantDynamics)
            self.__edgesRuleEntries(secondVariantDynamics)
        else:
            self.__normalRuleEntries(firstVariantDynamics)
            self.__cornerRuleEntries(firstVariantDynamics)
            self.__edgesRuleEntries(firstVariantDynamics)

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
        #print("Current board:\n")        
        #print(self.currentBoard)
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
                
                # check to see which rule we are using, deteministic(uses only 1st variant) or non-deterministic (can use either both or 1st variant).
                if (not self.isDeterministic):
                    centerOfKeyStr = ruleKeyStr[int(self.rule_bits/2)]
                    if (self.variants == 2):
                        #print("using both variants non-deterministic")
                        # handle the case for both I and I' in the neighborhood of current cell, if they're then we randomly pick one probFunc.
                        if ("I" in ruleKeyStr and "i" in ruleKeyStr):
                            r = np.random.randint(0,2)
                            # go to first variant map.
                            if (r == 0):
                                # get the probabilityPercent from first variant if there.
                                if (ruleKeyStr in self.ruleFor1stVariant):
                                    percent = self.ruleFor1stVariant[ruleKeyStr]
                                    # check based on the probability if we can transition from first variant. Otherwise,
                                    # go to the second disease variant map to see if we can transition cell state from that map,
                                    # if we cannot do it from there, then we keep the same cell.
                                    if (self.__prob(percent)):
                                        next[r][c] = self.transitionCellState(centerOfKeyStr, variant=1)
                                    else:
                                        if (ruleKeyStr in self.ruleFor2ndVariant):
                                            percent = self.ruleFor2ndVariant[ruleKeyStr]
                                            if (self.__prob(percent)):
                                                next[r][c] = self.transitionCellState(centerOfKeyStr, variant=2)
                                            else:
                                                next[r][c] = centerOfKeyStr
                                        else:
                                            print("This 1st variant non-deterministic ruleKey doesn't exist yet while using both variants: " + ruleKeyStr)

                                else:
                                    print("This 1st variant non-deterministic ruleKey doesn't exist yet while using both variants: " + ruleKeyStr)
                            # go to second variant map.
                            elif (r == 1):
                                # get the probabilityPercent from second variant if there.
                                if (ruleKeyStr in self.ruleFor2ndVariant):
                                    percent = self.ruleFor2ndVariant[ruleKeyStr]
                                    # check based on the probability if we can transition from second variant. Otherwise,
                                    # go to the first disease variant map to see if we can transition cell state from that map,
                                    # if we cannot do it from there, then we keep the same cell.
                                    if (self.__prob(percent)):
                                        next[r][c] = self.transitionCellState(centerOfKeyStr, variant=2)
                                    else:
                                        if (ruleKeyStr in self.ruleFor1stVariant):
                                            percent = self.ruleFor1stVariant[ruleKeyStr]
                                            if (self.__prob(percent)):
                                                next[r][c] = self.transitionCellState(centerOfKeyStr, variant=1)
                                            else:
                                                next[r][c] = centerOfKeyStr
                                        else:
                                            print("This 2nd variant non-deterministic ruleKey doesn't exist yet while using both variants: " + ruleKeyStr)

                                else:
                                    print("This 2nd variant non-deterministic ruleKey doesn't exist yet while using both variants: " + ruleKeyStr)

                        # handle the case where only I is in neighborhood and not I' (goto first variant map)
                        elif("I" in ruleKeyStr and not("i" in ruleKeyStr)):
                            if (ruleKeyStr in self.ruleFor1stVariant):
                                percent = self.ruleFor1stVariant[ruleKeyStr]
                                # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
                                if (self.__prob(percent)):
                                    next[r][c] = self.transitionCellState(centerOfKeyStr, variant=1)
                                else:
                                    next[r][c] = centerOfKeyStr
                            else:
                                print("This 1st variant non-deterministic ruleKey doesn't exist yet while using both variants and only I is in neighborhood: " + ruleKeyStr)

                        # handle the case where only I' is in neighborhood and not I (goto second variant map)
                        elif("i" in ruleKeyStr and not("I" in ruleKeyStr)):
                            if (ruleKeyStr in self.ruleFor2ndVariant):
                                percent = self.ruleFor2ndVariant[ruleKeyStr]
                                # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
                                if (self.__prob(percent)):
                                    next[r][c] = self.transitionCellState(centerOfKeyStr, variant=2)
                                else:
                                    next[r][c] = centerOfKeyStr                                
                            else:
                                print("This 2nd variant non-deterministic ruleKey doesn't exist yet while using both variants and only I' is in neighborhood: " + ruleKeyStr)

                        # else there are no I and I' in the neighborhood, the centerCell is either surrounded by all SSS.., or the cells have recovered
                        # (R or r for both variants)
                        else:
                            next[r][c] = centerOfKeyStr

                    else:
                        # only use 1st variant non-determinsitc rule. 
                        if (ruleKeyStr in self.ruleFor1stVariant):
                            percent = self.ruleFor1stVariant[ruleKeyStr]
                            # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
                            if (self.__prob(percent)):
                                next[r][c] = self.transitionCellState(centerOfKeyStr, variant=1)
                            else:
                                next[r][c] = centerOfKeyStr
                        else:
                            print("This 1st variant non-deterministic ruleKey doesn't exist yet: " + ruleKeyStr)
                else:
                    # Use deterministic rules for 1st variant.
                    # Check now whether a key is already in dictionary (it should always
                    # be because we accounted all possibilities for each cell).
                    if (ruleKeyStr in self.rule):
                        next[r][c] = self.rule[ruleKeyStr]
                    else:
                        print("This determinstic ruleKey doesn't exist yet: " + ruleKeyStr)
        
        # after one iteration, we now have next board.
        self.nextBoard = self.createNextBoard(next)
        #print("Next board:\n")
        #print(self.nextBoard)
        self.currentBoard.setBoard(self.nextBoard.getBoard())
        
        return self.nextBoard.getBoard()





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