"""
Written by Siri Khalsa
Maps out the genetic code with codons to amino acids.
"""

"""
This is a list of the possible bases
"""
bases = ['a','g','c','u']

"""
This is a list of all possible codons
"""
codons = [a + b + c for a in bases for b in bases for c in bases ] 

"""
Here is a map of the gentic code from codon -> Amino Acid.
This is the Wheel from the assignment.
for example:
genetic_code['cua'] -> L
"""
genetic_code = {
    'aaa': 'K',
    'aag': 'K',
    'aac': 'N',
    'aau': 'N',
    'aga': 'R',
    'agg': 'R',
    'agc': 'S',
    'agu': 'S',
    'aca': 'T',
    'acg': 'T',
    'acc': 'T',
    'acu': 'T',
    'aua': 'I',
    'aug': 'M',
    'auc': 'I',
    'auu': 'I',
    'gaa': 'E',
    'gag': 'E',
    'gac': 'D',
    'gau': 'D',
    'gga': 'G',
    'ggg': 'G',
    'ggc': 'G',
    'ggu': 'G',
    'gca': 'A',
    'gcg': 'A',
    'gcc': 'A',
    'gcu': 'A',
    'gua': 'V',
    'gug': 'V',
    'guc': 'V',
    'guu': 'V',
    'caa': 'Q',
    'cag': 'Q',
    'cac': 'H',
    'cau': 'H',
    'cga': 'R',
    'cgg': 'R',
    'cgc': 'R',
    'cgu': 'R',
    'cca': 'P',
    'ccg': 'P',
    'ccc': 'P',
    'ccu': 'P',
    'cua': 'L',
    'cug': 'L',
    'cuc': 'L',
    'cuu': 'L',
    'uaa': '*',
    'uag': '*',
    'uac': 'Y',
    'uau': 'Y',
    'uga': '*',
    'ugg': 'W',
    'ugc': 'C',
    'ugu': 'C',
    'uca': 'S',
    'ucg': 'S',
    'ucc': 'S',
    'ucu': 'S',
    'uua': 'L',
    'uug': 'L',
    'uuc': 'F',
    'uuu': 'F'
}


"""
Here we have a map of amino acids to a list of codons that code for them.
For example print(amino_acid_codons['S']) -> ['agc', 'agu', 'uca', 'ucg', 'ucc', 'ucu']
"""
amino_acid_codons = {
    'P': [],
    'S': [],
    'M': [],
    'Y': [],
    'I': [],
    'H': [],
    '*': [],
    'E': [],
    'G': [],
    'T': [],
    'W': [],
    'N': [],
    'F': [],
    'L': [],
    'D': [],
    'Q': [],
    'V': [],
    'R': [],
    'C': [],
    'K': [],
    'A': []
}

for key, value in genetic_code.items():
    amino_acid_codons[value].append(key)

print(amino_acid_codons['S'])