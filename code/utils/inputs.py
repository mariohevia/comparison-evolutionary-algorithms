#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:21:01 2018

@author: mario_hevia
"""

import argparse
import random
import math
import sys

class CommandLine:
    def __init__(self):
        
        problems = ['OneMax', 'LeadingOnes', 'SufSamp', 'MakespanScheduling']
        stop_criteria = ['solved', 'ngenerations', 'nevaluations']
        algorithms = ['OnePlusLambda', 'OnePlusLambdaSAMut',
                      'OnePlusLambdaSAOff', 'OnePlusLambdaCommaLambda',
                      'OnePlusLambdaCommaLambdaSA', 'OnePlusLambdaSAMutImp',
                      'OnePlusLambdaSAOffImp1', 'OnePlusLambdaSAOffImp2',
                      'OnePlusLambdaSAOffImp3', 'OnePlusLambdaSAMutOff',
                      'OnePlusLambdaCommaLambdaSAImp1',
                      'OnePlusLambdaCommaLambdaSAImp2',
                      'OnePlusLambdaCommaLambdaSAImp3',
                      'OnePlusLambdaCommaLambdaSAImp4', 'help']
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', dest='problem', type=str, default='OneMax',
                            choices=problems, metavar='', help='Problem to '
                            'solve. Allowed values are: '+', '.join(problems)+
                            '. (default: %(default)s)')
        parser.add_argument('-n', dest='problem_size', type=int, metavar=
                            '[10-5000]', default=100,
                            help='Size of the problem "n". (default: '
                            '%(default)d)')
        parser.add_argument('-r', dest='num_runs', type=int, metavar=
                            '[1-10000]', default=100, 
                            help='Number of runs. (default: %(default)d)')
        parser.add_argument('-s', dest='stop_criteria', type=str, metavar=''
                            , choices=stop_criteria, default='solved', 
                            help='Stop criteria. Allowed values are: ' +
                            ', '.join(stop_criteria)+'. (default: %(default)s)')
        parser.add_argument('-g', dest='max_generations', type=int, metavar=
                            '[10-100000]', default=1000, help='Maximum number of '
                            'generations. (default: %(default)d)')
        parser.add_argument('-e', dest='max_evaluations', type=int, metavar=
                            '[10-1000000]', default=10000, help='Maximum'
                            ' number of evaluations. (default: %(default)d)')
        parser.add_argument('-a', dest='algorithm', type= str, 
                            default='OnePlusLambda', choices=algorithms, 
                            metavar='', help='Algorithm used. Allowed values '
                            'are: '+', '.join(algorithms[:-1])+'. For '
                            'information on acronyms write "-a help". '
                            '(default: %(default)s)')
        parser.add_argument('-p', dest='mut_prob', type=float, metavar=
                            '[0.0-1.0]', help='Mutation probability ”p”. '
                            '(default: 1/n)')
        parser.add_argument('-l', dest='offspring_size', type=int, metavar=
                            '[1-50*n*log_2(n)]', default=1, help='Offspring '
                            'size population ”λ”.  (default: %(default)d)')
        parser.add_argument('-c', dest='cross_prob', type=float, metavar=
                            '[0.0-1.0]', help='Crossover probability. '
                            '(default: 1/λ)')
        parser.add_argument('-F', dest='mut_update_factor', type=float, 
                            metavar='[1.0-5.0]', default=2, help='Mutation '
                            'update factor. (default: %(default)d)')
        parser.add_argument('-G', dest='offspring_update_factor', type=float, 
                            metavar='[1.0-5.0]', default=2, help='Offspring '
                            'size population update factor. (default: '
                            '%(default)d)')
        parser.add_argument('--seed', dest='seed', type=int, 
                            metavar='int ∈ Z', help='Seed for random '
                            'number generation. (default: None)')
        parser.add_argument('-v', '--verbose', action='store_true'
                            , help='Print information per run. '
                            '(default: False)')
        args = parser.parse_args()
        arg_list = sys.argv
        self.problem = args.problem
        self.problem_size = args.problem_size
        self.num_runs = args.num_runs
        self.stop_criteria = args.stop_criteria
        self.max_generations = args.max_generations
        self.max_evaluations = args.max_evaluations
        self.algorithm = args.algorithm
        self.mut_prob = args.mut_prob
        self.offspring_size = args.offspring_size
        self.cross_prob = args.cross_prob
        self.mut_update_factor = args.mut_update_factor
        self.offspring_update_factor = args.offspring_update_factor
        self.seed = args.seed
        self.verbose = args.verbose
        
        alg_acro = ['(1+λ) EA', 
                    '(1+λ) EA with self-adjusting mutation rate', 
                    '(1+λ) EA with self-adjusting offspring popularion size',
                    '(1+(λ,λ)) GA',
                    'Self-adjusting (1+(λ,λ)) GA',
                    '(1+λ) EA with improved self-adjusting mutation rate',
                    '(1+λ) EA with improved self-adjusting offspring population size 1',
                    '(1+λ) EA with improved self-adjusting offspring population size 2', 
                    '(1+λ) EA with improved self-adjusting offspring population size 3', 
                    '(1+λ) EA with self-adjusting mutation rate and offspring population size', 
                    'Improved Self-adjusting (1+(λ,λ)) GA 1', 
                    'Improved Self-adjusting (1+(λ,λ)) GA 2', 
                    'Improved Self-adjusting (1+(λ,λ)) GA 3', 
                    'Improved Self-adjusting (1+(λ,λ)) GA 4']
        if self.algorithm == 'help':
            print('Acronyms for the argument -a')
            print('\n'.join(str(n+1) + '- %s - %s' % t for n, t in 
                            enumerate(zip(algorithms, alg_acro))))
            parser.exit()
        if self.problem_size < 10 or self.problem_size > 5000:
            parser.print_usage()
            print('master.py: error: argument -n: invalid choice:',
                  self.problem_size, '(choose from range 10 - 5000)')
            parser.exit()
        if self.num_runs < 1 or self.num_runs > 10000:
            parser.print_usage()
            print('master.py: error: argument -r: invalid choice:',
                  self.num_runs, '(choose from range 1 - 10000)')
            parser.exit()
        if self.stop_criteria != 'ngenerations' and '-g' in arg_list:
            print('master.py: warning: argument -g: not in use:', 
                  self.max_generations,
                  '(change argument -s to "ngenerations")')
        if (self.stop_criteria == 'ngenerations' and
            (self.max_generations < 10 or self.max_generations > 100000)):
            parser.print_usage()
            print('master.py: error: argument -g: invalid choice:',
                  self.max_generations, '(choose from range 10 - 100000)')
            parser.exit()
        if self.stop_criteria != 'nevaluations' and '-e' in arg_list:
            print('master.py: warning: argument -e: not in use:', 
                  self.max_evaluations,
                  '(change argument -s to "nevaluations")')
        if (self.stop_criteria == 'nevaluations' and
            (self.max_evaluations < 10 or self.max_evaluations > 1000000)):
            parser.print_usage()
            print('master.py: error: argument -e: invalid choice:',
                  self.max_evaluations, '(choose from range 10 - 1000000)')
            parser.exit()
        if ('OnePlusLambdaCommaLambdaSA' in self.algorithm and
            self.mut_prob is not None):
            print('master.py: warning: argument -p: not in use:', 
                  self.mut_prob, '(change argument -a)')
        if self.mut_prob is None:
            self.mut_prob = 1 / self.problem_size
        if self.mut_prob >= 1 or self.mut_prob <= 0:
            parser.print_usage()
            print('master.py: error: argument -p: invalid choice:',
                  self.mut_prob, '(choose from range 0.0 - 1.0)')
            parser.exit()
        max_offspring_size = round(50 * self.problem_size * 
                                   math.log(self.problem_size, 2))
        if self.offspring_size > max_offspring_size or self.offspring_size < 1:
            parser.print_usage()
            print('master.py: error: argument -l: invalid choice:',
                  self.offspring_size, '(choose from range  1 - %d)))' 
                  % max_offspring_size)
            parser.exit()
        if (self.algorithm == 'OnePlusLambdaCommaLambda' and 
            self.cross_prob is not None):
            print('master.py: warning: argument -c: not in use:', 
                  self.cross_prob, '(change argument -a)')
        if self.cross_prob is None:
            self.cross_prob = 1 / self.offspring_size
        if self.cross_prob > 1 or self.cross_prob < 0:
            parser.print_usage()
            print('master.py: error: argument -c: invalid choice:',
                  self.cross_prob, '(choose from range 0.0 - 1.0)')
            parser.exit()
        mut_factor_algorithms = ['OnePlusLambdaSAMut',
                                 'OnePlusLambdaSAMutImp', 
                                 'OnePlusLambdaSAMutOff']
        if '-F' in arg_list and self.algorithm not in mut_factor_algorithms:
            print('master.py: warning: argument -F: not in use:', 
                  self.mut_update_factor, '(change argument -a)')
        if self.mut_update_factor > 5 or self.mut_update_factor < 1:
            parser.print_usage()
            print('master.py: error: argument -F: invalid choice:',
                  self.mut_update_factor, '(choose from range 1.0 - 5.0)')
            parser.exit()
        off_factor_algorithms = ['OnePlusLambdaSAOff',
                                 'OnePlusLambdaCommaLambdaSA', 
                                 'OnePlusLambdaSAOffImp1', 
                                 'OnePlusLambdaSAOffImp2',
                                 'OnePlusLambdaSAOffImp3', 
                                 'OnePlusLambdaSAMutOff',
                                 'OnePlusLambdaCommaLambdaSAImp1',
                                 'OnePlusLambdaCommaLambdaSAImp2',
                                 'OnePlusLambdaCommaLambdaSAImp3',
                                 'OnePlusLambdaCommaLambdaSAImp4']
        if '-G' in arg_list and self.algorithm not in off_factor_algorithms:
            print('master.py: warning: argument -G: not in use:', 
                  self.offspring_update_factor, '(change argument -a)')
        if self.offspring_update_factor > 5 or self.offspring_update_factor < 1:
            parser.print_usage()
            print('master.py: error: argument -G: invalid choice:',
                  self.offspring_update_factor, '(choose from range 1.0 - 5.0)')
            parser.exit()
        if self.seed is None:
            self.seed = random.seed()
        