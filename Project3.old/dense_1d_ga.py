# This is the Genetic Algorithm for the 1d density CA
#
# The goal is  to make a population of CAs and evolve a ruleset that outputs all one color representing the most dense
from dense_1d_ca import CaOneDDense
import ca_inputs
from random import *
import copy

class Ga1DCA:
    _pop_size = 100
    

    def  __init__(self):
        # build a population with random rules 
        self.init_pop()
        # I ended up extrancting the rules from the CA when debugging
        # this probably was not needed but I will keep  anyways
        self.all_rules = []


    ### this will build a population of size Ga1DCA._pop_size 
    ### with a random rules and ca_inputs.dense_0 input
    def init_pop(self):
        self.pop = []
        for i in range(0,Ga1DCA._pop_size):
            self.pop.append(CaOneDDense(input=ca_inputs.dense_0))

    ### this will run each population against 75 inputs where the majority is '0'
    ### and 75 inputs with a majority '1' it will average the fitness of each input
    ### it will select 20 high fitness and then the remaining 80 population
    ### will be creating using crossover and mutation
    def run_one_gen(self):
        for p in self.pop:
            self.run_all_input(p)
        
        self.build_next_pop()

    ### this will perform iterations on all inputs and fitness calculations  
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


    def calculate_fitness(self, ca:CaOneDDense, majority:str):
        fitness = ca.input.count(majority)
        # print(fitness)
        ca.add_fitness(fitness)

    ### this may be the most complicated
    def build_next_pop(self):
        #initialize list containing all rules and fitness
        self.all_rules = []
        #maybe no longer needed but added during 
        # debugging and will just keep I thought 
        # this sorting was broken and needed a temp to test
        temp = []
        # lets first extract the rules from all CAs
        for ca in self.pop:
            temp.append(ca.get_rules_copy())

        # sort all the rules based on fitness which is now a property of the rules
        self.all_rules = sorted(temp, key=lambda x: x['fitness'], reverse = True)
        

        print("the highest fitness is from pop after sort ", self.all_rules[0]['fitness'])
        print(self.all_rules[0])
        # we will keep the best 20 and fill out the rest with modified rules
        # we keep the best 20 by starting to replace the rules starting at index 20
        for i in range(20,Ga1DCA._pop_size):
            # create a new rule set using crossover
            new_rule = self.get_crossover_rule(self.all_rules)
            new_rule = self.mutate_rule(new_rule, randint(1,3))

            self.all_rules[i] = new_rule

        # update each population with new rule from the genetically modified one above
        for i in range(0,self._pop_size):
            self.pop[i].new_rules(self.all_rules[i])
        
    
        

    # this will mutate m rules
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

    # merge two parents togethor
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


    ### this will take forever the input is huge 
    ### change the range to be smaller if needed
    def run_many_gen(self):
        for i in range(0,10):
           self.run_one_gen()
        #    if we find a max fitness stop running
           if(self.all_rules[0]['fitness']==CaOneDDense._input_len):
               break 


# this can run. you may want to have python 
# enter interactive mode afterwords so you can collect the rule data
test = Ga1DCA()
test.run_many_gen()

