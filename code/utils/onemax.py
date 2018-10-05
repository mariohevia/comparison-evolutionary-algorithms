#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:36:55 2018

@author: mario_hevia
"""

class OneMax:
    def __init__(self, problem_size):
        self.max_fitness = problem_size
        
    def evaluate(self, bit_string):
        fitness_value = bit_string.count('1')
        if fitness_value == self.max_fitness:
            optimal_fitness = True
        else:
            optimal_fitness = False
        return fitness_value, optimal_fitness