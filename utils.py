# -*- coding: utf-8 -*-
#from scipy import *
import scipy as sp
from numpy import array,arange
import numpy

def parseeqpoly(dados, listeq=[], expr_var='s') :
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
		eqt = numpy.poly1d([1])
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
			ichap = tt.find('^')
			if ichap != -1 :
				expoente = float(tt[ichap+1:])
				tt = tt[0:ichap]
			else : expoente = 1
			if tt.find(expr_var) > -1:
				if (int(expoente)-expoente) != 0:
					raise 'Erro 3 : ' + potencia
				if (expoente < 1):
					raise 'Erro 3 : ' + potencia				
				tt = tt.replace(expr_var,'')
				if tt != '':
					raise 'Erro 1 : ' + tt
				paux = numpy.poly1d([1,0])**int(expoente)
				if flagdiv:
					eqt = eqt / paux
				else:
					eqt = eqt * paux
			elif tt.find('#') > -1:
				i = tt.find('#')
				f = tt.find('#', i+1)
				if f == -1:
					raise 'Erro 2 : ' + tt
				idx = int(tt[i+1:f])
				if (int(expoente)-expoente) != 0:
					raise 'Erro 3 : ' + expoente
				if (expoente < 1):
					raise 'Erro 3 : ' + expoente					
				if flagdiv:
					eqt = eqt / (listeq[idx]**int(expoente))
				else:
					eqt = eqt * (listeq[idx]**int(expoente))
			else:				
				if flagdiv : 
					eqt = eqt / (float(tt.strip('/'))**expoente)
				else : 
					eqt = eqt * (float(tt)**expoente)				

			# if tt.find('s') > -1 :
			# 	if (int(expoente)-expoente) != 0 : raise 'Erro 3 : ' + potencia
			# 	if (expoente < 1) : raise 'Erro 3 : ' + potencia				
			# 	tt = tt.replace('s','')
			# 	if tt != '' : raise 'Erro 1 : ' + tt
			# 	paux = numpy.poly1d([1,0])**int(expoente)
			# 	if flagdiv : eqt = eqt / paux
			# 	else : eqt = eqt * paux
			# elif tt.find('#') > -1 :
			# 	i = tt.find('#')
			# 	f = tt.find('#',i+1)
			# 	if f == -1 : raise 'Erro 2 : ' + tt
			# 	idx = int(tt[i+1:f])
			# 	if (int(expoente)-expoente) != 0 : raise 'Erro 3 : ' + expoente
			# 	if (expoente < 1) : raise 'Erro 3 : ' + expoente					
			# 	if flagdiv : eqt = eqt / (listeq[idx]**int(expoente))
			# 	else : eqt = eqt * (listeq[idx]**int(expoente))
			# else :				
			# 	if flagdiv : 
			# 		eqt = eqt / (float(tt.strip('/'))**expoente)
			# 	else : 
			# 		eqt = eqt * (float(tt)**expoente)				
		retorno = retorno + sinal * eqt
	return retorno

def parseexpr(dados, expr_var='s') :	
	polys = []
	neq = 0
	dados = dados.replace(' ','').lower()
	i = dados.find('(')
	f = dados.find(')')
	if (i == -1) or (f == -1) :
		retorno = parseeqpoly(dados, expr_var=expr_var)
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
				polys.append(parseeqpoly(eqtemp, polys, expr_var=expr_var))				
				dados = dados.replace(eqoriginal,'#'+str(len(polys)-1)+'#')				
				i = dados.find('(')
			else :
				i = i2
		retorno = parseeqpoly(dados, polys, expr_var=expr_var)
		return retorno
	

def FreqResp(num,den,f,getcrossings=False) :	

	w = 2j*numpy.pi*f	
	fresp = num(w)/den(w)	
	dBmag = 20*numpy.log10(abs(fresp))
	phase = numpy.zeros(len(fresp))
	rnum = num.r
	rden = den.r	
	for I in range(len(w)) : phase[I] = sum(numpy.angle(w[I]-rnum))-sum(numpy.angle(w[I]-rden))

	if getcrossings :
		# Cruzamentos em magnitude (0dB) e fase correspondente
		crossmagidx = []
		lastsign = 20*numpy.log10(abs(fresp[0]))/abs(20*numpy.log10(abs(fresp[0])))
		ix = 1
		for item in fresp[1:] :
			mag = 20*numpy.log10(abs(item))
			if lastsign != (mag/abs(mag)) :	crossmagidx.append(ix)
			lastsign = (mag/abs(mag))
			ix = ix + 1
		crossfreqmag = []
		cfase = []
		for idx in crossmagidx :					
			fd = f[idx-1]
			vd = dBmag[idx-1]/abs(dBmag[idx-1])
			fu = f[idx]
			vu = dBmag[idx]/abs(dBmag[idx])
			aux = 1
			ct = 0
			while (ct < 50) and (abs(aux) > 1e-10) :
				fm = (fd+fu)/2
				aa = num(2j*numpy.pi*fm)/den(2j*numpy.pi*fm)
				aux = 20*numpy.log10(abs(aa))
				if vd == (aux/abs(aux)) :
					vd = aux/abs(aux)
					fd = fm
				else :
					vu = aux/abs(aux)
					fu = fm                        
				ct = ct + 1
			crossfreqmag.append(fm)			
			ph = (phase[idx]-phase[idx-1])/(f[idx]-f[idx-1]) * (fm-f[idx-1]) + phase[idx-1]
			if numpy.angle(aa) < 0 : 
				angx = numpy.floor((-1*ph)/(2*numpy.pi))
				cfase.append((numpy.angle(aa)-angx*2*numpy.pi)/numpy.pi*180)
			else : 
				angx = numpy.floor((-1*ph)/(2*numpy.pi))+1
				cfase.append((numpy.angle(aa)-angx*2*numpy.pi)/numpy.pi*180)
		
		if len(crossfreqmag) > 15 : 
			crossfreqmag = []
			cfase = []
		
			
		# Cruzamentos na fase e ganho correspondente
		crossfaseidx = []
		lastsign = ((phase[0])+numpy.pi)/abs(phase[0]+numpy.pi)
		ix = 1
		for item in phase[1:] :
			mfase = item+numpy.pi
			if lastsign != (mfase/abs(mfase)) :	crossfaseidx.append(ix)
			lastsign = (mfase/abs(mfase))
			ix = ix + 1
		crossfreqfase = []
		cmag = []
		for idx in crossfaseidx :		
			fd = f[idx-1]
			vd = (phase[idx-1]+numpy.pi)/abs(phase[idx-1]+numpy.pi)
			fu = f[idx]
			vu = (phase[idx]+numpy.pi)/abs(phase[idx]+numpy.pi)
			aux = 1
			ct = 0
			while (ct < 50) and (abs(aux) > 1e-10) :
				fm = (fd+fu)/2
				aa = num(2j*numpy.pi*fm)/den(2j*numpy.pi*fm)
				aux = numpy.angle(aa)+numpy.pi
				if vd == (aux/abs(aux)) :
					vd = aux/abs(aux)
					fd = fm
				else :
					vu = aux/abs(aux)
					fu = fm                        
				ct = ct + 1
			crossfreqfase.append(fm)
			cmag.append(20*numpy.log10(abs(aa)))
		
		if len(crossfreqfase) > 15 : 
			crossfreqfase = []
			cmag = []
		#print crossfreqfase
		#print cmag	
	
	if getcrossings is True : return dBmag, phase/numpy.pi*180, crossfreqmag, cfase, crossfreqfase, cmag
	else : return dBmag, phase
	
def Nyquist(num,den,f):
    w = 2j*numpy.pi*f	
    fresp = num(w)/den(w)
    preal = numpy.real(fresp)
    pimag = numpy.imag(fresp)	
    return preal, pimag
 
def MyRootLocus(num,den,kvect):
    
    """
    calculate the roots to draw the root locus
    
    num and den are poly1d numpy objects.
    """
    
    #Find the roots for the root locus:
    roots = []
    for k in kvect:
        curpoly = den+k*num
        curroots = curpoly.r
        curroots.sort()
        roots.append(curroots)
    mymat = numpy.row_stack(roots)
    # Sort the roots calculated above, so that the root
    # locus doesn't show weird pseudo-branches as roots jump from
    # one branch to another.
    sorted = numpy.zeros_like(mymat)
    for n, row in enumerate(mymat):
         if n==0:
             sorted[n,:] = row
         else:
             #sort the current row by finding the element with the
             #smallest absolute distance to each root in the
             #previous row
             available = list(range(len(numpy.prevrow)))
             for elem in row:
                 evect = elem-numpy.prevrow[available]
                 ind1 = abs(evect).argmin()
                 ind = available.pop(ind1)
                 sorted[n,ind] = elem
         numpy.prevrow = sorted[n,:]
    # sorted have the roots.
    return sorted

def RemoveEqualZeroPole(num, den, rtol=1e-5, atol=1e-10):
    """
    Remove, from the denominator and numerator the poles and zeros that are
    equals.
    """
    nroots = num.r.tolist()
    droots = den.r.tolist()
    
    ncoeff = num[len(num)] # higher order den coefficient
    dcoeff = den[len(den)] # higher order den coefficietn
    
    flag = 0
    n = 0
    while n < len(nroots):
        curn = nroots[n]
        ind = in_with_tol(curn, droots, rtol=rtol, atol=atol)
        if ind > -1:
            print("n: %d", n)
            print("ind: %d", ind)
            nroots.pop(n)
            droots.pop(ind)
            flag = 1
            #numpoly, rn = polydiv(numpoly, poly(curn))
            #denpoly, rd = polydiv(denpoly, poly(curn))
        else:
            n += 1
    if flag > 0:
        # When reconstruction polynomial numpy always return with high
        # order coefficient equal 1. So multiply by the original coef (gain)
        numcoeffs = numpy.poly(nroots) * ncoeff
        dencoeffs = numpy.poly(droots) * dcoeff
        nout = numpy.poly1d(numcoeffs)
        dout = numpy.poly1d(dencoeffs)
    else:
        nout = num
        dout = den

   
    return nout, dout

    
def in_with_tol(elem, searchlist, rtol=1e-5, atol=1e-10):
    """Determine whether or not elem+/-tol matches an element of
    searchlist."""
    for n, item in enumerate(searchlist):
       if numpy.allclose(item, elem, rtol=rtol, atol=atol):
            return n
    return -1
