# -*- coding: utf-8 -*-
#
#
# Class definitions for the system types used in LabControl 3.

import numpy as np
import control as ct
import scipy as sp
import logging as lg
import utils

class LTIsystem:
    """
    This class implements a LTI system with simulation methods.

    System Type:
        0   K.G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        1   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation after G(s)
        2   K.C(s).G(s) direct loop with H(s) in feedback. Perturbation before G(s)
    """
    K = 1.0                     # System gain.
    Gnum = [2,10]               # G(s) numerator polynomial coefficients.
    GnumStr = '2*s+10'          # G(s) numerator polynomial string
    Gden = [1,2,10]             # G(s) denominator polynomial coefficients.
    GdenStr = '1*s^2+2*s+10'    # G(s) denominator polynomial string.
    Genable = True
    
    Cnum = [1]          # C(s) numerator polynomial coefficients.
    CnumStr = '1'
    Cden = [1]          # C(s) denominator polynomial coefficients.
    CdenStr = '1'
    Cenable = False     # Flag to indicate if transfer function C(s) is enabled or not
    
    Hnum = [1]          # H(s) numerator polynomial coefficients.
    HnumStr = '1'
    Hden = [1]          # H(s) denominator polynomial coefficients.
    HdenStr = '1'
    Henable = False     # Flag to indicate if transfer function H(s) is enabled or not
    
    DLTF_r = ct.tf(1,1) # Open Loop Transfer Function for r input
    #CLTF_r = ct.tf(1,1) # Closed Loop Transfer Function for r input
    DLTF_poles = np.array([])
    DLTF_zeros = np.array([])
    DLTF_num_poly = np.poly1d([]) # Polynomial object for the Direct Loop transfer function numerator
    DLTF_den_poly = np.poly1d([]) # Polynomial object for the Direct Loop transfer function denominator
    #OLTF_w = ct.tf(1,1) # Open Loop Transfer Function for w input
    #CLTF_w = ct.tf(1,1) # Closed Loop Transfer Function for w input    
    
    TM = ct.tf(1,1) # Transfer Matrix (MIMO system)
    #TM = ct.tf(1,1) # Closed Loop Transfer Matrix (MIMO system)

    # Non linear system stuff:
    NLsysString = '0.7*self.u-0.7*numpy.square(y[0])'
    NLsysInputString = '0.7*U-0.7*numpy.square(Y)'

    Type = 0    # system type.
    Index = 0   # System index within a list.
    Name = ''
    TypeStrList = ['LTI_1','LTI_2', 'LTI_3']    # List with string for the system types.
    TypeStr = ''    # String with the current system type string.

    # Inputs (reference and perturbation):
    Rt_initStr = '0'    # String with the r(t) input function for initial segment.
    Rt_finalStr = '1'   # String with the r(t) input function for final segment.
    Rt_initValue = 0
    Rt_initType = 0     # Type of the r(t) function during initial period
    Rt_finalType = 0    # Type of the r(t) function during final period
    Rt_finalValue = 1
    InstRt = 0.0        # Time instant of r(t) changing.
    NoiseRt = 0.0       # Noise standard deviation for r(t) input.
    Wt_initStr = '0'    # String with the w(t) input function for initial segment.
    Wt_finalStr = '0'   # String with the w(t) input function for final segment.
    Wt_initValue = 0
    Wt_initType = 0     # Type of the w(t) function during initial period
    Wt_finalType = 0    # Type of the w(t) function during final period
    Wt_finalValue = 0
    InstWt = 0.0        # Time instant of w(t) changing.
    NoiseWt = 0.0       # Noise standard deviation for w(t) input.

    # Time simulation stuff:
    Delta_t = 0.005     # Time domain simulation time step value.
    Tmax = 10           # Time domain max simulation time.
    tfinal = 10         # Time domain simulation final time value.
    
    Loop = 'open'       # Feedback loop state (open or closed)
    Hide = False        # Hide system data (used for experimental system identification exercises)

    # Root Locus stuff:    
    Kmax = 10.0         # Max gain for root locus plot.
    Kmin = 0.0          # Min gain for root locus plot.
    Kpoints = 200       # Number of K point for root locus plot. 
    RL_root_vector = np.array([])   # Array that will contain the root locus data points.
    
    # Root locus forbidden regions paramethers:
    RL_FR_R = 0.0
    RL_FR_RI = 0.0
    RL_FR_I = 0.0
    
    # Bode diagram paramethers:
    Fmin = 0.01
    Fmax = 100.0
    Fpoints = 20
    
    # Nyquist plot paramethers:
    FminNyq = 0.01
    FmaxNyq = 100.0
    FpointsNyq = 100

    # System with discrete controller stuff:
    dT = 0.1        # Sample period
    Npts_dT = 20    # Number of points for each dT
    NdT = 100       # Number of discrete periods

    
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
    CurrentTimeSimId = -1
    #CurrentTimeSimIndex = -1       # An index for time simulation data. The LC3systems
                                    # object can store several simulations.
    TimeSimCounter = -1             # An absolute time simulation counter 
    # TimeSimData dictionary structure:
    #  key 'Name': a list containing the name of each simulation data
    #  Each name in the list will be a key in the dictionary. This key
    #  will contain also a dictionary with the following keys:
    #       'data' : a dictionary with the keys:
    #                'time' : time array
    #                'r(t)' : array of the reference input signal
    #                'w(t)' : array of the perturbation input signal
    #                'y(t)' : array of the main system output signal
    #                'u(t)' : array of the control action output signal
    #       'id' : the id number of the simulation
    #       'info' : a dictionary with the following keys:
    #  that contains the numpy arrays with the plotting data.
    TimeSimData = {'Name':[]}       # A Dictionary to store time simulation data.
    CurrentSimulName = ''

    # Frequency response data
    CurrentFreqResponseId = -1
    FreqResponseCounter = -1        # An absolute frequency response data counter
    FreqResponseData = {'Name':[]}  # A Dictionary to store frequency response data.
    CurrentFreqResponseName = ''

    def __init__(self,index,systype):
        """
        Init function. Updates
        """
        self.Type = systype
        self.Index = index
        #self.Name = '{i}: LTI_{t}'.format(i=index,t=systype)   # Format name string
        self.Name = 'SYS {i}'.format(i=index)   # Format name string
        self.TypeStr = self.TypeStrList[systype]
        self.updateSystem()
        self.clearTimeSimulData()
        self.clearFreqResponseData()
        self.RL_root_vector = np.array([])

    def updateSystem(self):
        """
        Update the system transfer functions (open and closed loop)
        according with the poynomial coefficients stored in
        the class properties Xnum and Xdem.

        For time domain simulation it is used a MIMO system
        Transfer Function object. The inputs are r(t) and w(t) 
        while outpus are y(t) and u(t)
        """
        self.N = self.Tmax/self.Delta_t
        self.G_tf = ct.tf(self.Gnum,self.Gden)
        self.C_tf = ct.tf(self.Cnum,self.Cden)
        self.H_tf = ct.tf(self.Hnum,self.Hden)

        # Compute the Direct Loop transfer functions accordingly with
        # the system type.
        if (self.Type == 0):
            self.DLTF_r = (self.G_tf * self.H_tf).minreal(0.0001)
            #self.CLTF_r = ((self.K * self.G_tf)/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
            #self.OLTF_w = ct.tf(1,1)
            #self.CLTF_w = (1/(1+self.K * self.G_tf * self.H_tf)).minreal(0.0001)
        elif (self.Type == 1):
            self.DLTF_r = (self.C_tf * self.G_tf * self.H_tf).minreal(0.0001)
            #self.CLTF_r = ((self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
            #self.OLTF_w = ct.tf(1,1)
            #self.CLTF_w = (1/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
        elif (self.Type == 2):
            self.DLTF_r = (self.C_tf * self.G_tf * self.H_tf).minreal(0.0001)
            #self.CLTF_r = ((self.K * self.C_tf * self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
        
        self.DLTF_poles = self.DLTF_r.poles()
        self.DLTF_zeros = self.DLTF_r.zeros()
        self.DLTF_num_poly = np.poly1d(self.DLTF_r.num[0][0])
        self.DLTF_den_poly = np.poly1d(self.DLTF_r.den[0][0])

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
        lg.debug('YR_tf numerator: {n}'.format(n=YR_tf.num))
        num = [[YR_tf.num[0][0],YW_tf.num[0][0]], [UR_tf.num[0][0],UW_tf.num[0][0]]] # array rows corresponds to outputs, columns to inputs
        den = [[YR_tf.den[0][0],YW_tf.den[0][0]], [UR_tf.den[0][0],UW_tf.den[0][0]]]
        lg.debug('Closed loop TF matrix numerator: {n}'.format(n=num))
        self.TM = ct.tf(num,den)


    def changeSystemType(self, newtype):
        # This method should do:
        #  Change CurrentSimulName
        #  Update the transfer matrix (if LTI)
        #  Add a new TimeSimData or overwrite the current one?
        if newtype <= 4:
            lg.debug('Changing system type to {t}'.format(t=newtype))
            self.Type = newtype
        else:
            lg.info('System type {t} no implemented yet!'.format(t=newtype))
    
    def clearTimeSimulData(self):
        """
        Clear all the time simulation data stored.
        """
        self.TimeSimData = {'Name':[]}
        self.CurrentSimulName = ''
        self.CurrentTimeSimId = -1
        self.TimeSimCounter = -1 


    def setAtiveTimeSimul(self,simulname):
        """
        Sets the current time simul data
        """
        if simulname in self.TimeSimData['Name']:
            lg.debug('Setting active simul in Sysname: {s} SimulName: {sm} List: {l}'.format(s=self.Name,sm=simulname,l=self.TimeSimData['Name']))
            self.CurrentSimulName = simulname
            self.CurrentTimeSimId = self.TimeSimData[simulname]['id']
        else:
            lg.info('Simulname {s} not found in TimeSimulData.'.format(s=simulname))

    def addSimul(self):

        self.TimeSimCounter = self.TimeSimCounter + 1
        # Format simul name string. The simulation number is 1 plus the last one:
        self.CurrentTimeSimId = self.TimeSimCounter
        self.CurrentSimulName = 'LTI_{t}:{i}'.format(t=self.Type,i=self.CurrentTimeSimId)
        self.TimeSimData['Name'].append(self.CurrentSimulName)
        self.TimeSimData[self.CurrentSimulName] = {}
        # Store this simul ID:
        self.TimeSimData[self.CurrentSimulName]['id'] = self.CurrentTimeSimId
        # Store this simul infos:
        self.TimeSimData[self.CurrentSimulName]['info'] = 'K = {k}'.format(k=self.K)
        
    
    def removeSimul(self, name):
        lg.debug('Removing simul {s} from sys index {i}'.format(s=name,i=self.Index))
        lg.debug('Simul names stored: {s}'.format(s=self.TimeSimData['Name']))
        # Find in wich position the removed data is in the dictionary:
        removedIdx = self.TimeSimData['Name'].index(name)

        # if the removed simulation data was the only one stored
        # resets the CurrentTimeSimIndex and TimeSimCounter.
        if not len(self.TimeSimData['Name']):
            #self.CurrentTimeSimIndex = -1
            self.TimeSimCounter = -1
        else: # simul to remove is not the only one.
            if self.CurrentSimulName == name:   # If the removed is the current one:
                # The new current data will be the prior one:
                lg.debug('Removing current selected simul:')
                lg.debug('Sysname: {s} SimulName: {sm} Index in the list: {i}'.format(s=self.Name,sm=name,i=removedIdx))
                self.CurrentSimulName = self.TimeSimData['Name'][removedIdx - 1]
                #print(self.TimeSimData)
                lg.debug('Current simul name: {n}'.format(n=self.CurrentSimulName))
                self.CurrentTimeSimId = self.TimeSimData[self.CurrentSimulName]['id'] # Gets the previous simuldataId.
                #self.CurrentTimeSimIndex = self.CurrentTimeSimIndex - 1
            #else: # If not, find the index of current SimulName in the list.
            #    self.CurrentTimeSimId = self.TimeSimData[self.CurrentSimulName]['id']
            #    currentIdx = self.TimeSimData['Name'].index(self.CurrentSimulName)

            # Updates the new current simulation data name:
            #self.CurrentSimulName = self.TimeSimData['Name'][self.CurrentTimeSimIndex]        
        self.TimeSimData['Name'].pop(removedIdx) # Remove the simulation name from the list.
        del self.TimeSimData[name] # Remove the data from the dictionary.

    def createInputVectors(self):
        """
        Create a time and an input vector from two strings representing
        any python mathematical function as a function of the variable t.        
        One string for the input r(t) and another for w(t)
        
        self.InstRt start instant of input r(t);
        self.InstWt start instant of input w(t).
        
        tinic = initial time.
        """
        
        if (self.InstRt > self.Tmax) or (self.InstWt > self.Tmax):
            lg.warning("Step time cannot be larger than Tmax.")
            return 0
        
        # Time vector:
        if (self.Type == 3):
            # For discrete simulation it is needed 2 more samples in input vector.
            time = np.arange(0,self.Tmax+2*self.Delta_t,self.Delta_t)
        else:
            time = np.arange(0,self.Tmax,self.Delta_t)
           
        r = np.zeros((len(time)))
        w = np.zeros((len(time)))
        self.N = len(time)
        #time = np.reshape(time,(1,len(time)))
        
        # Number of the sample corresponding to the begining of the inputs:
        sampleR = int(self.InstRt/self.Delta_t)
        sampleW = int(self.InstWt/self.Delta_t)
        
        # Create vector r(t):
        # r(t) initial part (between 0 and InstRt seconds):
        if (self.Rt_initType == 0): # 0 => Constant value.
            r[0:sampleR] = self.Rt_initValue
        elif (self.Rt_initType == 1): # 1 => Ramp 
            r[0:sampleR] = self.Rt_initValue * time[0:sampleR]
        elif (self.Rt_initType == 2): # 2 => Parabolic
            r[0:sampleR] = self.Rt_initValue * np.square(time[0:sampleR])
        elif (self.Rt_initType == 3): # 3 => Sin
            r[0:sampleR] = np.sin(2*np.pi*self.Rt_initValue*time[0:sampleR])
        elif (self.Rt_initType == 4): # 3 => Sin
            r[0:sampleR] = np.cos(2*np.pi*self.Rt_initValue*time[0:sampleR])
        else:
            lg.error('r(t) intial signal type {t} not recognized.'.format(t=self.Rt_initType))
        # r(t) final part (between InstRt and Tmax seconds):
        if (self.Rt_finalType == 0): # 0 => Constant value.
            r[sampleR:] = self.Rt_finalValue
        elif (self.Rt_finalType == 1): # 1 => Ramp 
            r[sampleR:] = self.Rt_finalValue * (time[sampleR:] - self.InstRt)
        elif (self.Rt_finalType == 2): # 2 => Parabolic
            r[sampleR:] = self.Rt_finalValue * np.square((time[sampleR:] - self.InstRt))
        elif (self.Rt_finalType == 3): # 3 => Sin
            r[sampleR:] = np.sin(2*np.pi*self.Rt_finalValue*(time[sampleR:] - self.InstRt))
        elif (self.Rt_finalType == 4): # 3 => Sin
            r[sampleR:] = np.cos(2*np.pi*self.Rt_finalValue*(time[sampleR:] - self.InstRt))
        else:
            lg.error('r(t) final signal type {t} not recognized.'.format(t=self.Rt_finalType))

        # Create vector w(t):
        # w(t) initial part (between 0 and InstWt seconds):
        if (self.Wt_initType == 0): # 0 => Constant value.
            w[0:sampleW] = self.Wt_initValue
        elif (self.Wt_initType == 1): # 1 => Ramp 
            w[0:sampleW] = self.Wt_initValue * time[0:sampleW]
        elif (self.Wt_initType == 2): # 2 => Parabolic
            w[0:sampleW] = self.Wt_initValue * np.square(time[0:sampleW])
        elif (self.Wt_initType == 3): # 3 => Sin
            w[0:sampleW] = np.sin(2*np.pi*self.Wt_initValue*time[0:sampleW])
        elif (self.Wt_initType == 4): # 3 => Sin
            w[0:sampleW] = np.cos(2*np.pi*self.Wt_initValue*time[0:sampleW])
        else:
            lg.error('r(t) intial signal type {t} not recognized.'.format(t=self.Wt_initType))
        # w(t) final part (between InstWt and Tmax seconds):
        if (self.Wt_finalType == 0): # 0 => Constant value.
            w[sampleW:] = self.Wt_finalValue
        elif (self.Wt_finalType == 1): # 1 => Ramp 
            w[sampleW:] = self.Wt_finalValue * (time[sampleW:] - self.InstWt)
        elif (self.Wt_finalType == 2): # 2 => Parabolic
            w[sampleW:] = self.Wt_finalValue * np.square((time[sampleW:] - self.InstWt))
        elif (self.Wt_finalType == 3): # 3 => Sin
            w[sampleW:] = np.sin(2*np.pi*self.Wt_finalValue*(time[sampleW:] - self.InstWt))
        elif (self.Wt_finalType == 4): # 3 => Sin
            w[sampleW:] = np.cos(2*np.pi*self.Wt_finalValue*(time[sampleW:] - self.InstWt))
        else:
            lg.error('r(t) final signal type {t} not recognized.'.format(t=self.Wt_finalType))

        # Creating Time Simulation Data with the inputs vectors:
        self.TimeSimData[self.CurrentSimulName]['data'] = {'time':time,'r(t)':r,'w(t)':w}

    def TimeSimulationTesting(self):
        """
        Temporary method only to test the UI and multiplot feature
        """
        self.createInputVectors()
        #time = np.arange(0,1,0.01)
        #y = np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time)
        #u = 2*np.sin(2*np.pi*np.random.uniform(low=1,high=10)*time+np.pi/2)
        #r = np.ones(len(time))
        #w = 0.5*np.ones(len(time))
        r = self.TimeSimData[self.CurrentSimulName]['data']['r(t)']
        y = self.TimeSimData[self.CurrentSimulName]['data']['r(t)'] * 2
        u = self.TimeSimData[self.CurrentSimulName]['data']['r(t)'] * 1.5

        e = r - y
        self.TimeSimData[self.CurrentSimulName]['data']['y(t)'] = y
        self.TimeSimData[self.CurrentSimulName]['data']['u(t)'] = u
        self.TimeSimData[self.CurrentSimulName]['data']['e(t)'] = e

    
    def TimeSimulation(self):
        """
        Performs a time domain simulation.
        """
        self.createInputVectors()
        T = self.TimeSimData[self.CurrentSimulName]['data']['time']
        U = np.append(np.reshape(self.TimeSimData[self.CurrentSimulName]['data']['r(t)'],(1,self.N)),np.reshape(self.TimeSimData[self.CurrentSimulName]['data']['w(t)'],(1,self.N)),axis=0)
        T,Y = ct.forced_response(self.TM,T,U,return_x=False)
        #print(np.shape(T))
        #print(np.shape(U))
        #print(np.shape(Y))
        self.TimeSimData[self.CurrentSimulName]['data']['y(t)'] = Y[0]
        self.TimeSimData[self.CurrentSimulName]['data']['u(t)'] = Y[1]
        self.TimeSimData[self.CurrentSimulName]['data']['e(t)'] = U[0]-Y[0]
    
    def RootLocus(self):
        """
        Calculate the root locus

        """

        #num = np.poly1d(self.OLTF_r.num[0][0]) #self.polyDnum
        #den = np.poly1d(self.OLTF_r.den[0][0]) #self.polyDden
        
        
        # Creating a gain vector (without the critical points):
        delta_k = (self.Kmax-self.Kmin) / self.Kpoints
        kvect = np.arange(self.Kmin,self.Kmax,delta_k)
        # Calculating the RL separation points by polynomial derivative:
        # d(-1/G(s))/ds = 0
        deriv = sp.polyder(self.DLTF_den_poly)*self.DLTF_num_poly - sp.polyder(self.DLTF_num_poly)*self.DLTF_den_poly
        cpss = sp.roots(deriv) # candidatos a ponto de separacao
        # Verificacao de quais os candidatos pertinentes
        for root in cpss:		
            aux = self.DLTF_num_poly(root)
            if aux != 0:
                Kc = -self.DLTF_den_poly(root) / self.DLTF_num_poly(root)
                if (np.isreal(Kc)) and (Kc <= self.Kmax) and (Kc >= self.Kmin):
                        #print(Kc)
                        kvect = np.append(kvect,Kc)
        # Reorder kvect:
        kvect = np.sort(kvect)
        # Calculate the roots:
        self.RL_root_vector = utils.MyRootLocus(self.DLTF_num_poly,self.DLTF_den_poly,kvect)

    def RLroots(self,K):
        """
        Calculate the roots of the characteristic equation, here given by
        the numerator and denominator of the direct loop transfer function.
        """
        
        # Characteristic equation:
        #  EqC = DL.den + K * DL.num
        EqC = self.DLTF_den_poly + K * self.DLTF_num_poly
        
        return EqC.roots

    def clearFreqResponseData(self):
        """
        Clear all the time simulation data stored.
        """
        self.FreqResponseData = {'Name':[]}
        self.FreqResponseName = ''
        self.CurrentFreqResponseId = -1
        self.FreqResponseCounter = -1 

    def setAtiveFreqResponse(self,name):
        """
        Sets the current frequency response data
        """
        if name in self.FreqResponseData['Name']:
            lg.debug('Setting active freq. response in Sysname: {s} SimulName: {sm} List: {l}'.format(s=self.Name,sm=name,l=self.FreqResponseData['Name']))
            self.CurrentFreqResponseName = name
            self.CurrentFreqResponseId = self.FreqResponseData[name]['id']
        else:
            lg.info('Freq. response name {s} not found in FreqResponseData.'.format(s=name))

    def addFreqResponse(self):
        self.FreqResponseCounter = self.FreqResponseCounter + 1
        # Format simul name string. The simulation number is 1 plus the last one:
        self.CurrentFreqResponseId = self.FreqResponseCounter
        self.CurrentFreqResponseName = 'LTI_{t}:{i}'.format(t=self.Type,i=self.CurrentFreqResponseId)
        self.FreqResponseData['Name'].append(self.CurrentFreqResponseName)
        self.FreqResponseData[self.CurrentFreqResponseName] = {}
        # Store this simul ID:
        self.FreqResponseData[self.CurrentFreqResponseName]['id'] = self.CurrentFreqResponseId
        # Store this simul infos:
        self.FreqResponseData[self.CurrentFreqResponseName]['info'] = 'K = {k}'.format(k=self.K)

    def removeFreqResponse(self, name):
        lg.debug('Removing freq response {s} from sys index {i}'.format(s=name,i=self.Index))
        lg.debug('Freq. response names stored: {s}'.format(s=self.TimeSimData['Name']))
        # Find in wich position the removed data is in the dictionary:
        removedIdx = self.FreqResponseData['Name'].index(name)

        # if the removed simulation data was the only one stored
        # resets the CurrentTimeSimIndex and TimeSimCounter.
        if not len(self.FreqResponseData['Name']):
            #self.CurrentTimeSimIndex = -1
            self.FreqResponseCounter = -1
        else: # simul to remove is not the only one.
            if self.CurrentFreqResponseName == name:   # If the removed is the current one:
                # The new current data will be the prior one:
                lg.debug('Removing current selected simul:')
                lg.debug('Sysname: {s} SimulName: {sm} Index in the list: {i}'.format(s=self.Name,sm=name,i=removedIdx))
                self.CurrentFreqResponseName = self.FreqResponseData['Name'][removedIdx - 1]
                #print(self.TimeSimData)
                lg.debug('Current simul name: {n}'.format(n=self.CurrentFreqResponseName))
                self.CurrentFreqResponseId = self.FreqResponseData[self.CurrentFreqResponseName]['id'] # Gets the previous simuldataId.
                #self.CurrentTimeSimIndex = self.CurrentTimeSimIndex - 1
            #else: # If not, find the index of current SimulName in the list.
            #    self.CurrentTimeSimId = self.TimeSimData[self.CurrentSimulName]['id']
            #    currentIdx = self.TimeSimData['Name'].index(self.CurrentSimulName)

            # Updates the new current simulation data name:
            #self.CurrentSimulName = self.TimeSimData['Name'][self.CurrentTimeSimIndex]        
        self.FreqResponseData['Name'].pop(removedIdx) # Remove the simulation name from the list.
        del self.FreqResponseData[name] # Remove the data from the dictionary.