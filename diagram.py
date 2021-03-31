# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""

from substance import nitrogen

import matplotlib.pyplot as plt
import numpy as np

# In T-s diagram, isobaric process is a curve,
#   which could be smoother and more beautiful when adding more points
def smooth_diagram(pressure, s1, s2):
    x = np.linspace(s1, s2, 30)
    y = [nitrogen(p=pressure, s=x[i]).t for i in range(30)]
    return (x, y)

# Draw T-s diagram using key state points
def ts_diagram(state, turbine_gasp):

    # Get t and s from key points
    x = [state[i].s for i in range(1, 13)]
    y = [state[i].t for i in range(1, 13)]
    x_gasp = [t.s for t in turbine_gasp]
    y_gasp = [t.t for t in turbine_gasp]

    # Smooth isobaric curve data
    line = []
    for start, end in [(2, 3), (6, 4), (8, 7), (9, 1)]:
        line.append(smooth_diagram(state[start].p, state[start].s, state[end].s))
    
    # Plot
    plt.scatter(x, y)
    plt.scatter(x_gasp, y_gasp, color='red')
    for i, j in [(0, 1), (2, 3), (6, 5), (8, 7)]:
        plt.plot([x[i], x[j]], [y[i], y[j]], color='blue', linewidth=1)
    for l in line:
        plt.plot(l[0], l[1], color='blue', linewidth=1)
    
    # Annotate
    for tag, i, j in zip(range(1, 13), x, y):
        plt.annotate(str(tag), xy=(i, j))
    for tag, i, j in zip(["HPT Gasp", "LPT Gasp"], x_gasp, y_gasp):
        plt.annotate(tag, xy=(i, j))
    
    # Plot setting
    plt.title(r"T-s Diagram of SFR Brayton Cycle")
    plt.xlabel(r"$s / [J\cdot (kg\cdot K)^{-1}]$")
    plt.ylabel(r"$T / ^{\circ }C$")
    plt.show()
