from spike import *
from neutral_network import *
import random

pop_size = 100
b = 20
total_dead = 0
average_mutations_dead = 0
average_mutations_completed = 0
total_completed = 0
max_hist = 0
b_indices = []
total_mutations = 0
total_overflow = 0
SARS = None

# fill up a population with covid-19 spikes
population = [Spike() for x in range(pop_size)]

for x in range(b):
    b_indices.append(random.randint(0,pop_size-1))

# keep mutating until a SARS varient has been found
while total_completed == 0:
    # loop over every population
    for i in range(100):
        population[i].mutate()
        # check to see if the new version is not neutral
        if(not isGenomeNeutral(population[i].getAminoAcids())):
            # if it isnt only keep it around IF the i is in b_indices
            if(not b_indices.__contains__(i)):
                population[i] = Spike()
                total_dead += 1

        if(isSARS(population[i].getAminoAcids())):
            SARS = population[i]
            total_completed += 1

        print(population[i].getAminoAcids())


    total_mutations += 1

SARS.printAminoAcids()
SARS.printRNA()
print("total history " + str(SARS.history))
print("Total mutations of the SARS variant: " + len(SARS.history))
print("Total dead variants: "+ str(total_dead))