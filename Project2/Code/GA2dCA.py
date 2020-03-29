"""
 This is a Genetic Algorithm (GA) implementation to evolve the transition
 probabilities for 2d Cellular Automata (CA) which uses SIR dynamics for the
 spread of epidemics called Coronavirus (Covid-19). 
 This GA model tries to evolve 2nd variant of the disease spread and its transition probabilities.

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
            print(self.popCA[i].currentBoard)
    
    def buildNextPop(self):
        return

    def calculateFitness(self):
        return
    
    def mutate(self):
        return
    
    """
     This iterates when 
    """
    def runSimulation(self):


test = GeneticAlgorithm2DCA()