# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""
# import pip

# try:
#     pip.main(["install", "-i", "https://pypi.douban.com/simple", "-r", "requirements.txt"])
# except:
#     print("Pip Failed.")

from iteration import inner_iteration
import optimization

from numpy import linspace
import colorama
from colorama import Fore, Style
from time import time, sleep
import json
import os


# Parameters of main loop and gasp, which determine the system
state_mid = json.loads(open("input-mid.json").read())

state_low = json.loads(open("input-low.json").read())

state_high = json.loads(open("input-high.json").read())

# Outer Iteration
def outer_iteration(s_mid=None, s_low=None, s_high=None, optm=None):

    # Run inner iteration

    # Option 1: Single State Solver
    if s_low is None and s_high is None:
        inner_iteration(s_mid, graph=True, print_all=True)
    
    # Option 2: Greedy Algorithm Optimized Solver
    elif optm == 'greedy':
        # Iterate the GreedyAlgo - Yikai Wu
        # mid_copy = s_mid.copy()
        # space = linspace(0.1, 0.9, 9)
        best = s_mid
        best_score = 0.01
        new_score = 0.10
        while abs(new_score - best_score) / best_score > 0.01:
            greedy = optimization.GreedyAlgo(best, s_low, s_high)
            best = greedy.loop()
            best_score = new_score
            new_score = greedy.best_score
        # for pr1 in space:
        #     for pr2 in space:
        #         print(f"\n{Fore.RED}r1_pointer={pr1}\tr2_pointer={pr2}{Style.RESET_ALL}\n")
        #         sleep(3)
        #         mid_copy['pr'] = [pr1, pr2]
        #         best = s_mid
        #         best_score = 0.01
        #         new_score = 0.10
        #         while abs(new_score - best_score) / best_score > 0.01:
        #             greedy = optimization.GreedyAlgo(best, s_low, s_high)
        #             best = greedy.loop()
        #             best_score = new_score
        #             new_score = greedy.best_score
        #         if new_score > 0.3944:
        #             inner_iteration(best, graph=True, print_all=True)
        with open('output.json', 'w') as o:
            o.write(json.dumps(best, indent=4))
        print(
            f"\n{Fore.YELLOW}Result of Greedy Algorithm Optimization:{Style.RESET_ALL}\n")
        for k, v in best.items():
            print("{} = {}".format(k, v))
        inner_iteration(best, graph=True, print_all=True)
    
    # Option 3: Genetic Algorithm Optimized Solver
    elif optm == 'genetic':
        genetic = optimization.GeneticAlgo(s_low, s_high)
    
    else:
        raise ValueError("Outer iteration parameters error.")


def main():
    colorama.init()
    print(
        f"\n{Fore.BLUE}Design Code of Thermodynamic System\n1. Single State Solver\n2. Greedy Algorithm Optimized Solver\n3. Genetic Algorithm Solver{Style.RESET_ALL}\n")
    
    # Determine the solver: Single State, Greedy Algorithm or Genetic Algorithm
    opt = input("Your choice ? ")
    start = time()
    if opt == '1':
        outer_iteration(state_mid)
    elif opt == '2':
        outer_iteration(state_mid, state_low, state_high, 'greedy')
    elif opt == '3':
        outer_iteration(state_mid, state_low, state_high, 'genetic')
    else:
        print(
            f"{Fore.RED}Invalid Choice.{Style.RESET_ALL}")
    # Time span
    end = time()
    print("\nTime span: {} sec\n".format(end - start))

# Main
if __name__ == '__main__':
    main()
