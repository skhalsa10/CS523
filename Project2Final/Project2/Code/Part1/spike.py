"""
The program was written by Siri. 
It encapsulates a 5 amino acid spike protein.
It can be initialized to any combination but the default
is the covid-19 spike given in the project handout.
"""

from genetic_code import *
import random
import copy

"""
This class encapsulates a spike protein. it contains a 15 nucleotide RNA strand of bases.
It will also keep track of the genome mappings as will with a 5 letter string as amino acids
"""
class Spike:
    def __init__(self, amino_Acids = "LFQQN"):

        if(len(amino_Acids) != 5):
            raise AssertionError
        else:
            self.__amino_Acids = amino_Acids

        self.__RNA_Strand = self.__buildRNAStrand(self.__amino_Acids)

        if(len(self.__RNA_Strand) != 15):
            raise AssertionError

        self.history = [(copy.deepcopy(self.__RNA_Strand),copy.deepcopy(self.__amino_Acids))]

    """
    This function Will build a random RNA string that satisfies the the genetic code inside the Amino_Acids
    for example is the Amino Acid was Y it will randomly pick  'uac' or 'uau'
    """
    def __buildRNAStrand(self, amino_acids):
        RNA_to_return = ""
        for a in amino_acids:
            RNA_to_return += self.__randomCodonFromAcid(a)
        return RNA_to_return

    """
    This function will pick a random codon that maps to the amino acid given as an argument.
    """
    def __randomCodonFromAcid(self, acid):
        codons = amino_acid_codons[acid.upper()]
        # pick a random codon from the list that codes the amino acid
        codon = codons[random.randint(0,len(codons)-1)]
        return codon

    """
    pick a random nucleotide and mutate the base to 1 of the 3 remaining bases.
    update the Amino_acids to reflect the new genome.
    """
    def mutate(self):
        # first mutate a random position
        mutation_index = random.randint(0,len(self.__RNA_Strand)-1)

        current_base_at_index  = self.__RNA_Strand[mutation_index]
        new_base = copy.deepcopy(current_base_at_index)
        while(new_base == current_base_at_index):
            new_base = bases[random.randint(0,len(bases)-1)]
        self.__RNA_Strand = self.__RNA_Strand[:mutation_index] +new_base+self.__RNA_Strand[mutation_index+1:] 
        # now recode the acid for that location
        amino_acids_index = int(mutation_index/3)

        codon = self.buildCodonFromIndex(amino_acids_index*3)
        self.__amino_Acids = self.__amino_Acids[:amino_acids_index]+genetic_code[codon]+self.__amino_Acids[amino_acids_index+1:]
        self.history.append((copy.deepcopy(self.__RNA_Strand),copy.deepcopy(self.__amino_Acids)))

    """
    this will take 3 nucleotids starting at index i and return a codon.
    It assumes that there are 3 consecutive codons in a rom starting at i.
    """
    def buildCodonFromIndex(self, i):
        codon = ""
        codon += copy.deepcopy(self.__RNA_Strand[i])
        codon += copy.deepcopy(self.__RNA_Strand[i+1])
        codon += copy.deepcopy(self.__RNA_Strand[i+2])
        return codon
    
    """
    print all 15 nucleotides as a string
    """
    def printRNA(self):
        print("RNA Strand : " + self.__RNA_Strand)

    """
    Prints the 5 amino acids as a string
    """
    def printAminoAcids(self):
        print("Amino Acids : " + self.__amino_Acids)
    
    """
    Returns the 5 amino acids as a string
    """
    def getAminoAcids(self):
        return copy.deepcopy(self.__amino_Acids)

