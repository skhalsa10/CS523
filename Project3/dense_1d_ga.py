# This is the Genetic Algorithm for the 1d density CA
#
# The goal is  to make a population of CAs and evolve a ruleset that outputs all one color representing the most dense
from dense_1d_ca import CaOneDDense
import ca_inputs
from random import *
import copy

class Ga1DCA:
    _pop_size = 100
    # lets keep track of the rules
    

    def  __init__(self):
        # build a population with random rules 
        self.init_pop()
        self.all_rules = []
        self.testr = {}

    ### this will build a population of size Ga1DCA._pop_size 
    ### with a random rules and ca_inputs.dense_0 input
    def init_pop(self):
        self.pop = []
        for i in range(0,Ga1DCA._pop_size):
            self.pop.append(CaOneDDense(input=ca_inputs.dense_0))


    def run_one_gen(self):
        for p in self.pop:
            self.run_all_input(p)
            # print("total fitness ", p.fitness)
        
        self.build_next_pop()

            
    def run_all_input(self, ca:CaOneDDense):
        # run all majority 0 input
        for input_0 in ca_inputs.dense_0_75:

            ca.new_input(input_0)
            ca.reset_Iter_Count()
            ca.iterate_all()
            self.calculate_fitness(ca,'0')
        # run all majority 1
        for input_1 in ca_inputs.dense_1_75:
            ca.new_input(input_1)
            ca.reset_Iter_Count()
            ca.iterate_all()
            self.calculate_fitness(ca,'1')
        #get an average fitness
        den = len(ca_inputs.dense_0_75)+len(ca_inputs.dense_1_75)
        ca.rules['fitness'] = int(ca.rules['fitness']/den)

        # ca.new_input(ca_inputs.dense_0)
        # ca.reset_Iter_Count()
        # ca.iterate_all()
        # self.calculate_fitness(ca,'0')
        # ca.new_input(ca_inputs.dense_1)
        # ca.reset_Iter_Count()
        # ca.iterate_all()
        # self.calculate_fitness(ca,'1')
        # ca.average_fitness(2)

    def calculate_fitness(self, ca:CaOneDDense, majority:str):
        fitness = ca.input.count(majority)
        # print(fitness)
        ca.add_fitness(fitness)

    def build_next_pop(self):
        self.all_rules = []
        temp = []
        # lets first extract the rules from all CAs
        for ca in self.pop:
            temp.append(ca.get_rules_copy())

        # sort all the rules based on fitness
        # self.all_rules.sort(key = lambda x: x['fitness'], reverse = True)
        self.all_rules = sorted(temp, key=lambda x: x['fitness'], reverse = True)
        

        print("the highest fitness is from pop after sort ", self.all_rules[0]['fitness'])
        # we will keep the best 20 and fill out the rest with modified rules
        for i in range(20,Ga1DCA._pop_size):
            # create a new rule set using crossover
            new_rule = self.get_crossover_rule(self.all_rules)
            new_rule = self.mutate_rule(new_rule, randint(1,3))

            self.all_rules[i] = new_rule

        # now lets add these rules  into the pop
        # print(self.all_rules[0])
        # for r in self.all_rules:
        #     print("fitness: ", r['fitness'])
        # print(self.all_rules)

        for i in range(0,self._pop_size):
            self.pop[i].new_rules(self.all_rules[i])
        
    
        


    def mutate_rule(self,new_rule, m):
        # have to get rid of one that contains the 'fitness' key
        length = len(new_rule)-1
        while m != 0:
            i = randint(1,length-1)
            if new_rule[i] == '0':
                new_rule[i] = '1'
            else:
                new_rule[i] = '0'

            m -= 1

        return new_rule

    def get_crossover_rule(self, all_rules):
        # get two elites from first 20
        p1_rule = copy.deepcopy(all_rules[randint(0,19)])
        p2_rule = copy.deepcopy(all_rules[randint(0,19)])

        length = len(p1_rule)-1
        cutover = randint(0,length-1)
        new_rules = copy.deepcopy(p1_rule)
        #p1_rule on left and p2_rule on right
        for i in range(cutover,length):
            new_rules[i] = copy.deepcopy(p2_rule[i])

        return new_rules



    def run_many_gen(self):
        for i in range(0,7):
           self.run_one_gen() 

    
test = Ga1DCA()
test.run_many_gen()

