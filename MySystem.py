# -*- coding: iso-8859-1 -*- 
#==============================================================================
# This file is part of LabControle 2.
# 
# LabControle 2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# LabControle 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LabControle 2.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
#==============================================================================
# Este arquivo é parte do programa LabControle 2
# 
# LabControle 2 é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 3 da 
# Licença.
# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a 
# qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral
# GNU para maiores detalhes.
# 
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#==============================================================================
#
# by Miguel Moreto
# Florianopolis, Brazil, 2015
#
import scipy
from scipy import signal
from scipy.integrate import odeint
import numpy
from utils import FreqResp,Nyquist, MyRootLocus, RemoveEqualZeroPole
import matplotlib.patches as plt


class MySystem:
    """
    This class implements a LTI system with simulation methods.
    It also implements a Non-linear system and a LTI system with a discrete
    controller.
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
    Rt = '1'       # String com a função de entrada r(t)
    InstRt = 0.0
    ruidoRt = 0.0
    Wt = '0'       # String com a função de entrada w(t)
    InstWt = 0.0
    ruidoWt = 0.0
    
    RtVar = 0.0         # Input variation value.
    RtVarInstant = 0.0  # Input variation instant.

    delta_t = 0.005      # Simulation time step value.
    Tmax = 10           # Max simulation time.
    tfinal = 10
    
    Malha = 'Aberta' # Estado da malha (aberta ou fechada)
    
    K = 1.0             # System gain.
    
    Kmax = 10.0         # Max gain for root locus plot.
    Kmin = 0.0          # Min gain for root locus plot.
    Kpontos = 200       # Number of K point for root locus plot. 
    
    # Root locus forbidden regions paramethers:
    Rebd = 0.0
    Ribd = 0.0
    Imbd = 0.0
    
    # Bode diagram paramethers:
    Fmin = 0.01
    Fmax = 100.0
    Fpontos = 20
    
    # Nyquist plot paramethers:
    NyqFmin = 0.01
    NyqFmax = 100.0
    NyqFpontos = 100
    
    # Initial states:
    X0r = None
    X0w = None
    
    # Non-linear system atributes:    
    order = 1
    sysString = '0.7*self.u -0.7*numpy.square(y[0])'
    sysInputString = '0.7*U -0.7*numpy.square(Y)'
    u = 1.0                         # Non-linear system instantaneous input value.
    #     Initial values:
    e0 = 0.0                        # Initial error value (C(s) input)
    y0 = numpy.array([0.0])         # Output initial value for 1 order system
    X0 = [0]                        # C(s) LTI initial states.
    y00 = numpy.array([0.0,0.0])    # Output initial value for 2 order system
    N = 0                           # Number of samples
    
    # System with discrete controller atributes:
    dT = 0.1        # Sample period
    Npts_dT = 20    # Number of points for each dT

    def __init__(self):
        """
        Função de inicialização. É executado ao instanciar a classe.
        """
        self.Atualiza()
        self.N = self.Tmax/self.delta_t
        
    def Atualiza(self):
        """
        Update the feedback system
        """
        
        # C(s) controller TF polynomials:
        self.polyCnum = numpy.poly1d(self.Cnum)
        self.polyCden = numpy.poly1d(self.Cden)

        # Plant TF:
        # Polynomials of G(s) and G(s):
        self.polyGnum = numpy.poly1d(self.Gnum)
        self.polyGden = numpy.poly1d(self.Gden)
        self.polyG2num = numpy.poly1d(self.G2num)
        self.polyG2den = numpy.poly1d(self.G2den)

        # Polynomials of H(s):
        self.polyHnum = numpy.poly1d(self.Hnum)
        self.polyHden = numpy.poly1d(self.Hden)

        # Direct loop polynomials:
        num = self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum
        den = self.polyCden * self.polyGden * self.polyG2den * self.polyHden
        
        # Updating Direct Loop transfer function:
        self.polyDnum, self.polyDden = RemoveEqualZeroPole(num,den)
        return
        
    def RaizesRL(self,K):
        """
        Cálcula as raízes da equação característica (denominador do sist.
        realimentado) aqui representada em função dos numeradores e denominadores
        da FT malha direta e H(s).
        """
        
        #MD = self.C * self.G # FT da malha direta.
        
        # Cálculo da equação característica:
        #EqC = MD.den * self.H.den + K * MD.num * self.H.num
        #EqC = (self.polyCden * self.polyGden * self.polyG2den *self.polyHden) + (K * self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum)
        EqC = self.polyDden + K * self.polyDnum
        
        return EqC.roots 
        
    def RaizesOL(self):
        """
        Retorna as raízes de malha aberta.
        """
        return self.polyDden.roots
        
    def ZerosOL(self):
        """
        Retorna o valor dos zeros.
        """
        return self.polyDnum.roots
    
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
            num = self.K * self.polyCnum * self.polyGnum * self.polyG2num
            den = self.polyCden * self.polyGden * self.polyG2den
            return signal.lti(num.coeffs,den.coeffs)
        else:

            num = self.K * self.polyCnum * self.polyGnum * self.polyG2num * self.polyHnum
            den = (self.polyCden * self.polyGden * self.polyG2den * self.polyHden) + num
            return signal.lti(num.coeffs,den.coeffs)
    
    def SistemaW(self):
        """
        Monta função de transferência do sistema em malha aberta ou fechada
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
        para condições iniciais nulas (X0 = 0).
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

        
        return youtR + youtW

    def CriaEntrada(self, tinic=0.0,delta_t=0.01, Rinic = 0, Winic = 0):
        """
        Cria um vetor de tempo e um de entrada a partir de duas strings
        representando qualquer função matemática do python em função da
        varíavel t.
        
        Uma string para a entrada r(t) e outra para w(t)
        
        self.InstRt instante de início da entrada r(t);
        self.InstWt instante de início da entrada w(t).
        
        tinic = tempo inicial.
        """
        
        if (self.InstRt > self.Tmax) or (self.InstWt > self.Tmax):
            print "O tempo do degrau nao pode ser maior do que o tmax."
            return 0, 0, 0
        
        # Time vector:
        t_total = numpy.arange(tinic,tinic+self.Tmax,self.delta_t)
           
        u = numpy.zeros_like(t_total)
        w = numpy.zeros_like(t_total)
        
        # Number of the sanples corresponding to the begining of the inputs:
        amostraR = int(self.InstRt/self.delta_t)
        amostraW = int(self.InstWt/self.delta_t)
        
        # create vector u(t):
        #t = t_total[0:(len(t_total)-amostraR)]
        if (self.ruidoRt > 0):
            u[amostraR:] = eval(self.Rt) + numpy.random.normal(0,self.ruidoRt,(len(t_total)-amostraR))
            u[0:amostraR] = Rinic + numpy.random.normal(0,self.ruidoRt,amostraR)
        else:
            u[amostraR:] = eval(self.Rt)
            u[0:amostraR] = Rinic

        # create vector w(t)
        if (self.ruidoWt > 0):
            w[amostraW:] = eval(self.Wt) + numpy.random.normal(0,self.ruidoWt,(len(t_total)-amostraW))
        else:
            w[amostraW:] = eval(self.Wt)
        w[0:amostraW] = Winic

        if (self.RtVar != 0):
            Delta_u = numpy.zeros_like(t_total)
            Dusample = int(self.RtVarInstant/self.delta_t)
            Delta_u[Dusample:] = self.RtVar
            u = u + Delta_u

        #u[0] = Rinic
        #w[0] = Winic

        self.tfinal = t_total[-1]
        self.Rfinal = u[-1]
        self.Wfinal = w[-1]
       
        return t_total, u, w

    def LGR(self,figura):
        """
        Função para traçado do Lugar Geométrico das Raízes
        
        kvect: Vetor dos ganhos;
        figura: referência a uma figura do Matplotlib.
        
        O LGR é traçado sempre com ganho K = 1.
        """

        num = self.polyDnum
        den = self.polyDden
        
        # Criando vetor de ganhos (sem os pontos críticos).
        # Kmin, Kmax e numero de pontos são atributos desta classe.
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
    
    def PontosSeparacao(self):
        """
        Calcula os pontos de separação e retorna só os pertinentes.
        """
        num = self.polyDnum
        den = self.polyDden

        pontos = []        
        ganhos = []
        
        # Geracao dos pontos de separacao
        # Fazendo d(-1/G(s))/ds = 0
        deriv = scipy.polyder(den)*num - scipy.polyder(num)*den
        cpss = scipy.roots(deriv) # candidatos a ponto de separacao
        # Verificacao de quais os candidatos pertinentes
        for raiz in cpss:		
            aux = num(raiz)
            if aux != 0:
                Kc = -den(raiz) / num(raiz)
                if (numpy.isreal(Kc)):# and (Kc <= self.Kmax) and (Kc >= self.Kmin):
                    pontos.append(raiz)
                    ganhos.append(Kc)
        
        return pontos, ganhos
    
    def Bode(self,figura):
        """
        Método para traçado do diagrama de bode.
        
        figura: referência a uma figura do Matplotlib.
        
        O bode é traçado para frequencias de self.Fmin a self.Fmax com
        self.Fpontos por década.
        """
        # Criando sistema da malha direta:
        Gnum = self.K * self.polyCnum * self.polyGnum * self.polyG2num
        Gden = self.polyCden * self.polyGden * self.polyG2den
        
        # Criando vetor de frequencias complexas.
        # Com o logspace, são necessários relativamente poucos pontos
        # para o gráfico ficar bom.
        dec = numpy.log10(self.Fmax/self.Fmin) # Número de decadas;
        f = numpy.logspace(numpy.log10(self.Fmin),numpy.log10(self.Fmax),self.Fpontos*dec)
        
        # Calculando resposta em frequencia do sistema:
        #val = G.FreqResp(f,fignum=None,fig=None)
        
        #dBmag = 20*log10(abs(val))
        #fase = angle(val,1)
        dBmag,fase,crossfreqmag,cfase,crossfreqfase,cmag = FreqResp(Gnum,Gden,f,True)
                                        
        # Ajustando os valores da fase se der menor do que -180 ou maior do
        # que 180 graus (função angle só retorna valores entre -180 e +180).
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
        Método para traçado do diagrama de nyquist.

        figura: referência a uma figura do Matplotlib.

        O bode é traçado para frequencias de self.Fmin a self.Fmax com
        self.Fpontos por década.
        """
        # Criando sistema da malha direta:
        #G = self.K*self.C*self.G
        Gnum = self.K * self.polyCnum * self.polyGnum * self.polyG2num
        Gden = self.polyCden * self.polyGden * self.polyG2den
        
        # Criando vetor de frequencias complexas.
        # Com o logspace, são necessários relativamente poucos pontos
        # para o gráfico ficar bom.
        dec = numpy.log10(self.NyqFmax/self.NyqFmin) # Número de decadas;
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
        
    #==========================================================================
    # Non-linear system methods:
    #==========================================================================
    def NLsysReset(self):
        """
        Reset the initial conditions of the Non-linear system.
        """
        self.e = 0.0
        self.e0 = 0.0
        self.y0 = numpy.array([0.0])
        self.y00 = numpy.array([0.0, 0.0])
        self.X0 = [0]
        self.u = 0
        return
        
    def NLsysParseString(self, string):
        """
        Parse the string entered by user.
        The terms DY,Y and U will be substitued by y[1], y[0] and self.u 
        respectivelly.
        After susbstituion, the parsed string is evaluated using the temp
        vecto y. Is eval fails, this method returns 0, otherwise 1.
        """
        
        sysstr = ''
        y = numpy.array([1,1]) # temp array to test the equation.
        self.sysInputString = string

        sysstr = string.replace(',','.')
        sysstr = sysstr.replace('DY','y[1]')
        sysstr = sysstr.replace('Y','y[0]')
        sysstr = sysstr.replace('U','self.u')
        
        #print sysstr
        try:
            eval(sysstr)
            #print 'Eval OK'
        except:
            #print 'Erro eval'
            return 0
            
        if ('y[1]' in sysstr):
            self.order = 2
            #print 'Ordem 2'
        elif ('y[0]' in sysstr):
            self.order = 1
            #print 'Ordem 1'
        else:
            #print 'Not ODE'
            return 0            
        
        self.sysString = sysstr
        return 1
        
    def NLsysODE1(self,y,t):
        """
        Non linear system ordinary differential equation of order 1.
        This is the callable function used by scipy.odeint
        """
        dy = eval(self.sysString)
        return dy
    
    def NLsysODE2(self,y,t):
        """
        Non linear system ordinary differential equation of order 2.
        This is the callable function used by scipy.odeint
        """
        dy0 = y[1]
        dy1 = eval(self.sysString)
        return numpy.array([dy0, dy1])

    def NLsysSimulate(self,R):
        """
        R is the input vector.
        """

        y_out = numpy.zeros(self.N)

        for i in numpy.arange(0,self.N):
            # Calculates the error signal:
            if (self.Malha == 'Fechada'):
                e = self.K * (R[i] - self.y0[0])
            else:
                e = self.K * R[i]

            # Check if C(s) is defined.
            if (len(self.Cden) > 1):
                # Solve one step of the C(s) differential equation:
                t, yc, xout = signal.lsim((self.Cnum,self.Cden),numpy.array([self.e0,e]),numpy.array([0,self.delta_t]),self.X0)
                self.u = yc[1]
                self.X0 = xout[1] # Save the last state.
            else:
                self.u = e

            self.e0 = e
            # Solve one step of the non-linear differential equation:
            if (self.order == 1):
                y = odeint(self.NLsysODE1,self.y0[0],numpy.array([0,self.delta_t]))
                self.y0[0]=y[1]
                y_out[i] = y[0]
            elif (self.order == 2):
                
                y = odeint(self.NLsysODE2,self.y00,numpy.array([0,self.delta_t]))
                self.y00=y[1]
                
                y_out[i] = y[0][0]
            
        #self.tfinal = t[-1]
        #self.Rfinal = u[-1]
        #self.Wfinal = w[-1]
            
        return y_out        