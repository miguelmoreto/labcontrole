# -*- coding: iso-8859-1 -*- 

__version__ ='$Rev: 34 $'
__date__ = '$LastChangedDate: 2008-09-03 19:57:10 -0300 (qua, 03 set 2008) $'

##    Este arquivo � parte do programa LabControle
##
##    LabControle � um software livre; voc� pode redistribui-lo e/ou 
##    modifica-lo dentro dos termos da Licen�a P�blica Geral GNU como 
##    publicada pela Funda��o do Software Livre (FSF); na vers�o 3 da 
##    Licen�a.
##
##    Este programa � distribuido na esperan�a que possa ser  util, 
##    mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUA��O a 
##    qualquer MERCADO ou APLICA��O EM PARTICULAR. Veja a Licen�a P�blica Geral
##    GNU para maiores detalhes.
##
##    Voc� deve ter recebido uma c�pia da Licen�a P�blica Geral GNU
##    junto com este programa, se n�o, escreva para a Funda��o do Software
##    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# $Author: miguelmoreto $
#
# M�dulo onde � definida uma classe contendo um sistema de controle
# realimentado e m�todos de simula��o utilizando o m�dulo "Controls".
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
    Classe que implementa um sistema cont�nuo com m�todos para simula��o.
    """
    Gnum = [2,10]   # Numerador de G(s).
    Gden = [1,2,10] # Denominador de G(s).
    Cnum = [1]      # Numerador de C(s).
    Cden = [1]      # Denominador de C(s).
    Hnum = [1]      # Numerador de H(s).
    Hden = [1]      # Denominador de H(s).

    # Entradas:
    Rt = '1'       # String com a fun��o de entrada r(t)
    InstRt = 0
    Wt = '0'       # String com a fun��o de entrada w(t)
    InstWt = 0

    delta_t = 0.01  # Passo de simula��o.
    
    Malha = 'Aberta' # Estado da malha (aberta ou fechada)
    
    K = 1.0 # Ganho do sistema.
    
    Kmax = 10.0 # Ganho m�ximo para o plot do LGR.
    Kmin = 0.0    # Ganho m�nimo para o plot do LGR.
    Kpontos = 200.0 # N�mero de pontos para o tra�ado do LGR. 
    
    # Par�metros das regi�es proibidas do LGR:
    Rebd = 0.0
    Ribd = 0.0
    Imbd = 0.0
    
    # Estados iniciais.
    X0r = None
    X0w = None

    def __init__(self):
        """
        Fun��o de inicializa��o. � executado ao instanciar a classe.
        """
        self.Atualiza()
        
        
    def Atualiza(self):
        """
        Atualiza fun��es de transfer�ncia do sistema realimentado.
        """
        
        # FT do controlador:
        self.C = controls.TransferFunction(self.Cnum,self.Cden)
        # FT da planta:
        self.G = controls.TransferFunction(self.Gnum,self.Gden)       
        # FT da realimenta��o:
        self.H = controls.TransferFunction(self.Hnum,self.Hden)
        
        return
    
    def RaizesRL(self,K):
        """
        C�lcula as ra�zes da equa��o caracter�stica (denominador do sist.
        realimentado) aqui representada em fun��o dos numeradores e denominadores
        da FT malha direta e H(s).
        """
        
        MD = self.C * self.G # FT da malha direta.
        
        # C�lculo da equa��o caracter�stica:
        EqC = MD.den * self.H.den + K * MD.num * self.H.num
        
        return EqC.roots 
        
    
    def RespostaDegrau(self, tempo_degrau=0.5, delta_t=0.01, tmax=2,**kwargs):
        """
        Simula��o da resposta ao degrau do sistema
        """
        
        S = self.SistemaR()
        
        y, t, u = S.step_response(fignum=None, dt=delta_t, maxt=tmax, 
                            step_time=tempo_degrau,**kwargs)
        
        return y, t, u
    
    def SistemaR(self):
        """
        Monta fun��o de transfer�ncia do sistema em malha aberta ou fechada
        considerando como entrada r(t).
        """
        
        if self.Malha == 'Aberta':
            return self.K*self.C*self.G
        else:
            S = self.K*self.C*self.G
            return S/(1.00000001 + self.H*S)
    
    def SistemaW(self):
        """
        Monta fun��o de transfer�ncia do sistema em malha aberta ou fechada
        considerando com entrada w(t).
        """
        
        if self.Malha == 'Aberta':
            return self.G
        else:
            return self.G/(1.000000001 + (self.K*self.H*self.C*self.G))
        
    def Simulacao(self, t, u, w, X0=0):
        """
        Simula um sistema dado as entradas u e w e um vetor de tempo qualquer
        para condi��es iniciais nulas (X0 = 0).
        """

        Sr = self.SistemaR() # Sistema considerando a entrada r(t)
        Sw = self.SistemaW() # Sistema considerando a entrada w(t)
        
        #y = signal.lsim(S, u, t, X0=None)[1]

        # Simula separadamente para cada entrada (superposi��o):
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
        
        # Armazena condi��es iniciais:
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
        representando qualquer fun��o matem�tica do python em fun��o da
        var�avel t.
        
        Uma string para a entrada r(t) e outra para w(t)
        
        tempoR = instante de in�cio da entrada r(t);
        tempoW = instante de in�cio da entrada w(t).
        
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

    def LGR(self,figura):
        """
        Fun��o para tra�ado do Lugar Geom�trico das Ra�zes
        
        kvect: Vetor dos ganhos;
        figura: refer�ncia a uma figura do Matplotlib.
        
        O LGR � tra�ado sempre com ganho K = 1.
        """
        
        
        # FT do controlador:
        C = controls.TransferFunction(self.Cnum,self.Cden)
        
        # FT da planta:
        G = controls.TransferFunction(self.Gnum,self.Gden)
        
        # FT da realimentacao:
        H = controls.TransferFunction(self.Hnum,self.Hden)
        
        # Ganho:
        K = 1
        
        S = K*C*G*H # A fazer: Mudar para inserir o H. (H inserido, verificar depois se esta certo)
        
        # Criando vetor de ganhos (sem os pontos cr�ticos).
        # Kmin, Kmax e numero de pontos s�o atributos desta classe.
        delta_k = (self.Kmax-self.Kmin) / self.Kpontos
        kvect = arange(self.Kmin,self.Kmax,delta_k)
        
        # Geracao dos pontos de separacao
        # Definicao dos polinomios do numerador e denominador
        nn = self.C.num * self.G.num * self.H.num
        dd = self.C.den * self.G.den * self.H.num
        # Fazendo d(-1/G(s))/ds = 0
        deriv = polyder(dd)*nn - polyder(nn)*dd
        cpss = roots(deriv) # candidatos a ponto de separacao
        # Verificacao de quais os candidatos pertinentes
        for raiz in cpss:		
                aux = dd(raiz)
                if aux != 0:
                        GG = nn(raiz) / dd(raiz)
                        Kc = -1/GG
                        if (isreal(Kc)) and (Kc <= self.Kmax) and (Kc >= self.Kmin):
                                kvect = append(kvect,Kc)
       
        # Reordena o kvect:
        kvect = sort(kvect);
        
        ganhos = S.RootLocus(kvect, figura, xlim=None, ylim=None)
        
        return ganhos
    
    def Bode(self,f,figura):
        """
        M�todo para tra�ado do diagrama de bode.
        
        f: Vetor de frequencias;
        figura: refer�ncia a uma figura do Matplotlib.
        """
        # Criando sistema da malha direta:
        G = self.K*self.C*self.G
        
        # Plotando o bode na figura:
        a=G.FreqResp(f,fig=figura)
        
        # Pega as inst�ncias dos axes da figura do Bode:
        [axMag,axFase] = figura.get_axes()
        
        axFase.grid(which='minor')
        axMag.grid(which='minor')
        
        axMag.set_ylabel('Magnitude [dB]')
        axFase.set_ylabel('Fase [graus]')
        axFase.set_xlabel('Frequencia [Hz]')
        
        axMag.set_title('Diagrama de Bode de K*C(s)*G(s)')

        print G.CrossoverFreq(f)
        print G.PhaseMargin(f)

        
        return
    