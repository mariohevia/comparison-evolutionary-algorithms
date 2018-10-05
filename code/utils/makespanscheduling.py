#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 10:57:09 2018

@author: mario_hevia
"""

import numpy as np
import operator

class MakespanScheduling:
    def __init__(self, problem_size):
        self.weights = np.random.uniform(low=0, high=1, size=(problem_size,))
        self.sum_weights = np.sum(self.weights)
        self.max_fitness = self.sum_weights - self.aprox_solution()
        
    def evaluate(self, bit_string):
        indices_0 = [i for i, char in enumerate(bit_string) if char == '0']
        indices_1 = [i for i, char in enumerate(bit_string) if char == '1']
        sum_0 = 0
        for index in indices_0:
            sum_0 += self.weights[index]
        sum_1 = 0
        for index in indices_1:
            sum_1 += self.weights[index]
        fitness_value = self.sum_weights - max(sum_0, sum_1)
        if fitness_value >= self.max_fitness:
            optimal_fitness = True
        else:
            optimal_fitness = False
        return fitness_value, optimal_fitness
    
    def aprox_solution(self):
        jobs_sorted = np.flip(np.sort(self.weights), 0)
        sums = [0, 0]
        for job in jobs_sorted:
            min_index, min_value = min(enumerate(sums), 
                                       key=operator.itemgetter(1))
            sums[min_index] += job
        return max(sums)
            
            
            
