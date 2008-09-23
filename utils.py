from scipy import poly1d
from numpy import array

def parseeqpoly(dados,listeq=[]) :
	dados = dados.replace(' ','').lower()
	termos = []
	termostemp = dados.split('+')	
	for aux in termostemp :
		aux2 = aux.split('-');		
		if len(aux2) > 1 :
			i = 1
			for a in aux2[1:] :
				aux2[i] = '-' + aux2[i]
				i = i+1
		termos.extend(aux2)
	termostemp = termos
	retorno = 0
	for termosoma in termostemp :
		if termosoma == '' : continue
		eqt = poly1d([1])
		if termosoma.startswith('-') : 
			sinal = -1
			termosoma = termosoma.strip('-')
		else : sinal = 1
		tmultdiv = []
		for tmult in termosoma.split('*') :
			tdiv = tmult.split('/')
			if len(tdiv) > 1 :
				tmultdiv.append(tdiv[0])
				for aa in tdiv[1:] : tmultdiv.append('/'+aa)
			else :
				tmultdiv.append(tmult)					
		for tt in tmultdiv :
			if tt.startswith('/') :
				flagdiv = True
				tt = tt.strip('/')
			else : flagdiv = False
			if tt.find('#') > -1 :
				i = tt.find('#')
				f = tt.find('#',i+1)
				if f == -1 : raise 'Erro 2 : ' + tt
				idx = int(tt[i+1:f])
				if flagdiv : eqt = eqt / listeq[idx]
				else : eqt = eqt * listeq[idx]
			elif tt.find('s') > -1 :
				ichap = tt.find('^')
				if ichap == -1 : potencia = 1				
				else :
					potencia = int(tt[ichap+1:])
					tt = tt[0:ichap]
				tt = tt.replace('s','')
				if tt != '' : raise 'Erro 1 : ' + tt
				paux = []
				paux.append(1)
				while potencia > 0 : 
					paux.append(0)
					potencia = potencia - 1	
				if flagdiv : eqt = eqt / poly1d(paux)
				else : eqt = eqt * poly1d(paux)
			else :							
				if flagdiv : 
					eqt = eqt / float(tt.strip('/'))
				else : 
					eqt = eqt * float(tt)
		retorno = retorno + sinal * eqt
	return retorno

def parseexpr(dados) :	
	polys = [];
	neq = 0;
	dados = dados.replace(' ','').lower()
	i = dados.find('(');
	f = dados.find(')');
	if (i == -1) or (f == -1) :
		retorno = parseeqpoly(dados)
		return retorno
	else :		
		while i != -1 :
			f = dados.find(')',i+1)
			if (f == -1) : break
			i2 = dados.find('(',i+1)
			if (f < i2) or (i2 == -1) :
				eqtemp = dados[i:f+1]
				eqoriginal = eqtemp
				eqtemp = eqtemp.strip('()')				
				polys.append(parseeqpoly(eqtemp,polys))				
				dados = dados.replace(eqoriginal,'#'+str(len(polys)-1)+'#')				
				i = dados.find('(')
			else :
				i = i2
		retorno = parseeqpoly(dados,polys)
		return retorno
	
