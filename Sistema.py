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

class SistemaContinuo:
    """
    Classe que implementa um sistema contínuo com métodos para simulação.
    """
    Gnum = [2,10]   # Numerador de G(s).
    Gden = [1,2,10] # Denominador de G(s).
    Cnum = [1]      # Numerador de C(s).
    Cden = [1]      # Denominador de C(s).
    
    Degrau = 1          # Amplitude do degrau de entrada.
    TempoDegrau = 0.5   # Instante de ocorrência do degrau.
    
    delta_t = 0.01  # Passo de simulação.
    
    def RespostaDegrau(self, degrau=1.0, tempo_degrau=0.5, delta_t=0.01, tmax=2,figura=None,plotu=True):
        """
        Simulação da resposta ao degrau do sistema
        """
        
        tf = controls.TransferFunction(self.Gnum,self.Gden)
        
        y, t, u = tf.step_response(fignum=None, dt=delta_t, maxt=tmax, amp=degrau, 
                            fig=figura,step_time=tempo_degrau,plotu=plotu)
        
        return y, t, u
    