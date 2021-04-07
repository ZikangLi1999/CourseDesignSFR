# -*- coding:utf-8 -*-
"""
Thermodynamic System Design of Sodium-cooled Fast Reactor
Course: NU317 Thermodynamic Design and Practise
Author: Zikang Li
Date: 2021 Spring
"""

from thermostate import State, Q_, units
from functools import partial

# Sodium thermodynamic state calculator
# Useless for now, since Na loop is seen as a black box
class sodium(object):

    def __init__(self, t=None, h=None):
        if t is not None:
            self.t = t
            self.h = self.__enthalpy__(t)
        elif h is not None:
            pass
        else:
            raise ValueError("Sodium Undefined.")
    
    def __enthalpy__(self, t):
        return 164.8 * (t - 370.87) - 1.97e-2


# Ease the procedure of creating a thermodynamic state using Q_
# Last Change: Zikang Li, 2021-3-17
class nitrogen(object):

    def __init__(self, p=None, t=None, h=None, s=None):
        self.substance = 'nitrogen' # Working Fluid
        self.nitrogen_state = partial(State, substance=self.substance)
        self.state = self.__state__(p, t, h, s)
        self.p = self.__getValue__(self.state.p)
        self.t = self.__getValue__(self.state.T)
        self.h = self.__getValue__(self.state.h)
        self.s = self.__getValue__(self.state.s)
    
    def __state__(self, p, t, h, s):
        # Two of the three parameters must exist to determine a thermodynamic state
        if p is None and t is None and s is None:
            raise ValueError("Lack of Parameter!")
        if p is not None:
            p = Q_(p, 'MPa') # Unit bar and Pa are allowed
        if t is not None:
            t = Q_(t+273.15, 'K') # Unit degC and degR are allowed
        if h is not None:
            h = Q_(h, 'J/kg')
        if s is not None:
            s = Q_(s, 'J/(kg*K)')
        try:
            if p and t:
                return self.nitrogen_state(p=p, T=t)
                # return State(self.substance, p=p, T=t)
            elif t and s:
                return self.nitrogen_state(T=t, s=s)
            elif p and s:
                return self.nitrogen_state(p=p, s=s)
            elif p and h:
                return self.nitrogen_state(p=p, h=h)
            elif t and h:
                return self.nitrogen_state(T=t, h=h)
            elif h and s:
                return self.nitrogen_state(h=h, s=s)
            else:
                raise RuntimeError("Nitrogen Undefined.")
        except RuntimeError as r:
            print(r)
    
    # Get Value of the Quantity Pair
    # 
    # Since thermostate.py uses Pint.Quantity to represent physical quantity as
    #     <Pint.Quantity(Value, Unit)>
    # e.g. entropy h = 6173.3846 J/kg is represented as
    #     <Pint.Quantity(6173.3846, Joule / kilograme)>
    # function __getValue__() returns the value without unit in type 'float'.
    def __getValue__(self, para):
        quan = str(para).split(' ')
        if quan[1] == 'pascal':
            return float(quan[0]) / 1e6
        elif quan[1] == 'kelvin':
            return float(quan[0]) - 273.15
        else:
            return float(quan[0])


# Examples
# How to get thermodynamic parameters using nitrogen or thermostste

'''Example with Class nitrogen above
state1 = nitrogen(p=1.0, t=30.0)
state2 = nitrogen(p=1.0, s=getValue(state1.s))
print("p1 = {}\tt1 = {}".format(state1.p, state1.t))
print("h1 = {}\ts1 = {}".format(state1.h, state1.s))
print("h2 = {}\ts2 = {}".format(state2.h, state2.s))
print("h1 - h2 = {}".format(state1.h - state2.h))
print(str(state1.h).split(' '))
print(getValue(state1.p), getValue(state1.t), getValue(state1.h))
'''

'''Example with the original thermostate
substance = 'nitrogen'
p1 = Q_(1.0, 'MPa')
t1 = Q_(30+273.15, 'K')
state1 = State(substance, T=t1, p=p1)

print("substance: {}".format(substance))
print("p = {}\tt = {}".format(p1, t1))
print("h = {:.2f}\ts = {:.2f}".format(state1.h, state1.s))
'''
