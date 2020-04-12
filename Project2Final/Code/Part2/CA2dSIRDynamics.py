"""
 This is a 3-state, 2d Cellular Automata (CA) with SIR dynamics to model coronavirus
 epidemic spread using both deterministic and non-deterministic rules with neighborhood size 1 in all 9 directions of a 
 particular cell/indivual (including itself).
 SIR dynamics is: 
   - whether an individual is Susceptible (possiblity of getting infected).
   - whether an individual is Infected.
   - whether an individual has Recovered. 
 This also adds the logic for adding a second disease variant. It also has some GA logic such as mutate and crossover functions.
 This CA2dSIRDynamics can be used using deterministic rules, non-deterministic rules for a disease variant as well
 as it adds the functionality to be able to use 2nd disease variant with the 1st variant.
 Implemented by: Anas Gauba
"""

import numpy as np
import random as rand
import itertools
from CABoard import *
from fractions import Fraction

class CA2dSIRDynamics:
    # 1st variant can either be deterministic or non-deterministic. 2nd disease variant will be non-deterministic.
    def __init__(self,board,diseaseVariants=1, rule_bits=9, ruleTypeIsDeterministic=True):
        # define any instance variables.
        self.rule_bits = rule_bits
        self.currentBoard = board
        self.isDeterministic = ruleTypeIsDeterministic
        self.variants = diseaseVariants
        
        if (self.variants == 2):
            # probability of S->I' and I'->R' (I' and R' represented in code as i and r)
            self.__sToIPrimeProb = rand.uniform(0,1)
            self.__iPrimeToRPrimeProb = rand.uniform(0,1)
            #print("s to i prime probability is: " + str(self.__sToIPrimeProb))
            #print("i prime to r prime probability is: " + str(self.__iPrimeToRPrimeProb))
        
        # now permute rules.
        self.permuteToBuildInitialRules()

    """
     Checks whether we are in bounds or not.
     This method is helpful for when we are going to check each cell's 8 neighbors in the board.
    """    
    def isInBounds(self,r,c):
        rowLim = CABoard._board_row
        colLim = CABoard._board_col

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
     and P(I->R) is fixed to be 10%.
    """
    def __probabilityFunc(self, mapKey):
        centerOfKeyStr = mapKey[int(self.rule_bits/2)]

        if (centerOfKeyStr == "S"):
            # calculate the probability based on the numbers of neighbors
            # infected, the more infected, the higher the probability is for
            # this cell to become infected.
            numerator = mapKey.count("I")
            denominator = self.rule_bits - 1
            self.nonDeterministicRule1stVar[mapKey] = numerator/denominator

        elif (centerOfKeyStr == "I"):
            # fixed probability, 10% => 1/10. 
            self.nonDeterministicRule1stVar[mapKey] = 1/10
        else:
            # its R, so 0% probability that it will change, hence, it will remain R when __prob() is called in iterateCABoard().
            self.nonDeterministicRule1stVar[mapKey] = 0
    
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
            self.nonDeterministicRule2ndVar[mapKey] = 0
        # if there are infected neighbors, then the initial random prob is used.
        elif (centerOfKeyStr == "S"):
            self.nonDeterministicRule2ndVar[mapKey] = self.__sToIPrimeProb
        elif (centerOfKeyStr == "i"):
            self.nonDeterministicRule2ndVar[mapKey] = self.__iPrimeToRPrimeProb
        # its r, 0% probability it will change.
        else:
            self.nonDeterministicRule2ndVar[mapKey] = 0


    """
     Private helper method to return True/False based on the uniform distribution
     of how likely an event is likely to occur based on the fraction
     P = numerator/denominator.
    """
    def __prob(self, percent):
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
                self.deterministicRule1stVar[mapKey] = "I"
            else:
                self.deterministicRule1stVar[mapKey] = "S"
        elif (centerOfKeyStr == "I"):
            # all neighbors are inflected plus the center cell (the cell in question).
            # if thats the case, the cell in question recovers. 
            if (mapKey.count("I") == self.rule_bits):
                self.deterministicRule1stVar[mapKey] = "R"
            else:
                self.deterministicRule1stVar[mapKey] = "I"
        else:
            self.deterministicRule1stVar[mapKey] = "R"

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
                    if (dynamics == "SIR"):
                        self.__probabilityFunc("".join(mapKey))
                    else:
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
                    if (dynamics == "Sir"):
                        self.__initialProbForSecondVariant(topLeftCellKey)
                        self.__initialProbForSecondVariant(bottomLeftCellKey)
                        self.__initialProbForSecondVariant(topRightCellKey)
                        self.__initialProbForSecondVariant(bottomRightCellKey)
                    else:
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
            topEdge = "X" + perm[0] + perm[1] + "X" + perm[2] + perm[3] + "X" + perm[4] + perm[5]
            rightEdge = "".join(perm) + "XXX"
            bottomEdge = perm[0] + perm[1] + "X" + perm[2] + perm[3] + "X" + perm[4] + perm[5] + "X"

            # add mapping for these in the dictionary. 
            if (not self.isDeterministic):
                if (self.variants == 2):
                    if (dynamics == "Sir"):
                        self.__initialProbForSecondVariant(leftEdge)
                        self.__initialProbForSecondVariant(topEdge)
                        self.__initialProbForSecondVariant(rightEdge)
                        self.__initialProbForSecondVariant(bottomEdge)
                    else:
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
        # deterministic rule map for 1st disease variant.
        self.deterministicRule1stVar = {}
        # non-deterministic rule of mapKeys of str for a cell with probability number (for 1st variant), this map will not be 
        # modified.
        self.nonDeterministicRule1stVar = {}
        # the initial rule of mapKeys with uniform random probability values between [0,1] for both s->i' and i-> r'.
        # after each run (the whole CA board is fully recovered), the GA will evolve both s->i' and i->r' probabilities in this
        # map for a given CA. 
        self.nonDeterministicRule2ndVar = {}
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
        return CABoard(board)
    
    """
     Cross overs two CA's and create a children-CA with modified 
     probabilityMap for 2nd variant (ruleFor2ndVariant). After crossing over,
     slightly mutate newly created child CA's ruleFor2ndVariant map.
     The child is going to use the same board as in previous generation. 
    """
    def crossOver(self, secondParent):
        length = len(self.nonDeterministicRule2ndVar)-1
        cutover = rand.randint(0,length-1)
        
        # add N key:value pairs for parent 1 (N = cutover).
        # Note: I dont want parents map to be modified, therefore, I am creating copies 
        # of dictionary for them.
        # newChildMap contains first half rules from parent 1 and second half rules from second parent.
        newChildMap = dict(list(self.nonDeterministicRule2ndVar.items())[0:cutover])
        secondHalf = dict(list(secondParent.ruleFor2ndVariant.items())[cutover:length])

        # update the child map to append second half rules from second parent.
        newChildMap.update(secondHalf)
        # now mutate this child map slightly.
        newChildMap = self.mutate(newChildMap)

        return newChildMap

    """
     Randomly mutates a spot in the newly created childCA 2nd variant map.
     Mutates the child map's non-zero random value slightly to +2%.
    """
    def mutate(self,newChildCAMap):
        randomKey, randomVal = rand.choice(list(newChildCAMap.items()))
        
        # loop till we find non-zero value for a key in the map.
        while (randomVal == 0):
            randomKey, randomVal = rand.choice(list(newChildCAMap.items()))
        
        newChildCAMap[randomKey] = randomVal + 0.02
        return newChildCAMap

    """
     After a run, adds the fitness score to 2nd variant map of the CA
     to see how the second variant probability performs. Helpful in evolving
     the probabilities of second variant's map using GA.
    """
    def addFitnessToSecondVariantMap(self, fitnessScore):
        self.nonDeterministicRule2ndVar["fitness"] = fitnessScore

    """
    Private helper method for adding logic in iterate method to handle cases for using 2 variants of
    the disease.
    """
    def __UseBothRuleVariants(self, ruleKeyStr, centerOfKeyStr):
        # handle the case for both I and I' in the neighborhood of current cell, if they're then we randomly pick one probFunc.
        if ("I" in ruleKeyStr and "i" in ruleKeyStr):
            r = np.random.randint(0,2)
            # go to first variant map.
            if (r == 0):
                # since the ruleKeyStr is mixture of both I and i, the nonDeterministicRule1stVar map will never have this key
                # so, we need to first make sure that the centerCell is not i (otherwise, its obvious to use 2nd variant for this).
                if (not(centerOfKeyStr == "i")):
                    # immediately return if the center cell has recovered from any of both diseases, the probability is 
                    # always zeros if centerCell has recovered, no need to call __prob() function to get T/F.
                    if (centerOfKeyStr == "r" or centerOfKeyStr == "R"):
                        return centerOfKeyStr
                    
                    # Since we are looking up 1st variant map, we can ignore the ruleKeyStr containing i and r
                    # and replace them with S and R respectively because these have no effect on how 1st variant behaves.  
                    tempStr = ruleKeyStr.replace("i","S")
                    if ("r" in tempStr):
                        tempStr = tempStr.replace("r","R")

                    percent = self.nonDeterministicRule1stVar[tempStr]
                    # if probability satisfies and we can transition using 1st variant. Otherwise, we need to try transitioning from
                    # second variant by following the same procedure as done for 1st variant. If we also cannot transition
                    # from second variant, then we know we can return the same centerCell back.
                    if (self.__prob(percent)):
                        return self.transitionCellState(centerOfKeyStr, variant=1)
                    else:
                        # we already tried transitioning from I to R above (if centerOfKeyStr was I), but we couldn't, so, remain I.
                        if (centerOfKeyStr == "I"):
                            return centerOfKeyStr
                        
                        # same as above, looking at 2nd variant map, so, the str containing I and R has no effect on 2nd variant behavior.
                        tempStr = ruleKeyStr.replace("I","S")
                        if ("R" in tempStr):
                            tempStr = tempStr.replace("R","r")
                
                        percent = self.nonDeterministicRule2ndVar[tempStr]
                        if (self.__prob(percent)):
                            return self.transitionCellState(centerOfKeyStr, variant=2)
                        else:
                            return centerOfKeyStr
                else:
                    # the centerCell is i, so, we have to use 2nd variant map. If we cannot transition, we return the same centerCell.
                    tempStr = ruleKeyStr.replace("I","S")
                    if ("R" in tempStr):
                        tempStr = tempStr.replace("R","r")
                    
                    percent = self.nonDeterministicRule2ndVar[tempStr]
                    if (self.__prob(percent)):
                        return self.transitionCellState(centerOfKeyStr,variant=2)
                    else:
                        return centerOfKeyStr
            # go to second variant map.
            elif (r == 1):
                # same steps as r = 0 but in reverse order.
                if (not(centerOfKeyStr == "I")):
                    if (centerOfKeyStr == "r" or centerOfKeyStr == "R"):
                        return centerOfKeyStr

                    tempStr = ruleKeyStr.replace("I","S")
                    if ("R" in tempStr):
                        tempStr = tempStr.replace("R","r")

                    percent = self.nonDeterministicRule2ndVar[tempStr]
                    if (self.__prob(percent)):
                        return self.transitionCellState(centerOfKeyStr, variant=2)
                    else:
                        if (centerOfKeyStr == "i"):
                            return centerOfKeyStr
                        
                        tempStr = ruleKeyStr.replace("i","S")
                        if ("r" in tempStr):
                            tempStr = tempStr.replace("r","R")
                        percent = self.nonDeterministicRule1stVar[tempStr]
                        
                        if (self.__prob(percent)):
                            return self.transitionCellState(centerOfKeyStr, variant=1)
                        else:
                            return centerOfKeyStr
                else:
                    tempStr = ruleKeyStr.replace("i","S")
                    if ("r" in tempStr):
                        tempStr = tempStr.replace("r","R")
                    percent = self.nonDeterministicRule1stVar[tempStr]
                    if (self.__prob(percent)):
                        return self.transitionCellState(centerOfKeyStr,variant=1)
                    else:
                        return centerOfKeyStr

        # handle the case where only I is in neighborhood and not I' (goto first variant map)
        elif("I" in ruleKeyStr and not("i" in ruleKeyStr)):
            if (centerOfKeyStr == "r" or centerOfKeyStr == "R"):
                return centerOfKeyStr
            if ("r" in ruleKeyStr):
                ruleKeyStr = ruleKeyStr.replace("r", "R")

            percent = self.nonDeterministicRule1stVar[ruleKeyStr]
            # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
            if (self.__prob(percent)):
                return self.transitionCellState(centerOfKeyStr, variant=1)
            else:
                return centerOfKeyStr

        # handle the case where only I' is in neighborhood and not I (goto second variant map)
        elif("i" in ruleKeyStr and not("I" in ruleKeyStr)):
            if (centerOfKeyStr == "r" or centerOfKeyStr == "R"):
                return centerOfKeyStr
            if ("R" in ruleKeyStr):
                ruleKeyStr = ruleKeyStr.replace("R", "r")

            percent = self.nonDeterministicRule2ndVar[ruleKeyStr]
            # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
            if (self.__prob(percent)):
                return self.transitionCellState(centerOfKeyStr, variant=2)
            else:
                return centerOfKeyStr                                

        # else there are no I and I' in the neighborhood, the centerCell is either surrounded by all SSS..,
        # or the cells have recovered (R or r for both variants).
        else:
            return centerOfKeyStr

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
        rows = CABoard._board_row
        cols = CABoard._board_col
        # next board to be (after an iteration).
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
                        next[r][c] = self.__UseBothRuleVariants(ruleKeyStr, centerOfKeyStr)
                    else:
                        # only use 1st variant non-determinsitc rule. 
                        if (ruleKeyStr in self.nonDeterministicRule1stVar):
                            percent = self.nonDeterministicRule1stVar[ruleKeyStr]
                            # check the probability to transition. If % is 0 then we dont change the state, we keep the same centerCell.
                            if (self.__prob(percent)):
                                next[r][c] = self.transitionCellState(centerOfKeyStr, variant=1)
                            else:
                                next[r][c] = centerOfKeyStr
                        else:
                            print("This 1st variant non-deterministic ruleKey doesn't exist yet: " + ruleKeyStr + ". Are you using a randomBoard which uses both 1st and 2nd variant of disease but CA uses only 1st variant?")
                else:
                    # Use deterministic rules for 1st variant.
                    # Check now whether a key is already in dictionary (it should always
                    # be because we accounted all possibilities for each cell).
                    if (ruleKeyStr in self.deterministicRule1stVar):
                        next[r][c] = self.deterministicRule1stVar[ruleKeyStr]
                    else:
                        print("This determinstic ruleKey doesn't exist yet: " + ruleKeyStr)
        
        # after one iteration, we now have next board.
        self.nextBoard = self.createNextBoard(next)
        self.currentBoard.setBoard(self.nextBoard.getBoard())
        
        return self.nextBoard
   