# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""

from substance import sodium, nitrogen
from diagram import ts_diagram

from colorama import Fore, Style
import csv


# Iteration
# 
# This solution consists of outer iteration and inner iteration.
# Outer iteration optimizes thermodynamic parameters of each state.
#   * Efficiency, Na-loop allocation ratio(alpha), Turbine allocation ratio(beta)
#     and extraction ratio(r1, r2) are used to evaluate the outer iteration.
#   * Outer iteration will be optimized manually, because we don't know the method exactly.
# Inner iteration solve the value of efficiency
#   * (|eff' - eff| < epsilon) is the convergence criterion of inner iteration.

'''
def outer_iteration(W, eff0):
    Q = W / eff0
    Q_HeatEx = alpha * Q
    Q_Reheator = (1 - alpha) * Q
'''

# Constants
equip = {
    'lpc_ratio': 2.0,
    'hpc_ratio': 1.8,
    'ihx_eff': 1.0,
    'reh_eff': 1.0,
    'hpt_eff': 1.0,
    'lpt_eff': 1.0,
    'fpt_eff': 1.0,
    'beta': 0.5,
}

# Inner Iteration
# state_para, gasp_para, link_para !!!
def inner_iteration(para, graph=False, print_key=True, print_all=False):
    r = [0.0 for i in range(2)]
    # Define states of the key points
    # state[0] is useless (just for more readable index).
    # state_gasp contains states of gasp from turbines.
    state = [None for i in range(13)]
    state_gasp = []
    state_link = []
    state[1] = nitrogen(p=para['p1'], t=para['t1'])
    state_gasp.append(nitrogen(p=para['pr1'], s=state[1].s))
    state[2] = nitrogen(p=para['p2'], s=state[1].s)
    state[3] = nitrogen(p=state[2].p, t=para['t3'])
    state_gasp.append(nitrogen(p=para['pr2'], s=state[3].s))
    state[4] = nitrogen(p=para['p4'], s=state[3].s)
    state[5] = nitrogen(p=state[4].p, t=para['t5'])
    state[6] = nitrogen(p=state[5].p, t=para['t6'])
    state[7] = nitrogen(p=equip['lpc_ratio']*state[6].p, s=state[6].s)

    if para['ptr1']*(state[1].t-state[2].t)+state[2].t < state_gasp[0].t or state[2].t > state_gasp[0].t:
        raise ValueError("HPT out of range.")
    if state[3].t < state_gasp[1].t or para['ptr2']*(state[3].t-state[4].t)+state[4].t > state_gasp[1].t:
        raise ValueError("LPT out of range.")

    # Equivalent enthalpy rise
    state[10] = nitrogen(p=state[1].p, t=para['t10'])
    state[11] = nitrogen(p=state[10].p, t=para['t11'])
    state[12] = nitrogen(p=state[11].p, t=para['t12'])

    # 1-2 & 2-3
    state_link.append(nitrogen(p=state_gasp[0].p, t=state_gasp[1].t))
    state_link.append(nitrogen(p=state_gasp[1].p, t=state[4].t))
    # state_link.append(nitrogen(p=state_gasp[0].p, t=para['tk1']))
    # state_link.append(nitrogen(p=state_gasp[1].p, t=para['tk2']))

    # if not (state_link[1].t > state[5].t and state_link[1].t > state[10].t and state_link[1].t < state_gasp[1].t):
    #     raise ValueError("Link[1] Temp.")
    # if not (state_link[0].t > state[11].t and state_link[0].t < state_gasp[0].t and state_link[1].t < state_link[0].t):
    #     raise ValueError("Link[0] Temp.")

    # Calculate r1, r2
    r[0] = (state[12].h - state[11].h)\
        / (state_gasp[0].h - state_link[0].h)
    r[1] = (state[11].h - state[10].h - r[0] * (state_link[0].h - state_link[1].h))\
        / (state_gasp[1].h - state_link[1].h)

    state[9] = nitrogen(p=state[1].p, h=state[10].h - ((1 - r[0] - r[1]) * (state[4].h - state[5].h) + (r[0] + r[1]) * (state_link[1].h - state[5].h)))
    state[8] = nitrogen(p=state[7].p, s=state[9].s)

    if state[9].t > para['t10'] or para['t10'] > para['t11'] or para['t11'] > para['t12']:
        raise ValueError("Temperatures Decrease.")
    if state[9].t >state[5].t:
        raise ValueError("R3 boomed.")
    # rise1 = (state[10].h - state[9].h) / (state[11].h - state[10].h)
    # rise2 = (state[11].h - state[10].h) / (state[12].h - state[11].h)
    # if not (rise1 > 0.1 and rise1 < 10.0 and rise2 > 0.1 and rise2 < 10.0):
    #     raise ValueError("Temperature Jump.")

    # Turbines and Compressers
    lpc = state[7].h - state[6].h
    hpc = state[9].h - state[8].h
    lpt = (1 - r[0]) * (state[3].h - state[4].h) - r[1] * (state_gasp[1].h - state[4].h)

    # Calculate alpha, beta
    alpha = 1 / (((1 - r[0]) * (state[3].h - state[2].h)\
        / (state[1].h - state[12].h)) + 1)
    beta = (r[0] * (state_gasp[0].h - state[2].h) + (lpc + hpc - lpt))\
        / (state[1].h - state[2].h)
    eff = (1 - beta) * (state[1].h - state[2].h) /\
        ((state[1].h - state[12].h) + (1 - r[0]) * (state[3].h - state[2].h))
    # flow = alpha * Q * (state[1].h - state[12].h)

    # Check legality of results
    for result in [alpha, beta, *r, eff]:
        if result < 0 or result >= 1:
            raise ValueError("Illegal result.")
    if sum(r) >= 1:
        raise ValueError("Illegal result.")
    if r[0] >= beta:
        raise ValueError("Illegal result.")
    
    # Print key parameters
    if print_key:
        print("\nalpha = {:.4f}".format(alpha))
        print("beta = {:.4f}".format(beta))
        print("r1 = {:.4f}\tr2 = {:.4f}".format(*r))
        print("enthalpy rise:\n\t9-10: {:.2f}\n\t10-11: {:.2f}\n\t11-12: {:.2f}\n".format(
            *[state[i+1].h - state[i].h for i in range(9, 12)]))
        print(
            f"{Fore.RED}efficiency = {eff:.4f}{Style.RESET_ALL}")

    # T-s Diagram
    if graph:
        ts_diagram(state, state_gasp)

    if print_all:
        tag = 0 if print_all is True else print_all
        with open('best_parameters{}.csv'.format(tag), 'w', newline='') as file:
            writer = csv.writer(file)
            title = [f'state', f'p / MPa', f't / degC', f'h / [J/kg]', f's / [J/(kg*K)]']
            writer.writerow(title)
            for idx, s in enumerate(state):
                if s is None:
                    continue
                else:
                    row = [idx, s.p, s.t, s.h, s.s]
                    writer.writerow(row)
            for idx, g in enumerate(state_gasp):
                row = [f'gasp[{idx}]', g.p, g.t, g.h, g.s]
                writer.writerow(row)
            for idx, l in enumerate(state_link):
                row = [f'link[{idx}]', l.p, l.t, l.h, l.s]
                writer.writerow(row)
            name = ['alpha', 'beta', 'r[0]', 'r[1]', 'eff']
            value = [alpha, beta, r[0], r[1], eff]
            for n, v in zip(name, value):
                writer.writerow([n, v])


    return eff
