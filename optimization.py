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
import numpy as np

# Genetic Algorithm
# Optimize efficiency of the thermodynamic system
class GeneticAlgo(object):
    
    def __init__(self, low, high, population_size=2000, elite=True, cross=0.4, mutation=0.05):
        self.size = population_size
        self.chromosome_len = len(low)
        self.diversity = 100
        self.fitness = [0.0 for i in range(self.size)]
        self.low = [v for v in low.values()]
        self.high = [v for v in high.values()]
        self.template = low.copy()
        self.elite = elite
        self.cross = cross
        self.mutation = mutation
        self.maxIter = 100
        self.population = self.__init_population__()
        self.__evolve__()
    
    def __init_population__(self):
        # Initialize a population
        # Row: Individual, Column: Gene
        population = np.random.randint(low=0, high=self.diversity, size=(self.size, self.chromosome_len), dtype=np.int8)
        print(population)
        return population

    def __fit__(self):
        # Calculate fitness level of indiviudals
        for idx, individual in enumerate(self.population):
            chromosome = self.__transcript__(individual)
            try:
                self.fitness[idx] = inner_iteration(self.__translate__(chromosome), print_key=False)
                if self.fitness[idx] > 0.30:
                    print(self.__translate__(chromosome))
                    print(self.fitness[idx])
            except ValueError:
                continue
            except ZeroDivisionError:
                continue

    def __select__(self):
        # Natural Selection
        # Individuals with higher fitness level are more propable to be selected.
        fitness = np.asarray(self.fitness)
        idx = np.random.choice(np.arange(self.size), size=self.size, replace=True, p=fitness/fitness.sum())
        return self.population[idx]        

    def __reproduce__(self, fathers, mother):
        # Population Reproduce
        # Chromosome Cross happens between parents.
        if np.random.rand() < self.mutation:
            idx = np.random.randint(0, self.size, size=1)
            cross_gene = np.random.randint(0, 2, self.chromosome_len).astype(np.bool)
            mother[cross_gene] = fathers[idx, cross_gene]
        return mother

    def __mutate__(self, child):
        # Gene Mutation
        # Genes mutate randomly to import more diversity.
        for gene in range(self.chromosome_len):
            if np.random.rand() < self.mutation:
                child[gene] = np.random.randint(low=0, high=self.diversity, size=1, dtype=np.int8)
        return child

    def __evolve__(self):
        # Evolution
        # Populations will reproduce, cross and mutate to adapt the environment.
        for i in range(self.maxIter):
            self.__fit__()
            self.population = self.__select__()
            population_copy = self.population.copy()
            for individual in self.population:
                child = self.__reproduce__(population_copy, individual)
                individual[:] = self.__mutate__(child)
        # End Evolution
        print(self.population)

    def __transcript__(self, individual):
        # Transcription
        # Transcript random numbers in chromosome into RNA parameters. 
        RNA = []
        for i in range(self.chromosome_len):
            gene = (individual[i] * self.low[i]\
                + (self.diversity - individual[i]) * self.high[i])\
                / self.diversity
            RNA.append(gene)
        return RNA

    def __translate__(self, ls):
        # Translation
        # Translate RNA list into protein dict.
        d = self.template.copy()
        for idx, key in enumerate(d.keys()):
            d[key] = ls[idx]
        return d


# Greedy Algorithm
class GreedyAlgo(object):

    def __init__(self, mid, low, high):
        self.step = 40
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
            if para == 'pr':
                continue
            else:
                for j in range(self.step + 1):
                    value = (j * self.high[i] + (self.step - j) * self.low[i]) / self.step
                    temp[i] = value
                    self.__get_best__(i, value, temp)
        return self.__encode__(self.best)
    
    def __get_best__(self, i, value, paras):
        try:
            score = self.func(self.__encode__(paras))
            # Update if acquiring a better efficiency
            if score > self.best_score:
                self.best[i] = value
                self.best_score = score
        except ValueError as e:
            print(e)
        except ZeroDivisionError as z:
            print(z)
