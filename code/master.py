#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 13:00:35 2018

@author: mario_hevia
"""

import numpy as np
import math
from utils.inputs import CommandLine
from utils.onemax import OneMax
from utils.leadingones import LeadingOnes
from utils.sufsamp import SufSamp
from utils.makespanscheduling import MakespanScheduling
from utils.onepluslambda import OnePlusLambda
from utils.onepluslambdasamut import OnePlusLambdaSAMut
from utils.onepluslambdasamutimp import OnePlusLambdaSAMutImp
from utils.onepluslambdasaoff import OnePlusLambdaSAOff
from utils.onepluslambdasaoffimp1 import OnePlusLambdaSAOffImp1
from utils.onepluslambdasaoffimp2 import OnePlusLambdaSAOffImp2
from utils.onepluslambdasaoffimp3 import OnePlusLambdaSAOffImp3
from utils.onepluslambdasamutoff import OnePlusLambdaSAMutOff
from utils.onepluslambdacommalambda import OnePlusLambdaCommaLambda
from utils.onepluslambdacommalambdasa import OnePlusLambdaCommaLambdaSA
from utils.onepluslambdacommalambdasaimp1 import OnePlusLambdaCommaLambdaSAImp1
from utils.onepluslambdacommalambdasaimp2 import OnePlusLambdaCommaLambdaSAImp2
from utils.onepluslambdacommalambdasaimp3 import OnePlusLambdaCommaLambdaSAImp3
from utils.onepluslambdacommalambdasaimp4 import OnePlusLambdaCommaLambdaSAImp4
from utils.outputs import Outputs

def execute_experiment():
    configuration = CommandLine()
    problem_string = (configuration.problem + '(' + 
                      str(configuration.problem_size) + ')')
    algorithm_string = (configuration.algorithm + '(' + 'problem,' +
                      str(configuration.problem_size) + ',' +
                      str(configuration.mut_prob) + ',' +
                      str(configuration.offspring_size) + ',' +
                      str(configuration.cross_prob) + ',' +
                      str(configuration.mut_update_factor) + ',' +
                      str(configuration.offspring_update_factor) + ')')
    np.random.seed(configuration.seed)
    
    if configuration.verbose:
        print('Experiment configurations')
        print('Problem:', configuration.problem, '\nSize:', 
              configuration.problem_size, '\nRuns:', configuration.num_runs,
              '\nStop criteria:', configuration.stop_criteria, 
              '\nMax generations (if aplicable):', 
              configuration.max_generations,
              '\nMax evaluations (if aplicable):', 
              configuration.max_evaluations, '\nAlgorithm:', 
              configuration.algorithm, '\nInitial mutation probability:',
              configuration.mut_prob, '\nInitial offspring population size:',
              configuration.offspring_size, '\nInitial crossover probability',
              '(if aplicable):', configuration.cross_prob, '\nMutation update',
              'factor (if aplicable):', configuration.mut_update_factor,
              '\nOffspring population size update factor (if aplicable):',
              configuration.offspring_update_factor)
        print('\n------------------------------------------------------------'
              '------\n')
    generations = []
    evaluations = []
    fitness = []
    lambdas = []
    mut_rates = []
    for run in range(1, configuration.num_runs + 1):    
        past_fitness = 0
        tol = 0
        tol2 = 0
        problem = eval(problem_string)
        algorithm = eval(algorithm_string)
        if configuration.stop_criteria == 'solved':
            m_size = max(100 * math.pow(configuration.problem_size,4), 1000000)
            while not algorithm.solved:
                next(algorithm)
                if (algorithm.parent[0][0] == past_fitness):
                    tol += 1
                    tol2 += algorithm.offspring_size
                else:
                    tol = 0
                    tol2 = 0
                past_fitness = algorithm.parent[0][0]
                if (algorithm.evaluations > m_size or tol2 > 1000000):
                    break
        elif configuration.stop_criteria == 'ngenerations':
            for i in range(configuration.max_generations):
                next(algorithm)
                if algorithm.solved:
                    break
        else:
            while algorithm.evaluations < configuration.max_evaluations:
                next(algorithm)
                if algorithm.solved:
                    break
        generations.append(algorithm.generations)
        evaluations.append(algorithm.evaluations)
        fitness.append(algorithm.fit_gen)
        lambdas.append(algorithm.lambda_gen)
        mut_rates.append(algorithm.mut_prob_gen)
        if configuration.verbose:
            print('Final results: ' + 
                  '{0:<4} {1:<4} {2:<5} {3:<7} {4:<6} {5:<7} {6:<2} {7} {8} {9} {10:<7} {11}'.format(
                    'Run:', run, 'Gens:', algorithm.generations, 'Evals:', 
                    algorithm.evaluations, 'λ:', algorithm.lambda_gen[-1], 
                    'p:', algorithm.mut_prob_gen[-1], 'Solved:', 
                    algorithm.solved))
    
    if configuration.verbose:
        print('\n------------------------------------------------------------'
              '------\n')
    
    avg_lambda = avg_list_of_lists(lambdas)
    avg_mut_rate = avg_list_of_lists(mut_rates)
    avg_fit = avg_list_of_lists(fitness)
    # Calculates average of generations and evaluations per run 
    avg_gen = sum(generations)/len(generations)
    avg_eval = sum(evaluations)/len(evaluations)
    
#    print(avg_mut_rate)
    
    results = {}
    results['Avg_generations'] = avg_gen
    results['Avg_evaluations'] = avg_eval
    results['Avg_fitness'] = avg_fit[-1]
    results['Avg_fitness_per_gen'] = avg_fit
    results['Avg_lambda_per_gen'] = avg_lambda
    results['Avg_mut_rate_per_gen'] = avg_mut_rate
    
    res = Outputs(results)
    name = ('_'+configuration.problem+'_'+str(configuration.problem_size)+'_'+
            configuration.algorithm+'_'+str(configuration.offspring_size))
    if configuration.verbose:
        res.show_results()
        res.show_plots(name)
    res.save(name)

    return results
    
def avg_list_of_lists(list_of_lists):
    # Makes all the list of the same lenght to make averages of fitness across
    # every generation.
    max_len = max(len(elem) for elem in list_of_lists)
    for i, elem in enumerate(list_of_lists):
        list_of_lists[i] = [elem[j] if j < len(elem) else elem[-1] 
                      for j in range(max_len)]
    # Calculates the average of fitness per generation without counting 0's
    array = np.asarray(list_of_lists)
    array = array.astype(float)
    array[array == 0] = np.nan
    avg_array = np.nanmean(array, axis=0)
    return list(avg_array)
    
if __name__ == '__main__':
    res = execute_experiment()
