#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 12:19:43 2018

@author: mario_hevia
"""

import pickle
import matplotlib.pyplot as plt

class Outputs:
    def __init__(self, results = None):
        self.results = results
        
    def save(self, name):
        with open('results/results' + name + '.pkl', 'wb') as f:
            pickle.dump(self.results, f)
        
    def load(self, name):
        with open('results/results' + name + '.pkl', 'rb' ) as f:
            self.results = pickle.load(f)
        
    def show_results(self):
        if self.results is None:
            print('No results available')
        else:
            print('Average generations to solve:', self.results['Avg_generations'])
            print('Average evaluations to solve:', self.results['Avg_evaluations'])
            print('Average fitness:', self.results['Avg_fitness'])
        
    def show_plots(self, name):
        if self.results is None:
            print('No results available')
        else:
            x = range(len(self.results['Avg_fitness_per_gen']))
            y = self.results['Avg_fitness_per_gen']
            y1 = self.results['Avg_lambda_per_gen']
            y2 = self.results['Avg_mut_rate_per_gen']
            plt.title('Average fitness per gen')
            plt.plot(x, y, 'bo')
            plt.savefig('results/Avg_fitness_per_gen' + name + '.png')
            plt.clf()
            plt.title('Average λ per gen')
            plt.plot(x, y1, c='black', ls='-')
            plt.savefig('results/Avg_lambda_per_gen' + name + '.png')
            plt.clf()
            plt.title('Average mutation rate per gen')
            plt.plot(x, y2, c='black', ls='--')
            plt.savefig('results/Avg_mut_rate_per_gen' + name + '.png')
            plt.close()
