"""
 This is a Genetic Algorithm (GA) implementation to evolve the transition
 probabilities for 2d Cellular Automata (CA) which uses SIR dynamics for the
 spread of epidemics called Coronavirus (Covid-19). 
 This GA model tries to evolve 2nd variant of the disease spread and its transition probabilities.

 Implemented by: Anas Gauba
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
        randomBoard = CABoard(isBoardRandom=True)

        for _ in range(0,GeneticAlgorithm2DCA._popSize):
            self.popCA.append(CA2dSIRDeterministicDynamics(randomBoard))
    

