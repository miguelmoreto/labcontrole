# -*- coding: utf-8 -*-
"""
Created on Wed May 21 09:47:59 2014

@author: User
"""
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

K = 1

numC = [0.5,1]
denC = [1,0]
polynumC = np.poly1d(numC)
polydenC = np.poly1d(denC)

numG1 = [1]
denG1 = [0.5, 1]
polynumG1 = np.poly1d(numG1)
polydenG1 = np.poly1d(denG1)

numG2 = [1]
denG2 = [1]
polynumG2 = np.poly1d(numG2)
polydenG2 = np.poly1d(denG2)

numH = [1]
denH = [1]
polynumH = np.poly1d(numH)
polydenH = np.poly1d(denH)


#FTR:
numFTR = K*polynumC*polynumG1*polynumG2*polynumH
denFTR = (polydenC*polydenG1*polydenG2*polydenH) + numFTR

sysFTR = signal.lti(numFTR,denFTR)

t,y = signal.step2(sysFTR)

plt.plot(t,y)
plt.grid()
plt.show()