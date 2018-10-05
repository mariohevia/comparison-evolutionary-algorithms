#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 13:59:43 2018

@author: mario_hevia
"""

class LeadingOnes:
    def __init__(self, problem_size):
        self.max_fitness = problem_size
        
    def evaluate(self, bit_string):
        fitness_value = 0
        for bit in bit_string:
            if bit == '1':
                fitness_value += 1
            else:
                break
        if fitness_value == self.max_fitness:
            optimal_fitness = True
        else:
            optimal_fitness = False
        return fitness_value, optimal_fitness