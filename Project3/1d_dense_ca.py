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

class CaOneDDense:

    #class variables get defined here  this is like a static class variable in java

    #define CaOneDDenseconstructor
    def __init__(self, rule_bits=7, rule:{str:int} = {},graphics = False):
        #instance variables need to be defined here
        self.graphics = graphics
        self.rule_bits = rule_bits

        #if default generate the rule dictionary
        #elif the dictionary is not the correct types generate default
        # otherwise we can use the input
        if(rule=={}):
            #TODO generate rules mapping
            pass
        elif (set(map(type,rule.keys()))!={str}) or (set(map(type,rule.values()))!={int}):
            print("wrong types")
            self.build_rules()
        else:
            print("passed")
    
    def build_rules(self)->{str:int}:
        print("BUILDING RULES ", self.rule_bits)
        


ca = CaOneDDense(rule={7:6})

print(bin(64))