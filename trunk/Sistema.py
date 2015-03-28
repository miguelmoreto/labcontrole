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
#from scipy import *
import scipy
from scipy import signal
import numpy
#import myControls
from utils import FreqResp,Nyquist, MyRootLocus, RemoveEqualZeroPole
import matplotlib.pyplot as plt
#import types
#import control

class SistemaContinuo:
    """
    Classe que implementa um sistema cont�nuo com m�todos para simula��o.
    """
    Gnum = [2,10]   # Numerador de G(s).
    GnumStr = '2*s+10'
    polyGnum = numpy.poly1d(Gnum)
    Gden = [1,2,10] # Denominador de G(s).
    GdenStr = '1*s^2+2*s+10'
    polyGden = numpy.poly1d(Gden)
    G2num = [1]
    polyG2num = numpy.poly1d(G2num)
    G2den = [1]
    polyG2den = numpy.poly1d(G2den)
    Cnum = [1]      # Numerador de C(s).
    CnumStr = '1'
    polyCnum = numpy.poly1d(Cnum)
    Cden = [1]      # Denominador de C(s).
    CdenStr = '1'
    polyCden = numpy.poly1d(Cden)
    Hnum = [1]      # Numerador de H(s).
    HnumStr = '1'
    polyHnum = numpy.poly1d(Hnum)
    Hden = [1]      # Denominador de H(s).
    HdenStr = '1'
    polyHden = numpy.poly1d(Hden)
    
    polyDnum = numpy.poly1d([1]) # numerator polynomial of the direct loop transfer function
    polyDden = numpy.poly1d([1]) # denominator polynomial of the direct loop transfer function

    Type = 0    # system type.
    Hide = False

    # Entradas:
    Rt = '1'       # String com a fun��o de entrada r(t)
    InstRt = 0.0
    ruidoRt = 0.0
    Wt = '0'       # String com a fun��o de entrada w(t)
    InstWt = 0.0
    ruidoWt = 0.0

    delta_t = 0.01  # Passo de simula��o.
    Tmax = 10   # Tempo m�ximo de simula��o
    
    Malha = 'Aberta' # Estado da malha (aberta ou fechada)
    
    K = 1.0 # Ganho do sistema.
    
    Kmax = 10.0 # Ganho m�ximo para o plot do LGR.
    Kmin = 0.0    # Ganho m�nimo para o plot do LGR.
    Kpontos = 200 # N�mero de pontos para o tra�ado do LGR. 
    
    # Par�metros das regi�es proibidas do LGR:
    Rebd = 0.0
    Ribd = 0.0
    Imbd = 0.0
    
    # Par�metros para o Diagrama de Bode:
    Fmin = 0.01
    Fmax = 100.0
    Fpontos = 20
    
    # Par�metros para o Diagrama de Nyquist:
    NyqFmin = 0.01
    NyqFmax = 100.0
    NyqFpontos = 100
    
    # Estados iniciais.
    X0r = None
    X0w = None
    
    #sysYR = control.tf([1],[1]) # Transfer function Y(s)/R(s)
    #sysYW = control.tf([1],[1]) # Transfer function Y(s)/W(s)

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
        #self.C = myControls.TransferFunction(self.Cnum,self.Cden)
        self.polyCnum = numpy.poly1d(self.Cnum)
        self.polyCden = numpy.poly1d(self.Cden)
        #self.tfC = control.tf(self.Cnum,self.Cden)
        # FT da planta:
        #self.G = myControls.TransferFunction(self.Gnum,self.Gden)
        self.polyGnum = numpy.poly1d(self.Gnum)
        self.polyGden = numpy.poly1d(self.Gden)

        self.polyG2num = numpy.poly1d(self.G2num)
        self.polyG2den = numpy.poly1d(self.G2den)
        
        #self.tfG = control.tf(self.Gnum,self.Gden)
        #self.tfG2 = control.tf(self.G2num,self.G2den)
        # FT da realimenta��o:
        #self.H = myControls.TransferFunction(self.Hnum,self.Hden)
        self.polyHnum = numpy.poly1d(self.Hnum)
        self.polyHden = numpy.poly1d(self.Hden)
        #self.tfH = control.tf(self.Hnum,self.Hden)

        # Direct loop numerator and denominator. Checking zeros equal to poles
        
        # Definicao dos polinomios do numerador e denominador
        num = self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum
        den = self.polyCden * self.polyGden * self.polyG2den * self.polyHden
        
        # Updating Direct Loop transfer function:
        self.polyDnum, self.polyDden = RemoveEqualZeroPole(num,den)
        
        
        return
    
    def RaizesRL(self,K):
        """
        C�lcula as ra�zes da equa��o caracter�stica (denominador do sist.
        realimentado) aqui representada em fun��o dos numeradores e denominadores
        da FT malha direta e H(s).
        """
        
        #MD = self.C * self.G # FT da malha direta.
        
        # C�lculo da equa��o caracter�stica:
        #EqC = MD.den * self.H.den + K * MD.num * self.H.num
        #EqC = (self.polyCden * self.polyGden * self.polyG2den *self.polyHden) + (K * self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum)
        EqC = self.polyDden + K * self.polyDnum
        
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
            num = self.K * self.polyCnum * self.polyGnum * self.polyG2num
            den = self.polyCden * self.polyGden * self.polyG2den
            return signal.lti(num.coeffs,den.coeffs)
        else:

            num = self.K * self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum
            den = (self.polyCden * self.polyGden * self.polyG2den * self.polyHden) + num
            return signal.lti(num.coeffs,den.coeffs)
    
    def SistemaW(self):
        """
        Monta fun��o de transfer�ncia do sistema em malha aberta ou fechada
        considerando com entrada w(t).
        """

        if self.Malha == 'Aberta':
            return signal.lti(self.polyG2num.coeffs,self.polyG2den.coeffs)
        else:
            num = self.polyG2num * self.polyCden * self.polyGden * self.polyHden
            den = (self.polyCden * self.polyGden * self.polyG2den * self.polyHden) + (self.K * self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum)
            return signal.lti(num.coeffs,den.coeffs)
        
    def Simulacao(self, t, u, w, X0=0):
        """
        Simula um sistema dado as entradas u e w e um vetor de tempo qualquer
        para condi��es iniciais nulas (X0 = 0).
        """

        Sr = self.SistemaR() # Sistema considerando a entrada r(t)
        Sw = self.SistemaW() # Sistema considerando a entrada w(t)


        # Simulation is done separately (input R and input W)
        # Simulating input R:
        T,youtR,xoutR = signal.lsim2(Sr, u, t,self.X0r,hmax=1)#, numpy.array([0,0]),full_output=0)
        # Set hmax=1 of odeint otherwise solver "do not see" when one delay the input.
        self.X0r = xoutR[-1]

        # Simulating input W:
        if (self.Type == 0 or self.Type == 1) and self.Malha == 'Aberta':
            # If system is LTI0 or LTI1 and with openloop, output due to W is equal to W.
            youtW = w
        else:
            # Set hmax=1 of odeint otherwise solver "do not see" when one delay the input.
            T,youtW,xoutW = signal.lsim2(Sw, w, t, self.X0w,hmax=1,full_output=0)
            # Store initial conditions:
            self.X0w = xoutW[-1]
        
        self.tfinal = t[-1]
        self.Rfinal = u[-1]
        self.Wfinal = w[-1]
        
        return youtR + youtW

    
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
        t_total = numpy.arange(tinic,tinic+tmax,self.delta_t)
           
        u = numpy.zeros_like(t_total)
        w = numpy.zeros_like(t_total)
        
        # Numero da amostra correspondente aos tempoR e tempoW:
        amostraR = int(tempoR/self.delta_t)
        amostraW = int(tempoW/self.delta_t)
        
        # monta vetor u(t):
        t = t_total[0:(len(t_total)-amostraR)]
        if (self.ruidoRt > 0):
            u[amostraR:] = eval(stringR) + numpy.random.normal(0,self.ruidoRt,(len(t_total)-amostraR))
        else:
            u[amostraR:] = eval(stringR)
        u[0:amostraR] = Rinic

        # monta vetor w(t)
        t = t_total[0:(len(t_total)-amostraW)]
        if (self.ruidoWt > 0):
            w[amostraW:] = eval(stringW) + numpy.random.normal(0,self.ruidoWt,(len(t_total)-amostraW))
        else:
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

        num = self.polyDnum
        den = self.polyDden
        
        # Criando vetor de ganhos (sem os pontos cr�ticos).
        # Kmin, Kmax e numero de pontos s�o atributos desta classe.
        delta_k = (self.Kmax-self.Kmin) / self.Kpontos
        kvect = numpy.arange(self.Kmin,self.Kmax,delta_k)
        
        # Geracao dos pontos de separacao
        # Fazendo d(-1/G(s))/ds = 0
        deriv = scipy.polyder(den)*num - scipy.polyder(num)*den
        cpss = scipy.roots(deriv) # candidatos a ponto de separacao
        # Verificacao de quais os candidatos pertinentes
        for raiz in cpss:		
            aux = num(raiz)
            if aux != 0:
                Kc = -den(raiz) / num(raiz)
                if (numpy.isreal(Kc)) and (Kc <= self.Kmax) and (Kc >= self.Kmin):
                        kvect = numpy.append(kvect,Kc)
        # Reordena o kvect:
        kvect = numpy.sort(kvect);
        
        # Calculate the roots:
        root_vector = MyRootLocus(num,den,kvect)
        
        # Ploting:
        figura.clf()
        ax = figura.add_subplot(111)
        # Open loop poles:
        poles = numpy.array(den.r)
        ax.plot(numpy.real(poles), numpy.imag(poles), 'x')
        # Open loop zeros:
        zeros = numpy.array(num.r)
        if zeros.any():
            ax.plot(numpy.real(zeros), numpy.imag(zeros), 'o')
        for col in root_vector.T:
            # Ploting the root locus.
            ax.plot(numpy.real(col), numpy.imag(col), '-')
        
        return root_vector
    
    def Bode(self,figura):
        """
        M�todo para tra�ado do diagrama de bode.
        
        figura: refer�ncia a uma figura do Matplotlib.
        
        O bode � tra�ado para frequencias de self.Fmin a self.Fmax com
        self.Fpontos por d�cada.
        """
        # Criando sistema da malha direta:
        Gnum = self.K * self.polyCnum * self.polyGnum * self.polyG2num
        Gden = self.polyCden * self.polyGden * self.polyG2den
        
        # Criando vetor de frequencias complexas.
        # Com o logspace, s�o necess�rios relativamente poucos pontos
        # para o gr�fico ficar bom.
        dec = numpy.log10(self.Fmax/self.Fmin) # N�mero de decadas;
        f = numpy.logspace(numpy.log10(self.Fmin),numpy.log10(self.Fmax),self.Fpontos*dec)
        
        # Calculando resposta em frequencia do sistema:
        #val = G.FreqResp(f,fignum=None,fig=None)
        
        #dBmag = 20*log10(abs(val))
        #fase = angle(val,1)
        dBmag,fase,crossfreqmag,cfase,crossfreqfase,cmag = FreqResp(Gnum,Gden,f,True)
                                        
        # Ajustando os valores da fase se der menor do que -180 ou maior do
        # que 180 graus (fun��o angle s� retorna valores entre -180 e +180).
        #for i in arange(1, fase.shape[0]):
        #    if abs(fase[i]-fase[i-1]) > 179:
        #        fase[i:] -= 360.        
        
        #figura.clf()
           
        # Plotando a magnitude:
        ax1 = figura.add_subplot(2,1,1)
        ax1.semilogx(f, dBmag)        
        ax1.semilogx([self.Fmin,self.Fmax],[0,0],'k--')
        ax1.grid(True)
        ax1.xaxis.grid(True, which='minor')
        # Plotando a fase:
        ax2 = figura.add_subplot(2,1,2, sharex=ax1)
        ax2.semilogx(f, fase)
        ax2.semilogx([self.Fmin,self.Fmax],[-180,-180],'k--')
        ax2.grid(True)
        ax2.xaxis.grid(True, which='minor')

        #[freq,index] = G.CrossoverFreq(f)
        
        #ax1.hold()
        #ax1.semilogx([f[index]],[dBmag[index]],'bo')
        #print G.PhaseMargin(f)
        ax2.semilogx(crossfreqmag,cfase,'ro')
        for I in range(len(crossfreqmag)) : ax2.semilogx([crossfreqmag[I],crossfreqmag[I]],[-180,cfase[I]],'r');
        ax1.semilogx(crossfreqfase,cmag,'ro')   
        for I in range(len(crossfreqfase)) : ax1.semilogx([crossfreqfase[I],crossfreqfase[I]],[0,cmag[I]],'r');
        
        return
    
    def Nyquist(self,figura,completo=False,comcirculo=False):
        """
        M�todo para tra�ado do diagrama de nyquist.

        figura: refer�ncia a uma figura do Matplotlib.

        O bode � tra�ado para frequencias de self.Fmin a self.Fmax com
        self.Fpontos por d�cada.
        """
        # Criando sistema da malha direta:
        #G = self.K*self.C*self.G
        Gnum = self.K * self.polyCnum * self.polyGnum * self.polyG2num
        Gden = self.polyCden * self.polyGden * self.polyG2den
        
        # Criando vetor de frequencias complexas.
        # Com o logspace, s�o necess�rios relativamente poucos pontos
        # para o gr�fico ficar bom.
        dec = numpy.log10(self.NyqFmax/self.NyqFmin) # N�mero de decadas;
        f = numpy.logspace(numpy.log10(self.NyqFmin),numpy.log10(self.NyqFmax),self.NyqFpontos*dec)
        
        preal,pimag = Nyquist(Gnum,Gden,f)
        
        # Plotando a magnitude:
        ax = figura.add_subplot(111)
        
        [linha1] = ax.plot(preal,pimag)
        if completo : [linha2] = ax.plot(preal,-1*pimag)        
        if comcirculo :
                circ = plt.Circle((0, 0), radius=1, color='r',fill=False)
                ax.add_patch(circ)
                #cx = numpy.arange(-1,1+0.025,0.025)
                #cy = numpy.zeros(len(cx))
                #ct = 0
                #for a in cx : 
                #        cy[ct] = numpy.sqrt(1-a*a)
                #        ct = ct+1
                #
                #ax.plot(cx,cy,':k')
                #ax.plot(cx,-1*cy,':k')
        
        xl = ax.get_xlim()
        yl = ax.get_ylim()
        if abs(xl[0]-xl[1]) < abs(yl[0]-yl[1]) : modx = abs(xl[0]-xl[1]) * 0.03                
        else : modx = abs(yl[0]-yl[1]) * 0.03        
        
        idxmaxvar = 0
        maxvar = 0
        for I in range(len(preal)-2) :
                if maxvar < abs(preal[I]-preal[I+1]) : 
                        maxvar = abs(preal[I]-preal[I+1])
                        idxmaxvar = I+1
                       
        idxmarcador = idxmaxvar

        #print (pimag[idxmarcador+1]-pimag[idxmarcador])
        #print (preal[idxmarcador+1]-preal[idxmarcador])
        angulo = numpy.arctan((pimag[idxmarcador]-pimag[idxmarcador-1])/(preal[idxmarcador]-preal[idxmarcador-1]))
        if (preal[idxmarcador+1]-preal[idxmarcador]) < 0 : angulo = numpy.pi + angulo 
        ang1 = angulo+numpy.pi-numpy.pi/9
        ang2 = angulo+numpy.pi+numpy.pi/9             
        ax.fill([preal[idxmarcador],preal[idxmarcador]+modx*numpy.cos(ang1),preal[idxmarcador]+modx*numpy.cos(ang2),preal[idxmarcador]],[pimag[idxmarcador],pimag[idxmarcador]+modx*numpy.sin(ang1),pimag[idxmarcador]+modx*numpy.sin(ang2),pimag[idxmarcador]],edgecolor=linha1.get_color(),facecolor=linha1.get_color())                
        if completo :                                        
                angulo = numpy.pi + numpy.arctan((-pimag[idxmarcador+1]+pimag[idxmarcador])/(preal[idxmarcador+1]-preal[idxmarcador]))   
                if (preal[idxmarcador+1]-preal[idxmarcador]) < 0 : angulo = numpy.pi + angulo 
                ang1 = angulo+numpy.pi-numpy.pi/9
                ang2 = angulo+numpy.pi+numpy.pi/9           
                ax.fill([preal[idxmarcador],preal[idxmarcador]+modx*numpy.cos(ang1),preal[idxmarcador]+modx*numpy.cos(ang2),preal[idxmarcador]],[-1*pimag[idxmarcador],-1*pimag[idxmarcador]+modx*numpy.sin(ang1),-1*pimag[idxmarcador]+modx*numpy.sin(ang2),-1*pimag[idxmarcador]],edgecolor=linha2.get_color(),facecolor=linha2.get_color())        
                        
        ax.grid(True)
        
       
        
        return