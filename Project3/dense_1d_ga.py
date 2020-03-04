# This is the Genetic Algorithm for the 1d density CA
#
# The goal is  to make a population of CAs and evolve a ruleset that outputs all one color representing the most dense
from dense_1d_ca import CaOneDDense
import ca_inputs
from random import *

class Ga1DCA:
    _pop_size = 100

    def  __init__(self):
        # build a population with random rules 
        self.init_pop()

    ### this will build a population of size Ga1DCA._pop_size 
    ### with a random rules and ca_inputs.dense_0 input
    def init_pop(self):
        self.pop = []
        for i in range(0,Ga1DCA._pop_size):
            self.pop.append(CaOneDDense(input=ca_inputs.dense_0))

    ### this will loop over the population
    ### run with dense_0 input calculate the fitness
    ### run a second time with dense_1 add this fitness calculation
    ### most elite N of pop is copied to next population and P-N of the population
    ### is created with crossovers of original population with m mutations
    def run_one_gen(self):
        for p in self.pop:
            self.run_all_input(p)
            # print("total fitness ", p.fitness)
        
        self.build_next_pop()
        for p in self.pop:
            p.reset_fitness()
            
    def run_all_input(self, ca:CaOneDDense):
        # run all majority 0 input
        for input_0 in ca_inputs.dense_0_75:

            ca.new_input(input_0)
            ca.reset_Iter_Count()
            ca.iterate_all()
            self.calculate_fitness(ca,'0')
        
        for input_1 in ca_inputs.dense_1_75:
            ca.new_input(input_1)
            ca.reset_Iter_Count()
            ca.iterate_all()
            self.calculate_fitness(ca,'1')
        #get an average fitness
        den = len(ca_inputs.dense_0_75)+len(ca_inputs.dense_1_75)
        ca.fitness = int(ca.fitness/den)

    def calculate_fitness(self, ca:CaOneDDense, majority:str):
        fitness = ca.input.count(majority)
        # print(fitness)
        ca.add_fitness(fitness)

    def build_next_pop(self):
        self.pop.sort(key = lambda x: x.fitness, reverse = True)
        print("the highest fitness is ", self.pop[0].fitness)

        print("the lowest fitness is ", self.pop[-1].fitness)
        temp_pop = []

        # copy 20 best fitness
        for i in range(0,20):
             temp_pop.append(self.pop[i])

        # I will modify pop in place dont touch first 20 
        # this copies the best 20 to the next generation
        for i in range(20,Ga1DCA._pop_size):
            # create a new rule set using crossover
            new_rule = self.get_crossover_rule()
            new_rule = self.mutate_rule(new_rule, randint(1,3))
            temp_pop.append(self.pop[i])
            # print(self.pop[i].rules == new_rule)
            temp_pop[i].new_rules(new_rule)


    def mutate_rule(self,new_rule, m):
        length = len(new_rule)
        while m != 0:
            i = randint(0,length-1)
            if new_rule[i] == '0':
                new_rule[i] = '1'
            else:
                new_rule[i] = '0'

            m -= 1

        return new_rule

    def get_crossover_rule(self):
        # get two elites from first 20
        p1_rule = self.pop[randint(0,20)].rules.copy()
        p2_rule = self.pop[randint(0,20)].rules.copy()

        length = len(p1_rule)
        cutover = randint(0,length-1)
        new_rules = p1_rule.copy()
        #p1_rule on left and p2_rule on right
        for i in range(cutover,length):
            new_rules[i] = p2_rule[i]

        return new_rules



    def run_many_gen(self):
        for i in range(0,5):
           self.run_one_gen() 

    
test = Ga1DCA()
test.run_many_gen()

