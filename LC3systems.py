# -*- coding: utf-8 -*-
#
#
# Class definitions for the system types used in LabControl 3.

import numpy as np
import control as ct
#import pandas as pd

class LTIsystem:
    """
    This class implements a LTI system with simulation methods.

    System Type:
        0   K.G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        1   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        2   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation before G(s)
    """
    K = 1.0         # System gain.
    Gnum = [2,10]           # G(s) numerator polynomial coefficients.
    GnumStr = '2*s+10'     # G(s) numerator polynomial string
    #polyGnum = np.poly1d(Gnum)
    Gden = [1,2,10]             # G(s) denominator polynomial coefficients.
    GdenStr = '1*s^2+2*s+10'    # G(s) denominator polynomial string.
    #polyGden = np.poly1d(Gden)
    Cnum = [1]      # C(s) numerator polynomial coefficients.
    CnumStr = '1'
    #polyCnum = np.poly1d(Cnum)
    Cden = [1]      # C(s) denominator polynomial coefficients.
    CdenStr = '1'
    #polyCden = np.poly1d(Cden)
    Hnum = [1]      # H(s) numerator polynomial coefficients.
    HnumStr = '1'
    #polyHnum = np.poly1d(Hnum)
    Hden = [1]      # H(s) denominator polynomial coefficients.
    HdenStr = '1'
    #polyHden = np.poly1d(Hden)
    
    OLTF_r = ct.tf(1,1) # Open Loop Transfer Function for r input
    CLTF_r = ct.tf(1,1) # Closed Loop Transfer Function for r input
    OLTF_w = ct.tf(1,1) # Open Loop Transfer Function for w input
    CLTF_w = ct.tf(1,1) # Closed Loop Transfer Function for w input    
    
    TM = ct.tf(1,1) # Transfer Matrix (MIMO system)
    #TM = ct.tf(1,1) # Closed Loop Transfer Matrix (MIMO system)

    #polyDnum = np.poly1d([1]) # numerator polynomial of the direct loop transfer function
    #polyDden = np.poly1d([1]) # denominator polynomial of the direct loop transfer function

    Type = 1    # system type.
    Index = 0   # System index within a list.
    Name = ''
    TypeStrList = ['LTI_1','LTI_2', 'LTI_3']    # List with string for the system types.
    TypeStr = ''    # String with the current system type string.

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

    # Time Domain simulation data
    TimeSimList = []                # List to store a collection of Data Dictionaries
    TimeSimData = {'Name':[]}       # A Dictionary to store time simulation data.
    CurrentTimeSimIndex = -1        # An index for time simulation data. The LC3systems
                                    # object can store several simulations.
    CurrentSimulName = ''
    # TimeSimData dictionary structure:
    #  key 'Name': a list containing the name of each simulation data
    #  Each name in the list will be a key in the dictionary. This key
    #  will contain also a dictionary with the keys 'time', 'r', 'w', 'y' and 'u'
    #  that contains the numpy arrays with the plotting data.

    def __init__(self,index,systype):
        """
        Init function. Updates
        """
        self.Type = systype
        self.Index = index
        self.Name = '{i}: LTI_{t}'.format(i=index,t=systype)   # Format name string
        self.TypeStr = self.TypeStrList[systype-1]
        self.updateSystem()

    def updateSystem(self):
        """
        Update the system transfer functions (open and closed loop)
        according with the poynomial coefficients stored in
        the class properties Xnum and Xdem.

        For time domain simulation it is used a MIMO system
        Transfer Function object. The inputs are r(t) and w(t) 
        while outpus are y(t) and u(t)
        """
        self.N = self.Tmax/self.delta_t
        self.G_tf = ct.tf(self.Gnum,self.Gden)
        self.C_tf = ct.tf(self.Cnum,self.Cden)
        self.H_tf = ct.tf(self.Hnum,self.Hden)

        # Compute OpenLoop and ClosedLoop transfer functions accordingly with
        # the system type.
        if (self.Type == 0):
            self.OLTF_r = (self.K * self.G_tf).minreal(0.0001)
            self.CLTF_r = ((self.K * self.G_tf)/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
            self.OLTF_w = ct.tf(1,1)
            self.CLTF_w = (1/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
        elif (self.Type == 1):
            self.OLTF_r = (self.K * self.C_tf * self.G_tf).minreal(0.0001)
            self.CLTF_r = ((self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
            self.OLTF_w = ct.tf(1,1)
            self.CLTF_w = (1/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
        elif (self.Type == 2):
            self.OLTF_r = (self.K * self.C_tf * self.G_tf).minreal(0.0001)
            self.CLTF_r = ((self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
        
        # Computing MIMO system Transfer Matrix polynomial coefficients.
        # This is a 2x2 MIMO system, therefore there are 4 transfer functions.
        if (self.Type == 0):
            if (self.Loop == 'open'):   # Open Loop
                YR_tf = (self.K * self.G_tf).minreal(0.0001)    # Y(s)/R(s) transfer function
                YW_tf = ct.tf(1,1)                              # Y(s)/W(s) transfer function
                UR_tf = self.K * ct.tf(1,1)                     # U(s)/R(s) transfer function
                UW_tf = ct.tf(0,1)                              # U(s)/W(s) transfer function
            else:   # Closed Loop
                YR_tf = ((self.K * self.G_tf)/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
                YW_tf = (1/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
                UR_tf = (self.K/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
                UW_tf = (-(self.K * self.H_tf)/(1 + self.K * self.G_tf * self.H_tf) ).minreal(0.0001)
        elif (self.Type == 1):
            if (self.Loop == 'open'):   # Open Loop
                YR_tf = (self.K * self.C_tf * self.G_tf).minreal(0.0001)    # Y(s)/R(s) transfer function
                YW_tf = ct.tf(1,1)                                          # Y(s)/W(s) transfer function
                UR_tf = (self.K * self.C_tf).minreal(0.0001)                # U(s)/R(s) transfer function
                UW_tf = ct.tf(0,1)                                          # U(s)/W(s) transfer function
            else:   # Closed Loop
                YR_tf = ((self.K * self.C_tf * self.G_tf)/(1+self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                YW_tf = (1/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                UR_tf = ((self.K * self.C_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                UW_tf = (-(self.K * self.C_tf * self.H_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf) ).minreal(0.0001)
        else:
            return 0 # System type not recognized.
        
        # Transfer Matrix:
        #  input 0: r(t)   output 0: y(t)
        #  input 1: w(t)   output 1: u(t)
        print(YR_tf.num)
        num = [[YR_tf.num[0][0],YW_tf.num[0][0]], [UR_tf.num[0][0],UW_tf.num[0][0]]] # array rows corresponds to outputs, columns to inputs
        den = [[YR_tf.den[0][0],YW_tf.den[0][0]], [UR_tf.den[0][0],UW_tf.den[0][0]]]
        print(num)
        self.TM = ct.tf(num,den)


    def changeSystemType(self, newtype):
        # This method should do:
        #  Change CurrentSimulName
        #  Update the transfer matrix (if LTI)
        #  Add a new TimeSimData or overwrite the current one?
        pass

    def addSimul(self):
        # Format simul name string:
        self.CurrentTimeSimIndex = self.CurrentTimeSimIndex + 1
        self.CurrentSimulName = 'LTI_{t}:{i}'.format(t=self.Type,i=self.CurrentTimeSimIndex)
        self.TimeSimData['Name'].append(self.CurrentSimulName)
    
    def createInputVectors(self, tinic=0.0, Rinic = 0, Winic = 0):
        """
        Create a time and an input vector from two strings representing
        any python mathematical function as a function of the variable t.        
        One string for the input r(t) and another for w(t)
        
        self.InstRt start instant of input r(t);
        self.InstWt start instant of input w(t).
        
        tinic = initial time.
        """
        
        if (self.InstRt > self.Tmax) or (self.InstWt > self.Tmax):
            print("Step time cannot be larger than Tmax.")
            return 0
        
        # Time vector:
        if (self.Type == 3):
            # For discrete simulation it is needed 2 more samples in input vector.
            t_total = np.arange(tinic,tinic+self.Tmax+2*self.delta_t,self.delta_t)
        else:
            t_total = np.arange(tinic,tinic+self.Tmax,self.delta_t)
           
        r = np.zeros((1,len(t_total)))
        w = np.zeros((1,len(t_total)))
        
        # Number of the samples corresponding to the begining of the inputs:
        sampleR = int(self.InstRt/self.delta_t)
        sampleW = int(self.InstWt/self.delta_t)
        
        # create vector r(t):
        t = t_total[0:(len(t_total)-sampleR)] # This is necessary to eval expressions with 't'
        if (self.ruidoRt > 0):
            r[0][sampleR:] = eval(self.Rt) + np.random.normal(0,self.ruidoRt,(len(t_total)-sampleR))
            r[0][0:sampleR] = Rinic + np.random.normal(0,self.ruidoRt,sampleR)
        else:
            r[0][sampleR:] = eval(self.Rt)
            r[0][0:sampleR] = Rinic

        # create vector w(t)
        if (self.ruidoWt > 0):
            w[1][sampleW:] = eval(self.Wt) + np.random.normal(0,self.ruidoWt,(len(t_total)-sampleW))
        else:
            w[1][sampleW:] = eval(self.Wt)
            w[1][0:sampleW] = Winic

        # Input variation (will be deprecated):
        if (self.RtVar != 0):
            Delta_r = np.zeros_like(t_total)
            Dusample = int(self.RtVarInstant/self.delta_t)
            Delta_r[Dusample:] = self.RtVar
            r = r + Delta_r

        #u[0] = Rinic
        #w[0] = Winic

        self.tfinal = t_total[-1]
        self.Rfinal = r[0][-1]
        self.Wfinal = w[0][-1]

        self.TimeSimData[self.CurrentSimulName] = {'time':t_total,'r(t)':r,'w(t)':w}
       
        #return t_total, r, w

    def TimeSimulationTesting(self):
        """
        Temporary method only to test the UI and multiplot feature
        """
        time = np.arange(0,1,0.01)
        y = np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time)
        u = 2*np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time+np.pi/2)
        r = np.ones(len(time))
        w = 0.5*np.ones(len(time))
        e = r - y
        self.TimeSimData[self.CurrentSimulName] = {'time':time,'r(t)':r,'w(t)':w,'y(t)':y,'u(t)':u,'e(t)':e}

    
    def TimeSimulation(self):
        """
        Performs a time domain simulation.
        """

        T = self.TimeSimData[self.CurrentSimulName]['time']
        U = np.append(self.TimeSimData[self.CurrentSimulName]['r'],self.TimeSimData[self.CurrentSimulName]['w'],axis=0)
        T,Y = ct.forced_response(self.TM,T,U,return_x=False)
        self.TimeSimData[self.CurrentSimulName]['y'] = Y[0]
        self.TimeSimData[self.CurrentSimulName]['u'] = Y[1]

        pass