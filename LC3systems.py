# -*- coding: utf-8 -*-
#
#
# Class definitions for the system types used in LabControl 3.

import numpy as np
import control as ct
import scipy as sp
from scipy import signal
from scipy.integrate import odeint
import logging as lg
import utils
import matplotlib as mpl
import math

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

    #     Initial values:
    NL_e0 = 0.0                     # Initial error value (C(s) input)
    NL_y0 = np.array([0.0])         # Output initial value for 1 order system
    NL_X0 = [0]                     # C(s) LTI initial states.
    NL_y00 = np.array([0.0,0.0])    # Output initial value for 2 order system
    NL_N = 0                        # Number of samples

    Type = 0    # system type.
    Index = 0   # System index within a list.
    Name = ''
    TypeStrList = ['LTI_1','LTI_2', 'LTI_3', 'DTS', 'NLS']    # List with string for the system types.
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
    
    # Frequency Response stuff:
    FreqAuto = True
    Fmin = 0.01
    Fmax = 100.0
    Fpoints = 1000

    # System with discrete controller stuff:
    dT = 0.1        # Sample period
    NpdT = 20    # Number of points for each dT
    NdT = 100       # Number of discrete periods
    Umax = 0

    
    # Initial states:
    X0r = None
    X0w = None

    # Non linear system simulation stuff:
    NL_sysString = '0.7*u-0.7*np.square(y[0])'
    NL_sysInputString = '0.7*U-0.7*np.square(Y)'
    NL_order  = 1

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
    #       'id'   : the id number of the simulation
    #       'type' : System type number when the simulation was performed
    #       'loop' : Feedback loop status ('open' or 'closed')
    #       'info' : a string with some info.
    TimeSimData = {'Name':[]}       # A Dictionary to store time simulation data.
    CurrentSimulName = ''

    # Frequency response data
    CurrentFreqResponseId = -1
    FreqResponseCounter = -1        # An absolute frequency response data counter
    # Frequency response data structure:
    #  key 'Name': a list containing the name of each freq. response data
    #  Each name in the list will be a key in the dictionary. This key
    #  will contain also a dictionary with the following keys:
    #       'data'   : a dictionary for the bode data, with the keys:
    #                   'omega' : angular frequency array
    #                   'mag'   : array of the magnitude of the frequency response (not in dB)
    #                   'phase' : array of the phase of the frequency response (in radians)
    #       'nydata' : a dictionary for nyquist graph data, with the keys:
    #                   'omega'     : angular frequency array
    #                   'reg_re'    : regular portion of the curve (real part)
    #                   'reg_im'    : regular portion of the curve (imaginary part)
    #                   'scaled_re' : scaled portion of the curve (real part)
    #                   'scaled_im' : scaled portion of the curve (imaginary part)
    #                   'arrow_re'  : invisible curve for plotting the arrows (real part)
    #                   'arrow_im'  : invisible curve for plotting the arrows (imaginary part)
    #       'id'     : the id number of the freq response
    #       'info'   : a dictionary with the folowing keys:
    #                   'wLimits'  : a tuple with the Fmin and Fmax values.
    #                   'GM'       : Gain margin value
    #                   'wG'       : Gain crossing frequency value (rad/s)
    #                   'PM'       : Phase margin value
    #                   'wP'       : Phase crossing frequency value (rad/s)
    #                   'SMflag'   : Draw Stability Margins flag: True or False.
    FreqResponseData = {'Name':[]}  # The Dictionary to store frequency response data.
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
        elif (self.Type == 1 or self.Type == 2):
            self.DLTF_r = (self.C_tf * self.G_tf * self.H_tf).minreal(0.0001)
        
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
        elif (self.Type == 2):
            if (self.Loop == 'open'):   # Open Loop
                YR_tf = (self.K * self.C_tf * self.G_tf).minreal(0.0001)    # Y(s)/R(s) transfer function
                YW_tf = self.G_tf                                           # Y(s)/W(s) transfer function
                UR_tf = (self.K * self.C_tf).minreal(0.0001)                # U(s)/R(s) transfer function
                UW_tf = ct.tf(0,1)                                          # U(s)/W(s) transfer function
            else:   # Closed Loop
                YR_tf = ((self.K * self.C_tf * self.G_tf)/(1+self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                YW_tf = ((self.G_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                UR_tf = ((self.K * self.C_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf)).minreal(0.0001)
                UW_tf = (-(self.K * self.C_tf * self.G_tf * self.H_tf)/(1 + self.K * self.C_tf * self.G_tf * self.H_tf) ).minreal(0.0001)
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
            self.TypeStr = self.TypeStrList[newtype]
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
        if self.Type < 3:
            self.CurrentSimulName = 'LTI_{t}:{i}'.format(t=self.Type,i=self.CurrentTimeSimId)
        elif self.Type == 3:
            self.CurrentSimulName = 'DTS_{t}:{i}'.format(t=self.Type,i=self.CurrentTimeSimId)
        elif self.Type == 4:
            self.CurrentSimulName = 'NLS_{t}:{i}'.format(t=self.Type,i=self.CurrentTimeSimId)
        self.TimeSimData['Name'].append(self.CurrentSimulName)
        self.TimeSimData[self.CurrentSimulName] = {}
        # Store this simul ID:
        self.TimeSimData[self.CurrentSimulName]['id'] = self.CurrentTimeSimId
        # Store this simul system type:
        self.TimeSimData[self.CurrentSimulName]['type'] = self.Type
        # Store this simul feedback loop status:
        self.TimeSimData[self.CurrentSimulName]['loop'] = self.Loop
        # Store this simul infos:
        self.TimeSimData[self.CurrentSimulName]['info'] = 'K = {k}, {l} loop'.format(k=self.K, l= self.Loop)
    
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
            # For discrete time simulation, calculates the total number of
            # samples based on the number os discrete step time and the
            # value of Delta_t (solving time step).
            self.NdT = round(self.Tmax/self.dT)     # Number of discrete time steps.
            self.NpdT = round(self.dT/self.Delta_t) # Number of points per each time step.
            # For discrete simulation it is needed 2 more samples in input vector.
            #time = np.arange(0,self.NdT*self.NpdT*self.Delta_t+2*self.Delta_t,self.Delta_t)
            time = np.arange(0,self.NdT*self.NpdT*self.Delta_t,self.Delta_t)
            #time = np.arange(0,self.Tmax+2*self.Delta_t,self.Delta_t)
        else:
            time = np.arange(0,self.Tmax,self.Delta_t)

        self.N = len(time)   
        r = np.zeros(self.N)
        w = np.zeros(self.N)
        
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
    
    def TimeSimulation(self):
        """
        Performs a time domain simulation using a MIMO system:
            inputs r(t) and w(t)
            outputs y(t) and u(t)
        """
        self.createInputVectors()
        T = self.TimeSimData[self.CurrentSimulName]['data']['time']
        U = np.append(np.reshape(self.TimeSimData[self.CurrentSimulName]['data']['r(t)'],(1,self.N)),np.reshape(self.TimeSimData[self.CurrentSimulName]['data']['w(t)'],(1,self.N)),axis=0)
        T,Y = ct.forced_response(self.TM,T,U,return_x=False)
        self.TimeSimData[self.CurrentSimulName]['data']['y(t)'] = Y[0]
        self.TimeSimData[self.CurrentSimulName]['data']['u(t)'] = Y[1]
        self.TimeSimData[self.CurrentSimulName]['data']['e(t)'] = U[0]-Y[0]
        self.TimeSimData[self.CurrentSimulName]['info'] = 'K = {k}, {l} loop'.format(k=self.K, l= self.Loop)
    
    def discreteTimeSimulation(self):
        """
        Time simulation considering a C(z) discrete controler and a
        Zero Order Hold (ZOH). 
            self.dT is the discrete sample time.
        The idea is to solve the process (G(s)) as a step response
        at every dT seconds. The value of the step is the output
        of C(z).
        """

        self.createInputVectors()
        Total_Nsamples = self.NdT * self.NpdT
        #orderG = len(self.Gden)
        orderG = np.poly1d(self.Gden).order
        # Initial state vector:
        X0G = np.zeros(orderG)
        order_Cnum = len(self.Cnum) # b coeff. order
        order_Cden = len(self.Cden) # a coeff. order
        if (order_Cden > 1):
            a = np.delete(self.Cden,0)
        else:
            a = np.zeros(0)
        b = self.Cnum
        R0 = np.zeros(order_Cnum)
        Y0 = np.zeros(order_Cnum)
        U0 = np.zeros(order_Cden-1)
        E0 = np.zeros(order_Cnum)
        yk = 0 # initial value of the output

        t_plot = np.zeros(Total_Nsamples)
        u_k = np.zeros(self.NdT)
        y_plot = np.zeros(Total_Nsamples)
        u_plot = np.zeros(Total_Nsamples)
        e_plot = np.zeros(Total_Nsamples)
        e_k = np.zeros(self.NdT)
        t_step = np.arange(0,self.dT+self.Delta_t,self.Delta_t)
        t_k = np.zeros(self.NdT)
        
        for k in np.arange(0,self.NdT):
            R0[0] = self.TimeSimData[self.CurrentSimulName]['data']['r(t)'][k*self.NpdT]
            Wk = self.TimeSimData[self.CurrentSimulName]['data']['w(t)'][k*self.NpdT]
            Y0[0] = yk + Wk
            
            if (self.Loop == 'closed'):
                E0 = R0 - Y0
            else:
                E0 = R0
                
            e_k[k] = R0[0] - Y0[0]
            t_k[k] = k * self.dT
            # Controller diference equation:
            uk = self.K * np.dot(b,E0) - np.dot(a,U0)

            # Apply saturation (if enable):
            if self.Umax > 0:
                if (uk > self.Umax):
                    uk = self.Umax
                elif (uk < -self.Umax):
                    uk = -self.Umax
                else:
                    pass
            
            U = uk * np.ones(len(t_step)) # input vector   
            # Lsim2 returns the initial condition in the first element
            # of the resulting array. We simulate with an aditional
            # Delta_t. The last value is used only in the next discrete step.
            t_out,yout,xout = signal.lsim2((self.Gnum,self.Gden),U=U,T=t_step,X0=X0G)
            
            t_plot[((k*self.NpdT)):(((k+1)*self.NpdT))] = t_out[0:(self.NpdT)] + k*self.dT
            y_plot[((k*self.NpdT)):(((k+1)*self.NpdT))] = yout[0:(self.NpdT)] + self.TimeSimData[self.CurrentSimulName]['data']['w(t)'][((k*self.NpdT)):(((k+1)*self.NpdT))]
            u_plot[((k*self.NpdT)):(((k+1)*self.NpdT))] = uk
            if (self.Loop == 'closed'):
                e_plot[((k*self.NpdT)):(((k+1)*self.NpdT))] = self.TimeSimData[self.CurrentSimulName]['data']['r(t)'][((k*self.NpdT)):(((k+1)*self.NpdT))] - (yout[0:(self.NpdT)] +  self.TimeSimData[self.CurrentSimulName]['data']['w(t)'][((k*self.NpdT)):(((k+1)*self.NpdT))])
            else:
                e_plot[((k*self.NpdT)):(((k+1)*self.NpdT))] = self.TimeSimData[self.CurrentSimulName]['data']['r(t)'][((k*self.NpdT)):(((k+1)*self.NpdT))]
        
            yk = yout[-1] # Save the final output value. 
            X0G = xout[-1] # Save the final state.
            
            Y0 = np.roll(Y0,1)
            Y0[0] = yk
            E0 = np.roll(E0,1)
            R0 = np.roll(R0,1)
            if (order_Cden > 1):
                U0 = np.roll(U0,1)
                U0[0] = uk
            u_k[k] = uk
        
        self.TimeSimData[self.CurrentSimulName]['data']['tk'] = t_k
        self.TimeSimData[self.CurrentSimulName]['data']['y(t)'] = y_plot
        self.TimeSimData[self.CurrentSimulName]['data']['u(t)'] = u_plot
        self.TimeSimData[self.CurrentSimulName]['data']['e(t)'] = e_plot
        self.TimeSimData[self.CurrentSimulName]['data']['e[k]'] = e_k
    
    def inspectTimeSimulation(self, simulname):
        """
        Calculates relevant parameters of the simulation data given 
        by simulname.
        Returns:
            y_max = maximum value of the output
            y_final = final value of the output (mean value of the last 5% samples of the signal)
            e_final = final value of the error (mean value of the last 5% samples of the signal)
            e_final_diff = mean value of differences between one sample and the next
                            during the last 5% samples of the error signal. This is to check
                            if the error is in steady state (this value should be aprox. zero)
            u_max = maximum value of the control signal
        """
        y_max = np.amax(self.TimeSimData[simulname]['data']['y(t)'])
        y_final_array = self.TimeSimData[simulname]['data']['y(t)'][math.floor(self.N - self.N * 0.05):]
        e_final_array = self.TimeSimData[simulname]['data']['e(t)'][math.floor(self.N - self.N * 0.05):]
        e_final_diff = np.mean(np.diff(e_final_array)/self.Delta_t)  # A mean of derivatives. If it is 0, them the error is stable.
        y_final = np.mean(y_final_array)
        e_final = np.mean(e_final_array)
        u_max = np.amax(self.TimeSimData[simulname]['data']['u(t)'])
        return y_max, y_final, e_final, e_final_diff, u_max
    
    def RootLocus(self):
        """
        Calculate the root locus

        """
       
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

   
    def RLseparationPoints(self):
        """
        Calculate the separation points (and the corresponding gain)
        of the Root Locus separation points.
        """
        num = self.DLTF_num_poly
        den = self.DLTF_den_poly

        points = []        
        gains = []
        
        # Calculating d(-1/G(s))/ds = 0
        deriv = sp.polyder(den)*num - sp.polyder(num)*den
        cpss = sp.roots(deriv) # candidate points
        # Verifing which point are ok.
        for root in cpss:		
            aux = num(root)
            if aux != 0:
                Kc = -den(root) / num(root)
                if (np.isreal(Kc)):# and (Kc <= self.Kmax) and (Kc >= self.Kmin):
                    points.append(root)
                    gains.append(Kc)
        
        return points, gains

    def RLroots(self,K):
        """
        Calculate the roots of the characteristic equation, here given by
        the numerator and denominator of the direct loop transfer function.
        """
        
        # Characteristic equation:
        #  EqC = DL.den + K * DL.num
        EqC = self.DLTF_den_poly + K * self.DLTF_num_poly
        
        return EqC.roots

    def DLroots(self):
        """
        Return the roots of the direct loop transfer function.
        """
        return self.DLTF_den_poly.roots

    def DLzeros(self):
        """
        Return the roots of the direct loop transfer function.
        """
        return self.DLTF_num_poly.roots 

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
        # Store system type used:
        self.FreqResponseData[self.CurrentFreqResponseName]['type'] = self.Type
        # Store this simul infos:
        self.FreqResponseData[self.CurrentFreqResponseName]['info'] = {'K': self.K}
        self.FreqResponseData[self.CurrentFreqResponseName]['info'] = {'SMflag': False}

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
    
    def calcOmega(self):
        """
        Determine the omega vector for frequency response (Bode and Nyquist plots).
        Using internal Control module functions.
        """

        if self.FreqAuto: # If the omega range is set to automatic:
            omega,omega_given = ct.freqplot._determine_omega_vector(self.K * self.DLTF_r,omega_in = None, omega_limits = None, omega_num = self.Fpoints,Hz=True,feature_periphery_decades=2)
            self.Fmin = omega[0]/(2*np.pi)
            self.Fmax = omega[-1]/(2*np.pi)
        else:
            omega,omega_given = ct.freqplot._determine_omega_vector(self.K * self.DLTF_r,omega_in = None, omega_limits = [2*np.pi*self.Fmin,2*np.pi*self.Fmax], omega_num = self.Fpoints,Hz=True)

        return omega,omega_given

    def FreqResponse(self):
        """
        Calculates the frequency response of the Direct Loop Transfer Function DLTF_r
        """
        # Create the complex frequency vector.
        # With logspace, there are no need for a lot o points to obtaind a good
        # graphic.
        #dec = np.log10(self.Fmax/self.Fmin) # Number of decades;
        #f = np.logspace(int(np.log10(self.Fmin)),
        #                   int(np.log10(self.Fmax)),
        #                   int(self.Fpoints*dec))
        #omega = 2*np.pi*f
        #         

        omega,_ = self.calcOmega()

        mag, phase, omega = ct.frequency_response(self.K * self.DLTF_r,omega, squeeze=True)
        gm,pm,sm,wpc,wgc,wms = ct.stability_margins(self.K * self.DLTF_r,returnall=False)
        self.FreqResponseData[self.CurrentFreqResponseName]['data'] = {'omega': omega}
        self.FreqResponseData[self.CurrentFreqResponseName]['data']['mag'] = mag
        self.FreqResponseData[self.CurrentFreqResponseName]['data']['phase'] = ct.unwrap(phase)
        self.FreqResponseData[self.CurrentFreqResponseName]['info']['GM'] = gm
        self.FreqResponseData[self.CurrentFreqResponseName]['info']['wG'] = wgc
        self.FreqResponseData[self.CurrentFreqResponseName]['info']['PM'] = pm
        self.FreqResponseData[self.CurrentFreqResponseName]['info']['wP'] = wpc
        self.FreqResponseData[self.CurrentFreqResponseName]['info']['wLimits'] = (omega[0],omega[-1])
    
    def NyquistGraphLines(self):
        """
        Calculates the Nyquist plot lines.
            Regular: portion of the graph where the magnitude is below the limit.
            Scaled: portion with larger magnitude, rescaled to better fit the plot.
        """
        arrows = 1
        arrow_size = 8
        #arrow_style = config._get_param('nyquist', 'arrow_style', kwargs, None)
        indent_radius = 1e-6
        encirclement_threshold = 0.05
        indent_direction = 'right'
        indent_points = 50
        max_curve_magnitude = 20
        max_curve_offset = 0.02
        start_marker = 'o'
        start_marker_size = 4
        label_freq = None
        warn_encirclements = True
        warn_nyquist = True
        #primary_style = _['-', '-.']
        #mirror_style = _parse_linestyle('mirror_style', allow_false=True)

        omega,omega_range_given = self.calcOmega()
        # Store omega vector:
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata'] = {'omega': omega}
        sys = self.K * self.DLTF_r
        # do indentations in s-plane where it is more convenient
        splane_contour = 1j * omega
        splane_contour[0] = 0

        # Bend the contour around any poles on/near the imaginary axis
        # TODO: smarter indent radius that depends on dcgain of system
        # and timebase of discrete system.
        if indent_direction != 'none':
            if sys.isctime():
                splane_poles = sys.poles()
                splane_cl_poles = sys.feedback().poles()

            #
            # Check to make sure indent radius is small enough
            #
            # If there is a closed loop pole that is near the imaginary access
            # at a point that is near an open loop pole, it is possible that
            # indentation might skip or create an extraneous encirclement.
            # We check for that situation here and generate a warning if that
            # could happen.
            #
            for p_cl in splane_cl_poles:
                # See if any closed loop poles are near the imaginary axis
                if abs(p_cl.real) <= indent_radius:
                    # See if any open loop poles are close to closed loop poles
                    p_ol = splane_poles[
                        (np.abs(splane_poles - p_cl)).argmin()]

                    if abs(p_ol - p_cl) <= indent_radius and \
                       warn_encirclements:
                        lg.warning("Indented contour may miss closed loop pole; "
                            "consider reducing indent_radius to be less than "
                            f"{abs(p_ol - p_cl):5.2g}")

            #
            # See if we should add some frequency points near imaginary poles
            #
            for p in splane_poles:
                # See if we need to process this pole (skip if on the negative
                # imaginary axis or not near imaginary axis + user override)
                if p.imag < 0 or abs(p.real) > indent_radius or \
                   omega_range_given:
                    continue

                # Find the frequencies before the pole frequency
                below_points = np.argwhere(
                    splane_contour.imag - abs(p.imag) < -indent_radius)
                if below_points.size > 0:
                    first_point = below_points[-1].item()
                    start_freq = p.imag - indent_radius
                else:
                    # Add the points starting at the beginning of the contour
                    assert splane_contour[0] == 0
                    first_point = 0
                    start_freq = 0

                # Find the frequencies after the pole frequency
                above_points = np.argwhere(
                    splane_contour.imag - abs(p.imag) > indent_radius)
                last_point = above_points[0].item()

                # Add points for half/quarter circle around pole frequency
                # (these will get indented left or right below)
                splane_contour = np.concatenate((
                    splane_contour[0:first_point+1],
                    (1j * np.linspace(
                        start_freq, p.imag + indent_radius, indent_points)),
                    splane_contour[last_point:]))

            # Indent points that are too close to a pole
            for i, s in enumerate(splane_contour):
                # Find the nearest pole
                p = splane_poles[(np.abs(splane_poles - s)).argmin()]

                # See if we need to indent around it
                if abs(s - p) < indent_radius:
                    # Figure out how much to offset (simple trigonometry)
                    offset = np.sqrt(indent_radius ** 2 - (s - p).imag ** 2) \
                        - (s - p).real

                    # Figure out which way to offset the contour point
                    if p.real < 0 or (p.real == 0 and
                                      indent_direction == 'right'):
                        # Indent to the right
                        splane_contour[i] += offset

                    elif p.real > 0 or (p.real == 0 and
                                         indent_direction == 'left'):
                        # Indent to the left
                        splane_contour[i] -= offset

                    else:
                        raise ValueError("unknown value for indent_direction")

        # change contour to z-plane if necessary
        if sys.isctime():
            contour = splane_contour
        else:
            contour = np.exp(splane_contour * sys.dt)

        # Compute the primary curve
        resp = sys(contour)

        # Compute CW encirclements of -1 by integrating the (unwrapped) angle
        phase = -ct.unwrap(np.angle(resp + 1))
        encirclements = np.sum(np.diff(phase)) / np.pi
        count = int(np.round(encirclements, 0))

        # Let the user know if the count might not make sense
        if abs(encirclements - count) > encirclement_threshold and \
           warn_encirclements:
            lg.warning(
                "number of encirclements was a non-integer value; this can"
                " happen is contour is not closed, possibly based on a"
                " frequency range that does not include zero.")
        #
        # Make sure that the enciriclements match the Nyquist criterion
        #
        # If the user specifies the frequency points to use, it is possible
        # to miss enciriclements, so we check here to make sure that the
        # Nyquist criterion is actually satisfied.
        #

        # Count the number of open/closed loop RHP poles:
        if indent_direction == 'right':
            P = (sys.poles().real > 0).sum()
        else:
            P = (sys.poles().real >= 0).sum()
        Z = (sys.feedback().poles().real >= 0).sum()

        # Check to make sure the results make sense; warn if not
        if Z != count + P and warn_encirclements:
            lg.warning(
                "number of encirclements does not match Nyquist criterion;"
                " check frequency range and indent radius/direction")
        elif indent_direction == 'none' and any(sys.poles().real == 0) and \
                warn_encirclements:
            lg.warning(
                "system has pure imaginary poles but indentation is"
                " turned off; results may be meaningless")
        
        # Find the different portions of the curve (with scaled pts marked)
        reg_mask = np.logical_or(
            np.abs(resp) > max_curve_magnitude,
            splane_contour.real != 0)
        scale_mask = ~reg_mask \
            & np.concatenate((~reg_mask[1:], ~reg_mask[-1:])) \
            & np.concatenate((~reg_mask[0:1], ~reg_mask[:-1]))        
        # Rescale the points with large magnitude
        rescale = np.logical_and(
            reg_mask, abs(resp) > max_curve_magnitude)
        resp[rescale] *= max_curve_magnitude / abs(resp[rescale])
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['reg_re'] = np.ma.masked_where(reg_mask, resp.real)
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['reg_im'] = np.ma.masked_where(reg_mask, resp.imag)

        # Figure out how much to offset the curve: the offset goes from
        # zero at the start of the scaled section to max_curve_offset as
        # we move along the curve
        curve_offset = self._compute_curve_offset(resp, scale_mask, max_curve_offset)

        # Plot the scaled sections of the curve (changing linestyle)
        # Moreto: I am not using this feature of scaled points.
        x_scl = np.ma.masked_where(scale_mask, resp.real)
        y_scl = np.ma.masked_where(scale_mask, resp.imag)
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['scaled_re'] = x_scl * (1 + curve_offset)
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['scaled_im'] = y_scl * (1 + curve_offset)

        # Calculate the primary curve (invisible) for setting arrows:
        x, y = resp.real.copy(), resp.imag.copy()
        x[reg_mask] *= (1 + curve_offset[reg_mask])
        y[reg_mask] *= (1 + curve_offset[reg_mask])
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['arrow_re'] = x
        self.FreqResponseData[self.CurrentFreqResponseName]['nydata']['arrow_im'] = y
    
    #
    # Function to compute Nyquist curve offsets
    #
    # This function computes a smoothly varying offset that starts and ends at
    # zero at the ends of a scaled segment.
    # Function taken from Control module.
    def _compute_curve_offset(self, resp, mask, max_offset):
        # Compute the arc length along the curve
        s_curve = np.cumsum(
            np.sqrt(np.diff(resp.real) ** 2 + np.diff(resp.imag) ** 2))

        # Initialize the offset
        offset = np.zeros(resp.size)
        arclen = np.zeros(resp.size)

        # Walk through the response and keep track of each continous component
        i, nsegs = 0, 0
        while i < resp.size:
            # Skip the regular segment
            while i < resp.size and mask[i]:
                i += 1              # Increment the counter
                if i == resp.size:
                    break
                # Keep track of the arclength
                arclen[i] = arclen[i-1] + np.abs(resp[i] - resp[i-1])

            nsegs += 0.5
            if i == resp.size:
                break

            # Save the starting offset of this segment
            seg_start = i

            # Walk through the scaled segment
            while i < resp.size and not mask[i]:
                i += 1
                if i == resp.size:  # See if we are done with this segment
                    break
                # Keep track of the arclength
                arclen[i] = arclen[i-1] + np.abs(resp[i] - resp[i-1])

            nsegs += 0.5
            if i == resp.size:
                break

            # Save the ending offset of this segment
            seg_end = i

            # Now compute the scaling for this segment
            s_segment = arclen[seg_end-1] - arclen[seg_start]
            offset[seg_start:seg_end] = max_offset * s_segment/s_curve[-1] * \
                np.sin(np.pi * (arclen[seg_start:seg_end]
                                - arclen[seg_start])/s_segment)

        return offset

        
    def NLsysParseString(self, string):
        """
        Parse the string entered by user.
        The terms DY,Y and U will be substitued by y[1], y[0] and u 
        respectivelly.
        After susbstituion, the parsed string is evaluated using the temp
        vector y and value u. Is eval fails, this method returns 0, 
        otherwise returns 1.
        """
        
        sysstr = ''
        y = np.array([1,1]) # temp array to test the equation.
        u = 1.0
        self.NL_sysInputString = string

        sysstr = string.replace(',','.')
        sysstr = sysstr.replace('DY','y[1]')
        sysstr = sysstr.replace('Y','y[0]')
        sysstr = sysstr.replace('U','u')
        print(sysstr)
        # Test the parsed string:
        try:
            eval(sysstr)
            print('Eval OK')
        except:
            print('Erro eval')
            return 0
            
        if ('y[1]' in sysstr):
            self.NL_order = 2
            #print 'Ordem 2'
        elif ('y[0]' in sysstr):
            self.NL_order = 1
            #print 'Ordem 1'
        else:
            #print 'Not ODE'
            return 0            
        
        self.NL_sysString = sysstr
        return 1
        
    def NLsysODE1(self,y,t,u):
        """
        Non linear system ordinary differential equation of order 1.
        This is the callable function used by scipy.odeint
        """
        dy = eval(self.NL_sysString)
        return dy
    
    def NLsysODE2(self,y,t,u):
        """
        Non linear system ordinary differential equation of order 2.
        This is the callable function used by scipy.odeint
        """
        dy0 = y[1]
        dy1 = eval(self.NL_sysString)
        return np.array([dy0, dy1])

    def NLsysSimulation(self):
        """
        Calculates the response of the Non-linear system with a
        controller in series (C(s)).
        """

        self.createInputVectors()
        y_out = np.zeros(self.N)
        e_out = np.zeros(self.N)
        u_out = np.zeros(self.N)
        u = 0
        e0 = 0.0                      # Initial error value (C(s) input)
        y0 = np.array([0.0])          # Output initial value for 1 order system
        X0 = np.zeros(len(self.Cden)-1) # C(s) LTI initial states.
        y00 = np.array([0.0,0.0])     # Output initial value for 2 order system

        # Loop throughout each simiul step:
        for i in np.arange(0,self.N):
            # Input sample:
            Ri=self.TimeSimData[self.CurrentSimulName]['data']['r(t)'][i]
            # Calculates the error signal:
            if (self.Loop == 'closed'):
                e = self.K * (Ri - y0[0])
            else:
                e = self.K * Ri
            e_out[i] = e
            # Check if C(s) is defined.
            if (self.Cenable):
                # Solve one step of the C(s) differential equation:
                t, yc, xout = signal.lsim2((self.Cnum,self.Cden),np.array([e0,e]),np.array([0,self.Delta_t]),X0)
                u = yc[1]
                X0 = xout[1] # Save the last state.
            else:
                u = e
            u_out[i] = u
            e0 = e
            # Solve one step of the non-linear differential equation:
            if (self.NL_order == 1):
                y = odeint(self.NLsysODE1,y0[0],np.array([0,self.Delta_t]),args=(u,))
                y0[0]=y[1]
                y_out[i] = y[0]
            elif (self.NL_order == 2):
                y = odeint(self.NLsysODE2,y00,np.array([0,self.Delta_t]),args=(u,))
                y00 = y[1]
                y_out[i] = y[0][0]
            
        self.TimeSimData[self.CurrentSimulName]['data']['y(t)'] = y_out
        self.TimeSimData[self.CurrentSimulName]['data']['u(t)'] = u_out
        self.TimeSimData[self.CurrentSimulName]['data']['e(t)'] = e_out
