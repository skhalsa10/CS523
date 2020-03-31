"""
 This is a Genetic Algorithm (GA) implementation to evolve the transition
 probabilities for 2d Cellular Automata (CA) which uses SIR dynamics for the
 spread of epidemics called Coronavirus (Covid-19). 
 This GA model tries to evolve 2nd variant of the disease spread and its transition probabilities
 by making sure the probability map of 2ndVariant evolves and become equivalent to
 1stvariantMap. 

 Implemented by: Anas Gauba
"""

"""
GA:
1) Randomly initialize populations p of CA.
2) Determine fitness of population
3) Untill convergence repeat:
      a) Select parents from population
      b) Crossover and generate new population
      c) Perform mutation on new population
      d) Calculate fitness for new population
"""

from CA2dSIRDynamicsPart2a import CA2dSIRDeterministicDynamics
from CABoard import CABoard

class GeneticAlgorithm2DCA:
    # 100 populations of CA with initial board config.
    _popSize = 100

    def __init__(self):
        # build initial CA population with random inital boards which 
        # include both disease variants, I and I'.
        self.popCA = []

        # each CA has random board and both 1st variant and initially 2nd variant to random probability.
        for i in range(0,GeneticAlgorithm2DCA._popSize):
            randomBoard = CABoard(isBoardRandom=True)
            self.popCA.append(CA2dSIRDeterministicDynamics(randomBoard,diseaseVariants=2,ruleTypeIsDeterministic=False))
            #print(self.popCA[i].currentBoard)
    
    def buildNextPop(self):
        return
    
    def crossOverProbabilities(self):
        return

    def mutateProbability(self, childProbability):
        return
    
    """
     After a run, count up R and r and see if they are equal, then the better fitness. 
     R - r (abs value, if the value is closer to zero, the better fitness)
    """
    def calculateFitness(self, ca):
        RCount = ca.currentBoard.__str__().count("R")
        rCount = ca.currentBoard.__str__().count("r")
        fitness = abs(RCount - rCount)
        print(fitness)
        ca.addFitnessToSecondVariantMap(fitness)    

    """
     This performs one run for each of the 100 populations of CA.
     One run/simulation consists of iterating over CA board until there are
     no infected cells left both variants I and i. 
    """
    def runSimulation(self):
        for ca in self.popCA:
            boardObj = ca.currentBoard
            while ("I" in boardObj.__str__() or "i" in boardObj.__str__()):
                #print(boardObj)
                boardObj = ca.iterateCABoard()
                #print(boardObj)
            self.calculateFitness(ca)

        self.buildNextPop()


def main():
    GA = GeneticAlgorithm2DCA()
    GA.runSimulation()

if __name__ == '__main__':
    main()