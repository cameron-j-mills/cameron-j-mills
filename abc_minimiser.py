# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 10:34:24 2021

@author: camer
"""
import numpy as np
import matplotlib.pyplot as plt
import time
import random

def fitness(f_test):
    if f_test >= 0:
        return 1/(1 + f_test)
    else:
        return 1 + abs(f_test)
    
def ABC(f, guess_ranges, args, args_index, N_food_sources, limit, convergence_crit, iterations):
    
    food_sources = np.zeros((N_food_sources, len(guess_ranges)))
    food_sources_best_guess = np.zeros((N_food_sources, len(guess_ranges)))
    func_values = np.zeros(N_food_sources)
    fitnesses = np.zeros(N_food_sources)
    trials = np.zeros(N_food_sources)
    
    total_fitness = 0
    # INITIALISATION
    for i in range(N_food_sources):                                           
        for p in range(len(guess_ranges)):
            food_sources[i,p] = np.random.uniform(guess_ranges[p,0],guess_ranges[p,1])
        args[args_index] = food_sources[i]
        func_values[i] = f(*args)
        fitnesses[i] = fitness(func_values[i])
        total_fitness += fitnesses[i]
        
    new_global_min_func_value = min(func_values)
    global_min = food_sources[0]
    
    all_iters_foodsource_points = [food_sources]
    all_iters_globmin = [new_global_min_func_value]
    all_iters_params_globmin = [global_min]
    
    for iters in range(iterations):
        
        # EMPLOYEED BEE PHASE
        for i in range(N_food_sources):
            param_index = np.random.randint(len(guess_ranges))
            food_source_indices_lst = list(range(N_food_sources))
            food_source_indices_lst.remove(i)
            partner_index = np.random.choice(np.array(food_source_indices_lst))
            
            phi = np.random.uniform(-1,1)
            x_test = np.copy(food_sources[i])
            x_test[param_index] = x_test[param_index] + phi*(x_test[param_index] \
                                                             - food_sources[partner_index,param_index])
                
            args[args_index] = x_test
            test_fitness = fitness(f(*args))
            if test_fitness > fitnesses[i]: 
                food_sources[i] = x_test
                food_sources_best_guess[i] = x_test
                func_values[i] = f(*args)
                total_fitness -= fitnesses[i]
                fitnesses[i] = test_fitness
                total_fitness += test_fitness
                trials[i] = 0
            else:
                trials[i] = trials[i] + 1
            
        
        # ONLOOKER BEE PHASE
        probs = fitnesses / total_fitness
        for i in range(N_food_sources):
            s = random.choices(np.array(range(N_food_sources)), probs)[0]
            param_index = np.random.randint(len(guess_ranges))
            food_source_indices_lst = list(range(N_food_sources))
            food_source_indices_lst.remove(s)
            partner_index = np.random.choice(np.array(food_source_indices_lst))
            
            phi = np.random.uniform(-1,1)
            x_test = np.copy(food_sources[s])
            x_test[param_index] = x_test[param_index] + phi*(x_test[param_index] \
                                                             - food_sources[partner_index,param_index])
            args[args_index] = x_test
            test_fitness = fitness(f(*args))
            if test_fitness > fitnesses[s]: 
                food_sources[s] = x_test
                food_sources_best_guess[s] = x_test
                func_values[s] = f(*args)
                fitnesses[s] = test_fitness
                trials[s] = 0
            else:
                trials[s] = trials[s] + 1

        # CHOOSE NEW GLOBAL MIN GUESS
        if min(func_values) < new_global_min_func_value:
            new_global_min_func_value = min(func_values)
            min_index = list(func_values).index(new_global_min_func_value)
            global_min = np.copy(food_sources[min_index])
           
        
        # SCOUT BEE PHASE  
        for i in range(N_food_sources):
            if trials[i] > limit:
                for p in range(len(guess_ranges)):
                    food_sources[i,p] = np.random.uniform(guess_ranges[p,0],guess_ranges[p,1])
                args[args_index] = food_sources[i]
                func_values[i] = f(*args)
                fitnesses[i] = fitness(func_values[i])
        
        all_iters_foodsource_points.append(np.copy(food_sources))
        all_iters_globmin.append(np.copy(new_global_min_func_value))
        all_iters_params_globmin.append(np.copy(global_min))
        
                
    return global_min, np.array(all_iters_foodsource_points), np.array(all_iters_globmin), np.array(all_iters_params_globmin)


