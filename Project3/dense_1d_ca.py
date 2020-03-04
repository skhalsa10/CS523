# This Project utilizes Processing p5 library. 
# API and setup instructions: https://p5.readthedocs.io/en/latest/install.html#prerequisites-python
# 
# In this project I will attempt to replicate Mitchels 1d density GA cellular automota
# it will converge to either all 1's or all 0's based on if the inititial 
# condition has a greater density of 1's or 0'sin the case of this application 
# 1's will be rendered as black and 0's will be rendered as white


import numpy as np
from random import randint
import ca_inputs


class CaOneDDense:

    #class variables get defined here  this is like a static class variable in java
    _input_len:int = 201 #must be odd to force there to be a majority density
    _iter_size:int = 201
    #define CaOneDDenseconstructor
    def __init__(self, rule_bits:int = 7, rules:{int:str} = {},  input = []):
        #instance variables need to be defined here
        self.rule_bits = rule_bits
        self.current_iter = 0
        self.fitness = 0

        #take care of the rules
        #if default is used or input is not correct length
        if(len(rules) != (2**self.rule_bits)):
            self.build_rules()
        #elif the dictionary is not the correct types generate default
        elif (set(map(type,rules.keys()))!={int}) or (set(map(type,rules.values()))!={str}):
            self.build_rules()
        else:
            self.rules = rules
    
        #Take care of the initial condition
        if len(input)!= CaOneDDense._input_len:
            self.build_input()
        #force type to be string
        elif set(map(type,input)) != {str}:
            self.build_input()
        else:
            self.input = input
        
        self.next_input = self.input.copy()

    ### This function will generate a random rule mapping###
    def build_rules(self)->{int:str}:
        self.rules = {}
        for i in range(0,(2**self.rule_bits)):
            self.rules[i] = str(randint(0,1))

    ### This function will generate a random initial conditionit status
    def build_input(self)->[str]:
        self.input = []
        for i in range(0,CaOneDDense._input_len):
            self.input.append(str(randint(0,1)))

    ###This will iterate once through the CA - useful for animating graphics###
    def iterate_once(self):
        if(self.current_iter> CaOneDDense._iter_size):
            print("all iterations complete")
        
        left_bound = -int(self.rule_bits/2)
        right_bound = self.rule_bits-int(self.rule_bits/2)

        for i in (range(0,CaOneDDense._input_len)):
            bit_Pattern = "0b"
            for j in range(left_bound,right_bound):
                bit_Pattern += self.input[(i+j)%CaOneDDense._input_len]

            self.next_input[i] = self.rules[int(bit_Pattern,2)]

        temp = self.input
        self.input = self.next_input
        self.next_input = temp

        self.current_iter += 1


    ### This will iterate the CA for _iter_size  - used when not needing to animate ###
    def iterate_all(self):
        while self.current_iter <= CaOneDDense._iter_size:
            self.iterate_once()
        
    
    def new_input(self, input):
        
        if len(input)!= CaOneDDense._input_len:
            raise ValueError
        #force type to be string
        elif set(map(type,input)) != {str}:
            raise TypeError
        else:
            self.input = input
    
    def new_rules(self, rules):
        if(len(rules) != (2**self.rule_bits)):
            raise ValueError
        #elif the dictionary is not the correct types generate default
        elif (set(map(type,rules.keys()))!={int}) or (set(map(type,rules.values()))!={str}):
            raise TypeError
        else:
            self.rules = rules

    def reset_Iter_Count(self):
        self.current_iter = 0
    
    def add_fitness(self, fitness):
        self.fitness += fitness

    def reset_fitness(self):
        self.fitness = 0
 


