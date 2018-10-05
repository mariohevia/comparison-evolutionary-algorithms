#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 14:14:58 2018

@author: mario_hevia
"""

import math
from utils.onemax import OneMax
from utils.leadingones import LeadingOnes

class SufSamp:
    def __init__(self, problem_size):
        self.m_1 = math.floor(problem_size/2)
        self.m_2 = math.ceil(problem_size/2)
        self.k = math.floor(math.sqrt(self.m_2))
#        self.one_max_0 = OneMax(problem_size)
        self.one_max_1 = OneMax(self.m_1)
        self.one_max_2 = OneMax(self.m_2)
        self.x_1 = ''.join(['0' for i in range(problem_size)])[:self.m_1]
        self.x_2 = ''.join(['0' for i in range(problem_size)])[self.m_1:]
        self.problem_size = problem_size
        self.max_fitness =  ((self.m_2+4) * self.m_2 + self.m_2)
        
    def evaluate(self, bit_string):
        bit_string_1 = bit_string[:self.m_1]
        bit_string_2 = bit_string[self.m_1:]
        if bit_string_1 != self.x_1 and bit_string_2 != self.x_2:
            fitness_value = (self.problem_size - 
                             self.one_max_2.evaluate(bit_string_2)[0])
        elif bit_string_1 != self.x_1 and bit_string_2 == self.x_2:
            fitness_value = (2 * self.problem_size - 
                             self.one_max_1.evaluate(bit_string_1)[0])
        elif bit_string_1 == self.x_1:
            fitness_value = self.evaluate_f(bit_string_2)
        if fitness_value == self.max_fitness:
            optimal_fitness = True
        else:
            optimal_fitness = False
        return fitness_value, optimal_fitness
    
    def evaluate_f(self, bit_string):
        count_i, first_condition = self.condition_f(bit_string)
        sub_bit_string = bit_string[self.k:]
        count2_i, second_condition = self.condition_f(sub_bit_string)
        num_k = math.floor(self.m_2 / self.k)
        list_k = [self.k*i for i in range(1, num_k - 2)]
        if (count2_i in list_k) and second_condition:
            other_conditions = True
        else:
            other_conditions = False
        if first_condition:
            fitness_value = ((count_i+4) * self.m_2 + 
                             self.one_max_2.evaluate(bit_string)[0])
        elif other_conditions:
            fitness_value = ((count2_i+4) * self.m_2 + 
                             self.one_max_2.evaluate(bit_string)[0])
        else:
            fitness_value = 0
        return fitness_value
    
    def condition_f(self, bit_string):
        # Checks if (x = 0^(n−i) 1^(i) with 0 ≤ i ≤ n)
        start_flag = False
        continue_flag = False
        end_flag = False
        count_i = 0
        for bit in bit_string:
            # Checks if the first bit is 1 if it is starts counting the 1's
            if bit == '1' and not start_flag:
                start_flag = True
                continue_flag = True
            else:
                start_flag = True
            # If the first bit is 0 waits until a 1 is found to start counting
            if bit == '1' and start_flag and not continue_flag:
                continue_flag = True
            # If a 1 has been found and a 0 is found again the condition is
            # nor fulfilled
            if bit != '1' and continue_flag:
                end_flag = False
                break
            # Start counting the 1's when the first is found
            if start_flag and continue_flag:
                count_i += 1
            end_flag = True
        return count_i, end_flag