"""
Written by Siri Khalsa

The goal of this is create a population of covid-19 spikes
every iteration it will randomly mutate.
if the spike is still in the neutral network after the mutation it stays around
if it is no longer in the neutral network than the virus will die and a 
new covid-19 spike will be generated in its place

It will run till a number of SARS or other final virus is found. it will then 
output the statistics of the run.
"""
from spike import *
from neutral_network import *
import random
# import matplotlib.pyplot as plt 
# import networkx as nx
import numpy as np

class SpikeDataCollector:
    

    def __init__(self, pop_size=100,b = 10):
        self.pop_size = pop_size
        self.b = b
        self.total_dead = 0
        self.average_mutations_dead = [] # this will be a list of histories of dead
        self.average_mutations_completed = [] # list of numbers
        self.total_completed = 0 # how many are successfull at SARS
        self.max_SARS_mutation = 0 # this will keep track of a maximum mutation to get to sars
        self.min_SARS_mutation = -1 #this will keept rack of the minimum mutations need for a SARS
        self.b_indices = [] # this will keep track of the b indices that are note limited to neutral network
        self.total_mutations = 0 #used to count the number of iteratiosn/mutations performed in total
        self.dead_overflow = 0
        self.allSARS = []

        # fill up a population with covid-19 spikes
        self.population = [Spike() for x in range(pop_size)]
    
    def collectData(self):

        # set indices for b that dont die when they leave the neutral network
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
                        # only collect history of the first 50 as it killed my computer before 
                        if len(self.average_mutations_dead) < 1000:
                            self.average_mutations_dead.append(len(self.population[i].history)-1)
                        self.population[i] = Spike()
                        dead_before = self.total_dead
                        self.total_dead += 1
                        if self.total_dead< dead_before:
                            self.dead_overflow += 1
                            print("DEAD OVERFLOWED: " + str(self.dead_overflow) )
                # check to see if we found a sars variant
                if(isComplete(self.population[i].getAminoAcids())):
                    # lets place it somewhere in case we need to analyse later
                    self.allSARS = self.population[i]
                    # how many mutations did it take to become sars?
                    hist_size = len(self.population[i].history) - 1
                    # add it to a list to caculate average later
                    self.average_mutations_completed.append(hist_size)
                    # store the max mutations needed
                    self.max_SARS_mutation = max(self.max_SARS_mutation, hist_size)
                    # store the minimum
                    if( not self.min_SARS_mutation == -1):
                        self.min_SARS_mutation = min(self.min_SARS_mutation, hist_size)
                    else:
                        self.min_SARS_mutation = hist_size
                    self.total_completed += 1
                    print("found 1")
                    print("history: " + str(self.population[i].history))
                    self.population[i] = Spike()

            self.total_mutations += 1


        print("complete")
        print("The total dead variants: "+str(self.total_dead))
        print("Max mutations needed tto get to SARS: "+str(self.max_SARS_mutation))
        print("Min mutations needed tto get to SARS: "+str(self.min_SARS_mutation))
        print("Average mutations of the dead are: " + str(sum(self.average_mutations_dead)/len(self.average_mutations_dead)))
        print("The Average mutation needed per sars: " + str(sum(self.average_mutations_completed)/self.total_completed))

    # def generatePlots(self):
    #     # first lets generate the bar graphs
    #     bar1 = plt.figure()
    #     xdata = ["SARS", "DEAD"]
    #     ydata = [self.total_completed,self.total_dead]
    #     plt.bar(ydata, xdata, align='center', alpha=0.5)
    #     plt.xticks(xdata)
    #     plt.ylabel('Total Varients')
    #     plt.title('Total Variants Mutating \n from \n COVID-19 Spike')
        
    #     bar2 = plt.figure()
    #     plt.show()



sdc = SpikeDataCollector(b=0)
sdc.collectData()
# sdc.generatePlots()