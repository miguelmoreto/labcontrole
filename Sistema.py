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
import controls
from scipy import *
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
        
        S = self.Sistema()
        
        y, t, u = S.step_response(fignum=None, dt=delta_t, maxt=tmax, 
                            step_time=tempo_degrau,**kwargs)
        
        return y, t, u
    
    def Sistema(self):
        """
        Monta função de transferência do sistema em malha aberta ou fechada.
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
        
    def Simulacao(self, u, t,X0=0):
        """
        Simula um sistema dado uma entrada e vetor de tempo qualquer para
        condições iniciais nulas (X0 = 0).
        """
        
        S = self.Sistema()
        
        y = signal.lsim(S, u, t, interp=0, X0=X0)[1]
        
        return y
    
    def CriaEntrada(self, string, tmax=5,delta_t=0.01,tempo_inic=0.0):
        """
        Cria um vetor de tempo e um de entrada a partir de uma string
        representando qualquer função matemática do python em função da
        varíavel t.
        """
        
        if tempo_inic > tmax:
            print "O tempo do degrau nao pode ser maior do que o tmax."
            return 0, 0
        
        # Vetor de tempo:
        t_total = arange(0,tmax,delta_t)
           
        u = zeros_like(t_total)
        
        # Numero da amostra correspondente ao tempo_inic:
        amostra = int(tempo_inic/delta_t)

        t = t_total[0:(len(t_total)-amostra)]
        u[amostra:] = eval(string)
       
        return t_total, u