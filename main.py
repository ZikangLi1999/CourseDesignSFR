# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""
import pip

modules = ["thermostate", "matplotlib", "numpy", "colorama"]
try:
    for module in modules:
        pip.main(["install", module])
except:
    print("Pip Failed.")

from iteration import inner_iteration
import optimization

import colorama
from colorama import Fore, Style
from time import time
import json
import os


# Parameters of main loop and gasp, which determine the system
state_mid = json.loads(open("input-mid.json").read())

state_low = json.loads(open("input-low.json").read())

state_high = json.loads(open("input-high.json").read())

# Outer Iteration
def outer_iteration(s_mid, s_low=None, s_high=None, optm=None):

    # Run inner iteration

    # Option 1: Single State Solver
    if s_low is None and s_high is None:
        inner_iteration(s_mid, graph=True)
    
    # Option 2: Greedy Algorithm Optimized Solver
    elif optm == 'pa':
        pa = optimization.GreedyAlgo(s_mid, s_low, s_high)
        best = pa.loop()
        with open('output.json', 'w') as o:
            o.write(json.dumps(best, indent=4))
        print(
            f"\n{Fore.YELLOW}Result of Greedy Algorithm Optimization:{Style.RESET_ALL}\n")
        for k, v in best.items():
            print("{} = {}".format(k, v))
        inner_iteration(best, graph=True, print_all=True)
    
    # Option 3: Genetic Algorithm Optimized Solver
    elif optm == 'ga':
        pass
    
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
        outer_iteration(state_mid, state_low, state_high, 'pa')
    elif opt == '3':
        print("Not available now.")
    else:
        print(
            f"{Fore.RED}Invalid Choice.{Style.RESET_ALL}")
    # Time span
    end = time()
    print("\nTime span: {} sec\n".format(end - start))

# Main
if __name__ == '__main__':
    main()
