from process_lib import *

import glob
import itertools

import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')

def peaky():
    data = np.genfromtxt('data/peaky.txt', usecols = (0, 1, 2, 3))
    #~ print (data)
    data =  np.array(sorted(data, key = lambda x: x[0]))
    #~ print (data)
    #vacsie neistoty
    data[0][1] = 0.01
    data[1][1] = 0.01
    data[2][1] = 0.01
    #~ print (data)
    
    p, dp, i, di = data.T
    
    positions = [ un.ufloat((p_, dp_)) for p_, dp_ in zip(p, dp)]
    intensities = [un.ufloat((i_, di_)) for i_, di_ in zip(i, di)]
    print (positions)
    
    lam = 1.54050
    
    def dhkl(theta, lam=lam):
        return lam/2/un.umath.sin(theta*math.pi/180)
    
    dhkls = [dhkl(pos/2) for pos in positions]
    #~ print ('\n'.join([str(_) for _ in dhkls]))
    Qis = [(dhkls[0]/dhkl_)**2 for dhkl_ in dhkls]
    print (Qis)

    Qis3 = [3*Q for Q in Qis]
    print (Qis3)
    
    with open('output/Qi.tex', 'w') as ofile:
        ofile.writelines(tex( positions, intensities, dhkls, [print_un_nopm(_, 2) for _ in Qis] ))
    print((3*list(range(4))))
    
    def odd_even(hkl):
        h, k, l = hkl
        return (h%2 == k%2) and (k%2 == l%2)
    triples = filter(odd_even, itertools.product(* (range(5), range(5), range(5))))
    sorted_triples = set([tuple(sorted(_, reverse=True)) for _ in triples])
    print(sorted_triples)
    
    hkls = [list() for _ in Qis]
    eps = 0.2
    for i, Qi in enumerate(Qis3):
        print (Qi)
        for triple in sorted_triples:
            h, k, l  = triple
            s = h**2 + k**2 + l**2
            if abs(s-Qi) < eps:
                hkls[i].append(triple)
                print (triple)
    print ((hkls))
    hkls = [_[0] for _ in hkls]
    hs, ks, ls = (list(zip(*hkls)))
    
    ahkls = [dhkl*(h**2+k**2+l**2)**0.5 for dhkl, h, k, l in zip(dhkls, hs, ks, ls)]
    
    with open('output/ahkl.tex', 'w') as ofile:
        ofile.writelines(tex( positions, [print_un_nopm(_, 2) for _ in Qis3], hs, ks, ls, ahkls))

    arg = [un.umath.cos(pos/2/180*math.pi)/un.umath.tan(pos/2/180*math.pi) for pos in positions]
    print (arg, ahkls)
    with open('output/kor.dat', 'w') as ofile:
        ofile.writelines(gnp(arg, ahkls))
    
    reload()
    a = gnuplot_dict['ae']
    print(a)
    with open('output/ae.tex', 'w') as ofile:
        ofile.write(print_un(a).replace('$', ''))
    
if __name__ == '__main__':
    peaky()
