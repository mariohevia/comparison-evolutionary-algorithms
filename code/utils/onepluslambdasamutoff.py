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

class OnePlusLambdaSAMutOff:
    def __init__(self, problem, problem_size, mutation_probability, 
                 offspring_size, not_used_1, mut_update_factor, 
                 offspring_update_factor):
        self.problem = problem
        self.problem_size = problem_size
        self.mutation_probability = mutation_probability
        self.offspring_size = offspring_size
        self.mut_update_factor = mut_update_factor
        self.adjust_mut_prob()
        self.offspring_update_factor = offspring_update_factor
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
                       self.bit_string, 0]
        self.mut_prob_gen.append(self.mutation_probability)
        self.lambda_gen.append(math.ceil(round(self.offspring_size)/2)*2)
        for i in range(math.ceil(round(self.offspring_size)/2)):
            mutated_string = self.mutate(self.mutation_probability/2)
            offspring.append([self.problem.evaluate(mutated_string), 
                              mutated_string, 1])
            self.evaluations += 1
        for i in range(math.ceil(round(self.offspring_size)/2)):
            mutated_string = self.mutate(2*self.mutation_probability)
            offspring.append([self.problem.evaluate(mutated_string), 
                              mutated_string, 2])
            self.evaluations += 1
        self.select(offspring)
        self.update()
        self.generations += 1
#        print(self.bit_string)
        
    def mutate(self, mut_prob):
        p = [1 - mut_prob, mut_prob]
        mut_array = np.random.choice(['0', '1'], self.problem_size, p = p)
        mutated_list = [str(xor(int(b), int(m))) for b, m in 
                        zip(self.bit_string, mut_array)]
        return ''.join(mutated_list)
        
    def select(self, offspring):
        # eval_fittest = tuple - (fitness_value, problem_solved)
        eval_fittest = heapq.nlargest(1, offspring)[0][0]
        # fitter_offspring = list - [offspring_bit_strings]
        fitter_offspring = [child[1] for child in offspring if 
                             child[0][0] >= self.parent[0][0] and
                             child[1] != self.parent[1]]
        self.s = len(fitter_offspring)
        # fittest_offspring = list of lists - [children[bit_string,
        #                                               mut_population]]
        fittest_offspring = [child[1:3] for child in offspring if 
                             child[0][0] == eval_fittest[0]]
        fittest_index = np.random.choice(len(fittest_offspring), 1)
        # fittest = list - [bit_string, mut_population]
        fittest = fittest_offspring[fittest_index[0]]
        if eval_fittest[0] >= self.parent[0][0]:
            self.bit_string = fittest[0]
            self.fit_gen.append(eval_fittest[0])
#            print(eval_fittest[0], '-', self.mutation_probability, '-', 
#                  self.offspring_size)
        else:
            self.fit_gen.append(self.parent[0][0])
#            print(self.parent[0][0], '-', self.mutation_probability, '-', 
#                  self.offspring_size)
        self.mut_population = fittest[1]
        if eval_fittest[1]:
            self.solved = True
            
    def update(self):
        # Update mutation rate
        action_choice = np.random.choice([True, False], 1)[0]
#        action_choice = True
        action_choice_2 = np.random.choice([True, False], 1)[0]
        if action_choice:
            if self.mut_population == 1:
                self.mutation_probability /= self.mut_update_factor
            else:
                self.mutation_probability *= self.mut_update_factor
        else:
            if action_choice_2:
                self.mutation_probability /= self.mut_update_factor
            else:
                self.mutation_probability *= self.mut_update_factor
        self.adjust_mut_prob()
        # Update offspring population size
        if self.s > 0:
            self.offspring_size /= self.s # Try dividing by 2
        else:
            self.offspring_size *= self.offspring_update_factor
        self.offspring_size = max(self.offspring_size, 2)
                
    def adjust_mut_prob(self):
        mut_rate = self.mutation_probability * self.problem_size
        mut_rate = min(max(self.mut_update_factor, mut_rate),
                       self.problem_size / (2*self.mut_update_factor))
        self.mutation_probability = mut_rate / self.problem_size