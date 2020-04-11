"""
Written by siri Khalsa

This is a simple script to build a graph needed for part 1b
"""
import numpy as np
import matplotlib.pyplot as plt
from Part1a import *

n=15
mutations_away = range(0,16)
genome_count_at_k_away = list(range(0,16))

for k in mutations_away:
    genome_count_at_k_away[k] = calc_K_Mutations_Away(k,n)

plt.yscale('log')
plt.plot(mutations_away, genome_count_at_k_away, label = "number of total genomes k mutations away")
plt.xlabel("k", fontsize='x-large')
plt.ylabel("Number of unique genomes", fontsize='x-large')
plt.title("Number of Genomes k Mutations Away from Original. \n For a genome with 15 nucleotides", fontsize='x-large')

plt.show()