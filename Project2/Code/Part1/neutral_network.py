"""
This module class thing can be used as a utility class to confirm that a genome falls
into the defined  neutral network in this file
"""



# UNCOMMENT THIS TO CHECK FOR SARS must comment the bat below
# complete = 'YLNYT'
# pos0 = ['L','Y','F','Q','H']
# pos1 = ['F', 'L']
# pos2 = ['Q','N','K','H']
# pos3 = ['Q', 'Y','H','N']
# pos4 = ['N','S','T']

# Uncooment this to check for BAT CORONA must comment the sars above
complete = 'WPRFA'
pos0 = ['L','S','W']
pos1 = ['F', 'L', 'S','P']
pos2 = ['Q','H', 'R']
pos3 = ['Q','H','L','Y','F']
pos4 = ['N','D','T','A']

neutral_genomes = [a+b+c+d+e for a in pos0 for b in pos1 for c in pos2 for d in pos3 for e in pos4]

def shouldDie(genome):
    return genome.__contains__('*')


def isGenomeNeutral(genome):
    return neutral_genomes.__contains__(genome)

def isComplete(genome):
    return genome == complete

