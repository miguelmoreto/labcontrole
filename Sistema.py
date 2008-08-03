# -*- coding: iso-8859-1 -*- 
#
#
# Módulo onde é definida uma classe contendo um sistema de controle
# realimentado e métodos de simulação utilizando o módulo "Controls".
#
#
# *** Descrever o diagrama de blocos aqui. ***
#
# Desenvolvido por Miguel Moreto
#
from scipy import *
from scipy import signal
import controls
import types

class SistemaContinuo:
    """
    Classe que implementa um sistema contínuo com métodos para simulação.
    """
    Gnum = [2,10]   # Numerador de G(s).
    Gden = [1,2,10] # Denominador de G(s).
    Cnum = [1,1]      # Numerador de C(s).
    Cden = [1,2]      # Denominador de C(s).
    Hnum = [1]      # Numerador de H(s).
    Hden = [1]      # Denominador de H(s).

    
    Degrau = 1          # Amplitude do degrau de entrada.
    TempoDegrau = 0.5   # Instante de ocorrência do degrau.
    
    delta_t = 0.01  # Passo de simulação.
    
    Malha = 'Aberta' # Estado da malha (aberta ou fechada)
    
    def RespostaDegrau(self, tempo_degrau=0.5, delta_t=0.01, tmax=2,**kwargs):
        """
        Simulação da resposta ao degrau do sistema
        """
        
        S = self.SistemaR()
        
        y, t, u = S.step_response(fignum=None, dt=delta_t, maxt=tmax, 
                            step_time=tempo_degrau,**kwargs)
        
        return y, t, u
    
    def SistemaR(self):
        """
        Monta função de transferência do sistema em malha aberta ou fechada
        considerando como entrada r(t).
        """
        
        # FT do controlador:
        C = controls.TransferFunction(self.Cnum,self.Cden)
        
        # FT da planta:
        G = controls.TransferFunction(self.Gnum,self.Gden)
        
        # FT da realimentação:
        H = controls.TransferFunction(self.Hnum,self.Hden)
        
        if self.Malha == 'Aberta':
            return C*G
        else:
            S = C*G
            return S/(1.0 + H*S)
    
    def SistemaW(self):
        """
        Monta função de transferência do sistema em malha aberta ou fechada
        considerando com entrada w(t).
        """
        
        # FT do controlador:
        C = controls.TransferFunction(self.Cnum,self.Cden)
        
        # FT da planta:
        G = controls.TransferFunction(self.Gnum,self.Gden)
        
        # FT da realimentação:
        H = controls.TransferFunction(self.Hnum,self.Hden)
        
        if self.Malha == 'Aberta':
            return G
        else:
            return G/(1.0 + (H*C*G))
        
    def Simulacao(self, t, u, w, X0=0):
        """
        Simula um sistema dado as entradas u e w e um vetor de tempo qualquer
        para condições iniciais nulas (X0 = 0).
        """

        Sr = self.SistemaR() # Sistema considerando a entrada r(t)
        Sw = self.SistemaW() # Sistema considerando a entrada w(t)
        
        #y = signal.lsim(S, u, t, X0=None)[1]

        # Simula separadamente para cada entrada (superposição):
        try:
            yr = signal.lsim(Sr, u, t)[1]
        except:
            yr = signal.lsim2(Sr, u, t)[1]
            
        try:
            yw = signal.lsim(Sw, w, t)[1]
        except:
            yw = signal.lsim2(Sw, w, t)[1]
        
        return yr + yw
    
    def CriaEntrada(self, stringR, stringW, tmax=5,delta_t=0.01,tempoR=0.0, tempoW=0.0):
        """
        Cria um vetor de tempo e um de entrada a partir de duas strings
        representando qualquer função matemática do python em função da
        varíavel t.
        
        Uma string para a entrada r(t) e outra para w(t)
        
        tempoR = instante de início da entrada r(t);
        tempoW = instante de início da entrada w(t).
        """
        
        if (tempoR > tmax) or (tempoW > tmax):
            print "O tempo do degrau nao pode ser maior do que o tmax."
            return 0, 0, 0
        
        # Vetor de tempo:
        t_total = arange(0,tmax,delta_t)
           
        u = zeros_like(t_total)
        w = zeros_like(t_total)
        
        # Numero da amostra correspondente aos tempoR e tempoW:
        amostraR = int(tempoR/delta_t)
        amostraW = int(tempoW/delta_t)
        
        # monta vetor u(t):
        t = t_total[0:(len(t_total)-amostraR)]
        u[amostraR:] = eval(stringR)

        # monta vetor w(t)
        t = t_total[0:(len(t_total)-amostraW)]
        w[amostraW:] = eval(stringW)

       
        return t_total, u, w