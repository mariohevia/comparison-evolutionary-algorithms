#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 21:02:19 2018

@author: mario_hevia
"""

import numpy as np
from operator import xor
import heapq

class OnePlusLambda:
    def __init__(self, problem, problem_size, mutation_probability, 
                 offspring_size, not_used_1, not_used_2, not_used_3):
        self.problem = problem
        self.problem_size = problem_size
        self.mutation_probability = mutation_probability
        self.offspring_size = offspring_size
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
        self.mut_prob_gen.append(self.mutation_probability)
        self.lambda_gen.append(self.offspring_size)
        for i in range(self.offspring_size):
            mutated_string = self.mutate()
            offspring.append((self.problem.evaluate(mutated_string), 
                              mutated_string))
        self.select(offspring)
        self.generations += 1
        self.evaluations += self.offspring_size
#        print(self.bit_string)
        
    def mutate(self):
        p = [1 - self.mutation_probability, self.mutation_probability]
        mut_array = np.random.choice(['0', '1'], self.problem_size, p = p)
        mutated_list = [str(xor(int(b), int(m))) for b, m in 
                        zip(self.bit_string, mut_array)]
#        print(self.generations, '\n' + self.bit_string, '\n' + ''.join(mutated_list), '\n')
        return ''.join(mutated_list)
        
    def select(self, offspring):
        # eval_fittest = tuple - (fitness_value, problem_solved)
        eval_fittest = heapq.nlargest(1, offspring)[0][0]
        # fittest_offspring = list - [offspring_bit_strings]
        fittest_offspring = [child[1] for child in offspring if 
                             child[0][0] == eval_fittest[0]]
        # fittest = bit_string
        fittest = np.random.choice(fittest_offspring, 1)[0]
        if eval_fittest[0] >= self.parent[0][0]:
            self.bit_string = fittest
            self.fit_gen.append(eval_fittest[0])
        else:
            self.fit_gen.append(self.parent[0][0])
        if eval_fittest[1]:
            self.solved = True
#        print(self.bit_string, eval_fittest[0], self.problem.max_fitness, 
#              self.evaluations, len(fittest_offspring))