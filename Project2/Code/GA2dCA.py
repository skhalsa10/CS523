"""
 This is a Genetic Algorithm (GA) implementation to evolve the transition
 probabilities for 2d Cellular Automata (CA) which uses SIR dynamics for the
 spread of epidemics called Coronavirus (Covid-19). 
 This GA model tries to evolve 2nd variant of the disease spread and its transition probabilities
 by making sure the probability map of 2ndVariant evolves and coexist equally with
 1stvariantMap. 

 Implemented by: Anas Gauba
"""

from CA2dSIRDynamics import CA2dSIRDynamics
from CABoard import CABoard
import random as rand

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
            self.popCA.append(CA2dSIRDynamics(randomBoard,diseaseVariants=2,ruleTypeIsDeterministic=False))
            #print(self.popCA[i].getSecondVariantMap())
     
    def buildNextPop(self):
        # sort CA's in increasing order of fitness.
        self.popCA = sorted(self.popCA, key=lambda x: x.ruleFor2ndVariant["fitness"])
        print("Fittest CA with lowest fitness: "+ str(self.popCA[0].ruleFor2ndVariant["fitness"]))

        # this list consists of all 100 CA's and their 2ndVariantProbabilityMaps.
        # we will pick the top 20 CA's based on the fitness of 2nd variant of the disease.
        nextPopCA = []

        # pick top 20% CA's who did reasonably well in previous generation than others to this 
        # nextPopCA list. 
        top20Percent = int((20*self._popSize)/100)
        nextPopCA.extend(self.popCA[:top20Percent])

        # Crossover any two of top 20% CA to produce children for the remaining 80 CA's
        for i in range(top20Percent,GeneticAlgorithm2DCA._popSize):
            randomTopCA1 = rand.randint(0,top20Percent-1)
            topParentCA1 = self.popCA[randomTopCA1]
            randomTopCA2 = rand.randint(0,top20Percent-1)
            topParentCA2 = self.popCA[randomTopCA2]

            while (randomTopCA1 == randomTopCA2):
                randomTopCA2 = rand.randint(0,top20Percent-1)
                topParentCA2 = self.popCA[randomTopCA2]

            childCA2ndVariantMap = topParentCA1.crossOver(topParentCA2)
            
            childCA = self.popCA[i]
            childCA.ruleFor2ndVariant = childCA2ndVariantMap
            
            nextPopCA.append(childCA)
        
        self.popCA = nextPopCA
        
        # for the next run, make the board be random for the whole CA population.
        for i in range(0, GeneticAlgorithm2DCA._popSize):
            self.popCA[i].currentBoard = CABoard(isBoardRandom=True)

    """
     After a run, count up R and r and see if they are equal, then the better fitness. 
     R - r (abs value, if the value is closer to zero, the better fitness)
    """
    def calculateFitness(self, ca):
        RCount = ca.currentBoard.__str__().count("R")
        rCount = ca.currentBoard.__str__().count("r")
        fitness = abs(RCount - rCount)
        print("Fitness: " + str(fitness))
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
                boardObj = ca.iterateCABoard()
                
            self.calculateFitness(ca)

        self.buildNextPop()

    """
     This runs generations of CA's until the best fitness is found for the probability
     map of 2nd disease. Sometimes, there can be false fitness of 0 in the initial run, so
     I am making sure that the GA atleast runs for 10 generations to eliminate any false 
     positives.
    """
    def runUntilBestSolution(self):
        i = 0
        while(True):
            self.runSimulation()

            if (self.popCA[0].ruleFor2ndVariant["fitness"] <= 5 and i >= 10):
                f = open("secondVariantRuleGA.py", "w")
                f.write("ruleFor2ndVariant = ")
                f.write(str(self.popCA[0].ruleFor2ndVariant))
                f.close()

                break
            
            i += 1


def main():
    GA = GeneticAlgorithm2DCA()
    GA.runUntilBestSolution()

if __name__ == '__main__':
    main()