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
    Cnum = [1]      # Numerador de C(s).
    Cden = [1]      # Denominador de C(s).
    Hnum = [1]      # Numerador de H(s).
    Hden = [1]      # Denominador de H(s).

    # Entradas:
    Rt = '1'       # String com a função de entrada r(t)
    InstRt = 0
    Wt = '0'       # String com a função de entrada w(t)
    InstWt = 0

    delta_t = 0.01  # Passo de simulação.
    
    Malha = 'Aberta' # Estado da malha (aberta ou fechada)
    
    K = 1.0 # Ganho do sistema.
    
    Kmax = 10.0 # Ganho máximo para o plot do LGR.
    
    # Parâmetros das regiões proibidas do LGR:
    Rebd = 0.0
    Ribd = 0.0
    Imbd = 0.0
    
    # Estados iniciais.
    X0r = None
    X0w = None

    def __init__(self):
        """
        Função de inicialização. É executado ao instanciar a classe.
        """
        self.Atualiza()
        
        
    def Atualiza(self):
        """
        Atualiza funções de transferência do sistema realimentado.
        """
        
        # FT do controlador:
        self.C = controls.TransferFunction(self.Cnum,self.Cden)
        # FT da planta:
        self.G = controls.TransferFunction(self.Gnum,self.Gden)       
        # FT da realimentação:
        self.H = controls.TransferFunction(self.Hnum,self.Hden)
        
        return
    
    def RaizesRL(self,K):
        """
        Cálcula as raízes da equação característica (denominador do sist.
        realimentado) aqui representada em função dos numeradores e denominadores
        da FT malha direta e H(s).
        """
        
        MD = self.C * self.G # FT da malha direta.
        
        # Cálculo da equação característica:
        EqC = MD.den * self.H.den + K * MD.num * self.H.num
        
        return EqC.roots 
        
    
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
        
        if self.Malha == 'Aberta':
            return self.K*self.C*self.G
        else:
            S = self.K*self.C*self.G
            return S/(1.0 + self.H*S)
    
    def SistemaW(self):
        """
        Monta função de transferência do sistema em malha aberta ou fechada
        considerando com entrada w(t).
        """
        
        if self.Malha == 'Aberta':
            return self.G
        else:
            return self.G/(1.0 + (self.K*self.H*self.C*self.G))
        
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
            yr = signal.lsim(Sr, u, t, self.X0r)
        except:
            yr = signal.lsim2(Sr, u, t, self.X0r)
            
        try:
            yw = signal.lsim(Sw, w, t, self.X0w)
        except:
            yw = signal.lsim2(Sw, w, t, self.X0w)
        
        Xr = yr[-1]
        Xw = yw[-1]
        
        # Armazena condições iniciais:
        self.X0r = Xr[-1]
        self.X0w = Xw[-1]
        
        self.tfinal = t[-1]
        self.Rfinal = u[-1]
        self.Wfinal = w[-1]
        #print self.X0r, self.X0w, self.tfinal

        
        return yr[1] + yw[1]

    
    def CriaEntrada(self, stringR, stringW, tinic=0.0, tmax=5,delta_t=0.01,\
                    tempoR=0.0, tempoW=0.0, Rinic = 0, Winic = 0):
        """
        Cria um vetor de tempo e um de entrada a partir de duas strings
        representando qualquer função matemática do python em função da
        varíavel t.
        
        Uma string para a entrada r(t) e outra para w(t)
        
        tempoR = instante de início da entrada r(t);
        tempoW = instante de início da entrada w(t).
        
        tinic = tempo inicial.
        """
        
        if (tempoR > tmax) or (tempoW > tmax):
            print "O tempo do degrau nao pode ser maior do que o tmax."
            return 0, 0, 0
        
        # Vetor de tempo:
        t_total = arange(tinic,tinic+tmax,delta_t)
           
        u = zeros_like(t_total)
        w = zeros_like(t_total)
        
        # Numero da amostra correspondente aos tempoR e tempoW:
        amostraR = int(tempoR/delta_t)
        amostraW = int(tempoW/delta_t)
        
        # monta vetor u(t):
        t = t_total[0:(len(t_total)-amostraR)]
        u[amostraR:] = eval(stringR)
        u[0:amostraR] = Rinic

        # monta vetor w(t)
        t = t_total[0:(len(t_total)-amostraW)]
        w[amostraW:] = eval(stringW)
        w[0:amostraW] = Winic

       
        return t_total, u, w

    def LGR(self,kvect,figura):
        """
        Função para traçado do Lugar Geométrico das Raízes
        
        kvect: Vetor dos ganhos;
        figura: referência a uma figura do Matplotlib.
        
        O LGR é traçado sempre com ganho K = 1.
        """
        
        
        # FT do controlador:
        C = controls.TransferFunction(self.Cnum,self.Cden)
        
        # FT da planta:
        G = controls.TransferFunction(self.Gnum,self.Gden)
        
        # Ganho:
        K = 1
        
        S = K*C*G
        
        ganhos = S.RootLocus(kvect, figura, xlim=None, ylim=None)
        
        return ganhos
    