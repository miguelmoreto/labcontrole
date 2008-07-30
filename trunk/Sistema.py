# -*- coding: iso-8859-1 -*- 
#
#
# M�dulo onde � definida uma classe contendo um sistema de controle
# realimentado e m�todos de simula��o utilizando o m�dulo "Controls".
#
#
# *** Descrever o diagrama de blocos aqui. ***
#
# Desenvolvido por Miguel Moreto
#
import controls

class SistemaContinuo:
    """
    Classe que implementa um sistema cont�nuo com m�todos para simula��o.
    """
    Gnum = [2,10]   # Numerador de G(s).
    Gden = [1,2,10] # Denominador de G(s).
    Cnum = [1]      # Numerador de C(s).
    Cden = [1]      # Denominador de C(s).
    
    Degrau = 1          # Amplitude do degrau de entrada.
    TempoDegrau = 0.5   # Instante de ocorr�ncia do degrau.
    
    delta_t = 0.01  # Passo de simula��o.
    
    def RespostaDegrau(self, degrau=1.0, tempo_degrau=0.5, delta_t=0.01, tmax=2,figura=None,plotu=True):
        """
        Simula��o da resposta ao degrau do sistema
        """
        
        tf = controls.TransferFunction(self.Gnum,self.Gden)
        
        y, t, u = tf.step_response(fignum=None, dt=delta_t, maxt=tmax, amp=degrau, 
                            fig=figura,step_time=tempo_degrau,plotu=plotu)
        
        return y, t, u
    