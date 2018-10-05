#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 21:02:19 2018

@author: mario_hevia
"""

import numpy as np
from operator import xor
import heapq
import math

class OnePlusLambdaCommaLambdaSA:
    def __init__(self, problem, problem_size, not_used_0, 
                 offspring_size, not_used_1, not_used_2, 
                 offspring_update_factor):
        self.problem = problem
        self.problem_size = problem_size
        if offspring_size > problem_size:
            print('Initial offspring population size changed from',
                  offspring_size, 'to', problem_size)
        self.offspring_size = min(offspring_size, problem_size)
        self.offspring_update_factor = offspring_update_factor
        self.mutation_probability = self.offspring_size / self.problem_size
        self.crossover_probability = 1 / self.offspring_size
        bit_array = np.random.choice(['0', '1'], self.problem_size)
        self.bit_string = ''.join(bit_array)
        self.solved = False
        self.evaluations = 0
        self.generations = 0
        self.fit_gen = []
        self.lambda_gen = []
        self.mut_prob_gen = []
        
    def __next__(self):
        offspring = []
        self.parent = [self.problem.evaluate(self.bit_string), 
                        self.bit_string]
#        print('\n'+self.bit_string, self.problem.evaluate(self.bit_string)[0])
        self.mut_prob_gen.append(self.mutation_probability)
        self.lambda_gen.append(round(self.offspring_size))
        l = np.random.binomial(self.problem_size, self.mutation_probability)
        for i in range(round(self.offspring_size)):
            mutated_string = self.mutate(l)
            offspring.append((self.problem.evaluate(mutated_string), 
                              mutated_string))
            self.evaluations += 1
        fittest_mut = self.select_1(offspring)
#        print(fittest_mut, self.problem.evaluate(fittest_mut)[0])
        offspring = [] # ask if comment or not
        
        for i in range(round(self.offspring_size)):
            cross_string = self.crossover(fittest_mut)
            offspring.append((self.problem.evaluate(cross_string), 
                              cross_string))
            self.evaluations += 1
        self.select_2(offspring)
        self.generations += 1
        self.update()
        
    def mutate(self, l):
        mut_indexes = np.random.choice(self.problem_size, size = l,
                                       replace=False)
        mutated_list = [str(xor(int(bit), 1)) if i in mut_indexes else bit 
                        for i, bit in enumerate(self.bit_string)]
#        print(self.generations, '\n' + self.bit_string, '\n' + ''.join(mutated_list), '\n')
        return ''.join(mutated_list)
        
    def select_1(self, offspring):
        # eval_fittest = tuple - (fitness_value, problem_solved)
        eval_fittest = heapq.nlargest(1, offspring)[0][0]
        # fittest_offspring = list - [offspring_bit_strings]
        fittest_offspring = [child[1] for child in offspring if 
                             child[0][0] == eval_fittest[0]]
        # fittest = bit_string
        fittest = np.random.choice(fittest_offspring, 1)[0]
#        print(fittest, eval_fittest[0])
        return fittest
    
    def crossover(self, second_parent):
        p_c = [1 - self.crossover_probability, self.crossover_probability]
        cross_list = [self.cross_select(self.parent[1][i], 
                                        second_parent[i], p_c) for i in 
                                        range(self.problem_size)]
#        print(''.join(cross_list), self.problem.evaluate(''.join(cross_list)))
        return ''.join(cross_list)
        
    def select_2(self, offspring):
        offspring = [child for child in offspring if 
                     child[1] != self.parent[1]]
        if len(offspring) == 0:
            self.s = 0
            self.fit_gen.append(self.parent[0][0])
            return
        # eval_fittest = tuple - (fitness_value, problem_solved)
        eval_fittest = heapq.nlargest(1, offspring)[0][0]
        # fitter_offspring = list - [offspring_bit_strings]
        fitter_offspring = [child[1] for child in offspring if 
                             child[0][0] > self.parent[0][0]]
        self.s = len(fitter_offspring)
        # fittest_offspring = list - [offspring_bit_strings]
        fittest_offspring = [child[1] for child in offspring if 
                             child[0][0] == eval_fittest[0]]
        # fittest = bit_string
        fittest = np.random.choice(fittest_offspring, 1)[0]
#        print(fittest, self.problem.evaluate(fittest)[0])
        if eval_fittest[0] >= self.parent[0][0]:
            self.bit_string = fittest
            self.fit_gen.append(eval_fittest[0])
#            print(eval_fittest[0])
        else:
            self.fit_gen.append(self.parent[0][0])
#            print(self.parent[0][0])
        if eval_fittest[1]:
            self.solved = True
#        print(self.bit_string, eval_fittest[0], self.problem.max_fitness, 
#              self.evaluations, len(fittest_offspring))
            
    def cross_select(self, selection1, selection2, p):
        return np.random.choice([selection1, selection2], 1, p = p)[0]
    
    def update(self):
        if self.s > 0:
            self.offspring_size /= self.offspring_update_factor
        else:
            self.offspring_size *= math.pow(self.offspring_update_factor, 1/4)
        self.offspring_size = max(self.offspring_size, 1)
        self.offspring_size = min(self.offspring_size, self.problem_size)
        self.mutation_probability = self.offspring_size / self.problem_size
        self.crossover_probability = 1 / self.offspring_size