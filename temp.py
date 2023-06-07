#!/usr/bin/ python3
# -*- coding: utf-8 -*-
#
# Testing control system module.
# import control as ct
# #import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# from scipy.signal import lti, lsim2

# # Testing solver:
# A = np.array([[0, 1], [0, 0]])
# B = np.array([[0], [1]])
# C = np.array([[1, 0]])
# D = 0
# system = lti(A, B, C, D)

# t = np.linspace(0, 5, num=50)
# u = np.ones_like(t)

# tout, y, x = lsim2(system, u, t,X0=[1,1])

# print(len(t))
# print(len(tout))

#plt.plot(t, y)
#plt.grid(alpha=0.3)
#plt.xlabel('t')
#plt.show()

#sys = ct.tf([2,10],[1,2,10])
#FTMF = sys/(1+sys)
#data = ct.step_response(sys,10)
#ct.set_defaults('nyquist',indent_radius=0.001)
#ct.set_defaults('nyquist',max_curve_magnitude=20)
#G1 = ct.zpk([],[0,-1,-2],10)
#N,contour = ct.nyquist_plot(sys,return_contour=True,plot=True)
#resp = G1(contour)
#x, y = resp.real.copy(), resp.imag.copy()

#fig,ax = plt.subplots(figsize=(6, 5))#,layout='constrained')
#ax.plot(x,y)
#fig.suptitle('Grafico')

#serie.plot(x='time',ax=ax)


# make data
# x = np.linspace(0, 10, 100)
# y = 4 + 2 * np.sin(2 * x)
# 
# z = np.zeros((2,10))
# z[0][5:] = 2
# z[1][3:] = 1
# y = z.transpose()
# a = np.arange(0,10,1)
# 
# TimeSimData = {}
# 
# time = np.arange(0,1,0.01)
# y = np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time)
# u = np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time+np.pi/2)
# r = np.ones(len(time))
# w = 0.5*np.ones(len(time))
# TimeSimData['simul1'] = {'time':time,'r(t)':r,'w(t)':w,'y(t)':y,'u(t)':u}
# 
# 
# #ax.plot(time, y, linewidth=2.0)
# ret1 = ax.plot('time', 'y(t)', data=TimeSimData['simul1'])
# ret2 = ax.plot('time', 'u(t)', data=TimeSimData['simul1'])
# ax.legend(loc=1)
#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#       ylim=(0, 8), yticks=np.arange(1, 8))

#roots, gains = ct.root_locus(sys,kvect=np.linspace(0,20,100),plot=True,ax=ax)
# plt.show()

# https://matplotlib.org/stable/gallery/event_handling/cursor_demo.html
import matplotlib.pyplot as plt
from matplotlib.backend_tools import Cursors


fig, axs = plt.subplots(len(Cursors), figsize=(6, len(Cursors) + 0.5),
                        gridspec_kw={'hspace': 0})
fig.suptitle('Hover over an Axes to see alternate Cursors')

for cursor, ax in zip(Cursors, axs):
    ax.cursor_to_use = cursor
    ax.text(0.5, 0.5, cursor.name,
            horizontalalignment='center', verticalalignment='center')
    ax.set(xticks=[], yticks=[])


def hover(event):
    if fig.canvas.widgetlock.locked():
        # Don't do anything if the zoom/pan tools have been enabled.
        return

    fig.canvas.set_cursor(
        event.inaxes.cursor_to_use if event.inaxes else Cursors.POINTER)


fig.canvas.mpl_connect('motion_notify_event', hover)

plt.show()
