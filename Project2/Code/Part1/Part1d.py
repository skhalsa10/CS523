from spike import *
from neutral_network import *
import random


b = 10
total_dead = 0
average_mutations_dead = 0
average_mutations_completed = 0
total_completed = 0
max_hist = 0
non_neutral_indices = []
total_mutations = 0
total_overflow = 0

population = [Spike() for x in range(100)]

while total_completed == 0:
    for i in range(100):
        population[i].mutate()
        if(not isGenomeNeutral(population[i].getAminoAcids())):
            non_neutral_indices.append(i)
        hist = len(population[i].history)
        max_hist = max(max_hist,hist)
        if(isSARS(population[i].getAminoAcids())):
            total_completed += 1

    to_remove = len(non_neutral_indices)-b
    while(to_remove>0):
        # pick a random index to kill a nonneutral
        index_To_Pop = random.randint(0,to_remove+(b-1))
        index = non_neutral_indices.pop(index_To_Pop)
        # now set population at this index to a new spike
        population[index] = Spike()
        overflow_test = total_dead
        total_dead += 1
        if total_dead<overflow_test:
            total_overflow += 1
        to_remove -= 1
    # print(total_dead)
    total_mutations += 1

print("total mutations needed to get sars " + str(total_mutations))
print("total dead viruses " + str(total_dead))
print("dead integer overflow " + str(total_overflow))