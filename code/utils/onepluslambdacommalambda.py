#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 21:02:19 2018

@author: mario_hevia
"""

import numpy as np
from operator import xor
import heapq

class OnePlusLambdaCommaLambda:
    def __init__(self, problem, problem_size, mutation_probability, 
                 offspring_size, cross_prob, not_used_2, not_used_3):
        self.problem = problem
        self.problem_size = problem_size
        self.mutation_probability = mutation_probability
        self.crossover_probability = cross_prob
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
        l = np.random.binomial(self.problem_size, self.mutation_probability)
        for i in range(self.offspring_size):
            mutated_string = self.mutate(l)
            offspring.append((self.problem.evaluate(mutated_string), 
                              mutated_string))
            self.evaluations += 1
        fittest_mut = self.select_1(offspring)
        offspring = []
        for i in range(self.offspring_size):
            cross_string = self.crossover(fittest_mut)
            offspring.append((self.problem.evaluate(cross_string), 
                              cross_string))
            self.evaluations += 1
        self.select_2(offspring)
        self.generations += 1
        
    def mutate(self, l):
        mut_indexes = np.random.choice(self.problem_size, size = l,
                                       replace=False)
        mutated_list = [str(xor(int(bit), 1)) if i in mut_indexes else bit 
                        for i, bit in enumerate(self.bit_string)]
        return ''.join(mutated_list)
        
    def select_1(self, offspring):
        # eval_fittest = tuple - (fitness_value, problem_solved)
        eval_fittest = heapq.nlargest(1, offspring)[0][0]
        # fittest_offspring = list - [offspring_bit_strings]
        fittest_offspring = [child[1] for child in offspring if 
                             child[0][0] == eval_fittest[0]]
        # fittest = bit_string
        fittest = np.random.choice(fittest_offspring, 1)[0]
        return fittest
    
    def crossover(self, second_parent):
        p_c = [1 - self.crossover_probability, self.crossover_probability]
        cross_list = [self.cross_select(self.parent[1][i], 
                                        second_parent[i], p_c) for i in 
                                        range(self.problem_size)]
        return ''.join(cross_list)
        
    def select_2(self, offspring):
        offspring = [child for child in offspring if 
                     child[1] != self.parent[1]]
        if len(offspring) == 0:
            self.fit_gen.append(self.parent[0][0])
            return
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
            
    def cross_select(self, selection1, selection2, p):
        return np.random.choice([selection1, selection2], 1, p = p)[0]