from spike import *
from neutral_network import *
import random

class SpikeDataCollector:

    def __init__(self, pop_size=100,b = 10):
        self.pop_size = 100
        self.b = 10
        self.total_dead = 0
        # self.average_mutations_dead = []
        self.average_mutations_completed = []
        self.total_completed = 0
        self.max_SARS_mutation = 0
        self.min_SARS_mutation = 0
        self.b_indices = []
        self.total_mutations = 0
        self.dead_overflow = 0
        # self.SARS = None

        # fill up a population with covid-19 spikes
        self.population = [Spike() for x in range(pop_size)]
    
    def collectData(self):

        for x in range(self.b):
            self.b_indices.append(random.randint(0,self.pop_size-1))

        # keep mutating until a SARS varient has been found
        while self.total_completed <10:
            # loop over every population
            for i in range(self.pop_size):
                self.population[i].mutate()
                # check to see if the new version is not neutral
                if(not isGenomeNeutral(self.population[i].getAminoAcids())):
                    # if it isnt only keep it around IF the i is in b_indices
                    if((not self.b_indices.__contains__(i)) or shouldDie(self.population[i].getAminoAcids())):
                        self.population[i] = Spike()
                        dead_before = self.total_dead
                        self.total_dead += 1
                        if self.total_dead< dead_before:
                            self.dead_overflow += 1
                            print("DEAD OVERFLOWED: " + str(self.dead_overflow) )

                if(isSARS(self.population[i].getAminoAcids())):
                    hist_size = len(self.population[i].history)
                    self.average_mutations_completed.append(hist_size)
                    self.max_SARS_mutation = max(self.max_SARS_mutation, hist_size)
                    self.min_SARS_mutation = min(self.min_SARS_mutation, hist_size)
                    self.total_completed += 1
                    self.population[i] = Spike()


            self.total_mutations += 1

        print("complete")



sdc = SpikeDataCollector(b=0)
sdc.collectData()