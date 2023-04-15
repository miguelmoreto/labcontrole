import control as ct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys = ct.tf([2,10],[1,2,10])
FTMF = sys/(1+sys)
data = ct.step_response(sys,10)

topandas = {'time': data.time}
topandas.update({'u' : data.inputs})
topandas.update({'y' : data.outputs})
serie = pd.DataFrame(topandas)


fig,ax = plt.subplots(figsize=(6, 5),layout='constrained')
fig.suptitle('Grafico')

serie.plot(x='time',ax=ax)

#roots, gains = ct.root_locus(sys,kvect=np.linspace(0,20,100),plot=True,ax=ax)
plt.show()
