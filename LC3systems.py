# -*- coding: utf-8 -*-
#
#
# Class definitions for the system types used in LabControl 3.

import numpy as np
import control as ct

class LTIsystem:
    """
    This class implements a LTI system with simulation methods.

    System Type:
        0   K.G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        1   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        2   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation before G(s)
    """
    Gnum = [2,10]   # G(s) numerator polynomial coefficients.
    #polyGnum = np.poly1d(Gnum)
    Gden = [1,2,10] # G(s) denominator polynomial coefficients.
    #polyGden = np.poly1d(Gden)
    Cnum = [1]      # C(s) numerator polynomial coefficients.
    #polyCnum = np.poly1d(Cnum)
    Cden = [1]      # C(s) denominator polynomial coefficients.
    #polyCden = np.poly1d(Cden)
    Hnum = [1]      # H(s) numerator polynomial coefficients.
    #polyHnum = np.poly1d(Hnum)
    Hden = [1]      # H(s) denominator polynomial coefficients.
    #polyHden = np.poly1d(Hden)
    
    OLTF_r = ct.tf(1,1) # Open Loop Transfer Function for r input
    CLTF_r = ct.tf(1,1) # Closed Loop Transfer Function for r input
    OLTF_w = ct.tf(1,1) # Open Loop Transfer Function for w input
    CLTF_w = ct.tf(1,1) # Closed Loop Transfer Function for w input    

    #polyDnum = np.poly1d([1]) # numerator polynomial of the direct loop transfer function
    #polyDden = np.poly1d([1]) # denominator polynomial of the direct loop transfer function

    Type = 1    # system type.
    Index = 0   # System index within a list.
    Name = ""

    # Inputs (reference and perturbation):
    Rt = '1'        # String with the r(t) input function.
    InstRt = 0.0    # Time instant of r(t).
    noiseRt = 0.0   # Noise standard deviation.
    Wt = '0'        # String with the w(t) input function.
    InstWt = 0.0    # Time instant of w(t).
    noiseWt = 0.0   # Noise standard deviation.
    
    RtVar = 0.0         # Input variation value.
    RtVarInstant = 0.0  # Input variation instant.

    delta_t = 0.005     # Time domain simulation time step value.
    Tmax = 10           # Time domain max simulation time.
    tfinal = 10         # Time domain simulation final time value.
    
    Loop = 'open'       # Feedback loop state (open or closed)
    Hide = False        # Hide system data (used for experimental system identification exercises)
    
    K = 1.0             # System gain.
    
    Kmax = 10.0         # Max gain for root locus plot.
    Kmin = 0.0          # Min gain for root locus plot.
    Kpoints = 200       # Number of K point for root locus plot. 
    
    # Root locus forbidden regions paramethers:
    Rebd = 0.0
    Ribd = 0.0
    Imbd = 0.0
    
    # Bode diagram paramethers:
    Fmin = 0.01
    Fmax = 100.0
    Fpoints = 20
    
    # Nyquist plot paramethers:
    NyqFmin = 0.01
    NyqFmax = 100.0
    NyqFpoints = 100
    
    # Initial states:
    X0r = None
    X0w = None

    #     Initial values:
    e0 = 0.0                     # Initial error value (C(s) input)
    y0 = np.array([0.0])         # Output initial value for 1 order system
    X0 = [0]                     # C(s) LTI initial states.
    y00 = np.array([0.0,0.0])    # Output initial value for 2 order system
    N = 0                        # Number of samples

    def __init__(self,index,systype):
        """
        Init function. Updates
        """
        self.Type = systype
        self.Index = index
        self.Name = '{i}: LTI_{t}'.format(i=index,t=systype)   # Format name string
        self.updateSystem()

    def updateSystem(self):
        """
        Update the system transfer functions (open and closed loop)
        """
        self.N = self.Tmax/self.delta_t
        self.G_tf = ct.tf(self.Gnum,self.Gden)
        self.C_tf = ct.tf(self.Cnum,self.Cden)
        self.H_tf = ct.tf(self.Hnum,self.Hden)

        # Compute OpenLoop and ClosedLoop transfer functions accordingly with
        # the system type.
        if (self.Type == 0):
            self.OLTF_r = self.K * self.G_tf
            self.CLTF_r = (self.K * self.G_tf)/(1+self.K * self.G_tf * self.H_tf)
            self.OLTF_w = ct.tf(1,1)
            self.CLTF_w = 1/(1+self.K * self.G_tf * self.H_tf)
        elif (self.Type == 1):
            self.OLTF_r = self.K * self.C_tf * self.G_tf
            self.CLTF_r = (self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)
            self.OLTF_w = ct.tf(1,1)
            self.CLTF_w = 1/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)
        elif (self.Type == 2):
            self.OLTF_r = self.K * self.C_tf * self.G_tf
            self.CLTF_r = (self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)
