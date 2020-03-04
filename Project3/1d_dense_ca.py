# This Project utilizes Processing p5 library. 
# API and setup instructions: https://p5.readthedocs.io/en/latest/install.html#prerequisites-python
# 
# In this project I will attempt to replicate Mitchels 1d density GA cellular automota
# it will converge to either all 1's or all 0's based on if the inititial 
# condition has a greater density of 1's or 0'sin the case of this application 
# 1's will be rendered as black and 0's will be rendered as white

###
### I have made this a class that can be used different ways.
###
### 1. we can turn on graphics by using named parameter graphics = True the default is false
### 2? we can input a rule bits that is used to determin the number of cells being analyzed
### 3 must give an initial rule mapping or a random one will be generated.
### 4. initial condition or  one will be generated.
import numpy as np
from p5 import *
from random import randint


class CaOneDDense:

    #class variables get defined here  this is like a static class variable in java
    _input_len:int = 201 #must be odd to force there to be a majority density
    _iter_size:int = 201
    #define CaOneDDenseconstructor
    def __init__(self, rule_bits:int = 7, rules:{int:str} = {},  input = []):
        #instance variables need to be defined here
        self.rule_bits = rule_bits
        self.current_iter = 0

        #take care of the rules
        #if default is used or input is not correct length
        if(len(rules) != (2**self.rule_bits)-1):
            self.build_rules()
        #elif the dictionary is not the correct types generate default
        elif (set(map(type,rules.keys()))!={int}) or (set(map(type,rules.values()))!={str}):
            self.build_rules()
        else:
            print("the rules were good!")
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
        print("iteration completed")
 

def setup():
    size(CaOneDDense._input_len*4,CaOneDDense._iter_size*4)
    no_stroke()



def draw():

    # print(CaOneDDense._init_cond_len)
    for i in range(0,CaOneDDense._input_len):
        if ca.input[i]=='0':
            fill(0)
        else:
            fill(255)
        square((i*4,ca.current_iter*4),4)

    ca.iterate_once()
    if ca.current_iter >= ca._iter_size:
        no_loop()



ca = CaOneDDense()
ca.iterate_all()
# run()
