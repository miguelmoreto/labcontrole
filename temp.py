#!/usr/bin/ python3
# -*- coding: utf-8 -*-
#
# Testing control system module.
import control as ct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys = ct.tf([2,10],[1,2,10])
FTMF = sys/(1+sys)
data = ct.step_response(sys,10)

topandas = {'time': data.time}
topandas.update({'u' : data.inputs})
topandas.update({'y' : data.outputs})
serie = pd.DataFrame(topandas)


fig,ax = plt.subplots(figsize=(6, 5),layout='constrained')
fig.suptitle('Grafico')

#serie.plot(x='time',ax=ax)


# make data
x = np.linspace(0, 10, 100)
y = 4 + 2 * np.sin(2 * x)

z = np.zeros((2,10))
z[0][5:] = 2
z[1][3:] = 1
y = z.transpose()
a = np.arange(0,10,1)

ax.plot(a, y, linewidth=2.0)
#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#       ylim=(0, 8), yticks=np.arange(1, 8))

#roots, gains = ct.root_locus(sys,kvect=np.linspace(0,20,100),plot=True,ax=ax)
plt.show()
