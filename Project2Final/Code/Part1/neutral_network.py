"""
This module class thing can be used as a utility class to confirm that a genome falls
into the defined  neutral network in this file

It defines two neutral networks.

one is used for sars in part 1d

the other is a neutral network for 1e

please uncomment the one you want to run.

Written by Siri
"""



# UNCOMMENT THIS TO CHECK FOR SARS must comment the bat below
# complete = 'YLNYT'
# pos0 = ['L','Y','F','Q','H']
# pos1 = ['F', 'L']
# pos2 = ['Q','N','K','H']
# pos3 = ['Q', 'Y','H','N']
# pos4 = ['N','S','T']

# Uncomment this to check for BAT CORONA must comment the sars above
complete = 'LLYYD'
pos0 = ['L']
pos1 = ['F', 'L']
pos2 = ['Q','H', 'Y']
pos3 = ['Q','H','L','Y']
pos4 = ['N','D']

"""
this build every possible genome in the defined neutral network
"""
neutral_genomes = [a+b+c+d+e for a in pos0 for b in pos1 for c in pos2 for d in pos3 for e in pos4]

"""
this will return true if a stop codon exists anywhere
"""
def shouldDie(genome):
    return genome.__contains__('*')

"""
will return true or false if the input is in the defined neutral network
"""
def isGenomeNeutral(genome):
    return neutral_genomes.__contains__(genome)

"""
This will return true or false if the input is equal to the completed mutation
"""
def isComplete(genome):
    return genome == complete

