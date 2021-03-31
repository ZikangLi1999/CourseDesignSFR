# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""

from iteration import inner_iteration

from functools import partial
from colorama import Fore, Style
from math import isclose

# Genetic Algorithm
# Optimize efficiency of the thermodynamic system
class GeneticAlgo(object):
    
    def __init__(self, low, high, elite=True, mutation=0.1):
        self.population_size = 100
        self.low = low
        self.high = high
        self.elite = elite
        self.mutation = mutation
    
    def __init_population__(self):
        pass

    def __select__(self):
        pass

    def __reproduce__(self):
        pass # double and half ?

    def __mutate__(self):
        pass

    def __evolve__(self):
        pass


# Greedy Algorithm optimization
class GreedyAlgo(object):

    def __init__(self, mid, low, high):
        self.step = 20
        self.low = [v for v in low.values()]
        self.high = [v for v in high.values()]
        self.best = [v for v in mid.values()]
        self.template = mid
        self.func = inner_iteration
        self.best_score = 0.10 # self.func(self.__encode__(self.best))
        
    def __encode__(self, ls):
        d = self.template.copy()
        for idx, key in enumerate(d.keys()):
            d[key] = ls[idx]
        return d
    
    def loop(self):
        for i, para in enumerate(self.template.keys()):
            print(
                f"\n{Fore.YELLOW}Parameter: {para}{Style.RESET_ALL}\n")
            temp = self.best.copy()
            for j in range(self.step + 1):
                value = (j * self.high[i] + (self.step - j) * self.low[i]) / self.step
                temp[i] = value
                try:
                    score = self.func(self.__encode__(temp))
                except ValueError as e:
                    print(e)
                    continue
                except ZeroDivisionError as z:
                    print(z)
                    continue
                # Update if acquiring a better efficiency
                if score > self.best_score:
                    self.best[i] = value
                    self.best_score = score
                if isclose(score, 0.3037, abs_tol=0.0001):
                    return self.__encode__(self.best)
        return self.__encode__(self.best)
    
    def get_best(self, best=None):
        if best is None:
            best = self.loop()
        try:
            pass
        except:
            print('!')
