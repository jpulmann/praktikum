from process_lib import *

import glob
import itertools

import numpy as np
import os

import skimage
import skimage.io

if not os.path.exists('output'):
    os.mkdir('output')

def dfs(image, start):
    neighbors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    visited = np.zeros(image.shape[:2], dtype=np.uint8)
    to_visit = [start]
    data = []
    while len(to_visit):
        cur_pos = to_visit.pop()
        ci, cj = cur_pos
        visited[ci, cj] = 1
        data.append(cur_pos[::-1])
        for neighbor in neighbors:
            #~ print ('asdfas', neighbor)
            i, j = neighbor+cur_pos
            if 0>i or image.shape[0]<=i:
                continue
            if 0>j or image.shape[1]<=j:
                continue

            #~ print(i, j)
            if not visited[i, j]:
                #~ print(image[i, j])
                if image[i, j, 0] < 128:
                    #~ print (i, j)
                    to_visit.append(neighbor + cur_pos)
    #~ skimage.io.imshow(visited)
    #~ skimage.io.show()
    
    return data

def kalibracia():
    name = 'data/stern_gerlach_bw_os.png'
    #~ image = skimage.io.imread(name)
    #~ skimage.io.imshow(image)
    #~ skimage.io.show()
    body = np.array([
        [1, 3333, 5],
        [2, 3334, 204],
        [3, 3333, 439],
        [4, 3336, 703],
        [5, 3337, 1017],
        [6, 3337, 1365],
        [7, 3339, 1739],
        [8, 3341, 2109],
        [9, 3343, 2446],
    ])
    otocka, X, Y = body.T
    with open('output/kalibracia.dat', 'w') as ofile:
        ofile.writelines(gnp(otocka, X, Y))
    reload()
    a = gnuplot_dict['a1']
    b = gnuplot_dict['b1']
    c = gnuplot_dict['c1']
    d = gnuplot_dict['d1']
    
    aa = gnuplot_dict['aa']
    bb = gnuplot_dict['bb']
    
    print (a, b, c, d )
    
    def otocenie(point):
        def ot_from_X(X):
            return a+b*X+c*X**2+d*X**3
        X_vector = np.array([1, aa])/(1+aa**2)**0.5
        X = point.dot(X_vector.T)
        y = np.sum((point - X*X_vector)**2)**0.5
        #~ print (X)
        return (ot_from_X(X), y)
        
    return otocenie
        
def obrazky(otocenie):
    starts = np.array([[3308, 61], 
                       [3186, 46], 
                       [2923, 49], 
                       [2633, 80], 
                       [2363, 55]])
    for i in range(5):
        name = 'data/stern_gerlach_bw_m%d.png'%i
        image = skimage.io.imread(name)
        data =  (dfs(image, starts[i]))
        ots = []
        ints = []
        print (len(data))
        for datum in data:
            ot, intenzita = otocenie(datum)
            #~ print (ot, intenzita)
            ots.append(ot)
            ints.append(intenzita)
        print( 'Zapisujem')
        with open('output/norm_s%d.dat'%i, 'w') as ofile:
            ofile.writelines(gnp(ots, ints))
        #~ break

def maxima():
    data = np.genfromtxt('data/maxima.dat')
    X1, dX1, X2, dX2, B, I = data.T
    X1 = [un.ufloat((u, du)) for u, du in zip(X1, dX1)]
    X2 = [un.ufloat((u, du)) for u, du in zip(X2, dX2)]
    B = [un.ufloat((b, 0.005)) for b in B]
    I = [un.ufloat((i, 5)) for i in I]
    
    

    
    alpha = 1.8e-3
    L = 70e-3
    l = 455e-3
    a = 2.5e-3
    T = un.ufloat((175, 2))+273.15
    
    def dBz(b):
        return 0.968*b/a
    
    ue = [alpha*(u2-u1)/2 for u1, u2 in zip(X1, X2)]
    print (ue)
    with open('output/tab_maxima.tex', 'w') as ofile:
        ofile.writelines(tex(
            list(map(str, range(1,5))), 
            I, 
            B,
            [dBz(b) for b in B],
            X1,
            X2,
            [_*1000 for _ in ue]
            ))

    D = alpha*un.ufloat((6.015-5.085, 0.01))/2
    p = alpha*(un.ufloat((5.764, 0.01)) - un.ufloat((5.589, 0.005)))/2
    
    with open('output/c_D.tex', 'w') as ofile:
        ofile.writelines(print_nice(D*1e6).replace('$', ''))
    with open('output/c_p.tex', 'w') as ofile:
        ofile.writelines(print_nice(p*1e6).replace('$', ''))
    
    print (D, p)
    
    C = (D**4-p**4/5)/(D**2-p**2/3)
    print('C=', C)
    
    kB = 1.38e-23
    prefaktorX = l*L*(1-L/2/l)
    prefaktorY = 2*kB*T
    X = [prefaktorX*dBz(b) for b in B]
    Y = [(3*u-C/u) for u in ue]

    
    print (ue)
    with open('output/tofit.dat', 'w') as ofile:
        ofile.writelines(gnp(X, Y))
    reload()    
    ub = 2*kB*T*gnuplot_dict['ub']
    with open('output/c_uB.tex', 'w') as ofile:
        ofile.writelines(print_nice(ub*1e24).replace('$', ''))
    ubb = un.ufloat((ub.nominal_value, ub.nominal_value*0.15))
    with open('output/c_uBB.tex', 'w') as ofile:
        ofile.writelines(print_un(ubb*1e24, 1).replace('$', ''))
        
if __name__ == '__main__':
    #~ otocenie = kalibracia()
    #~ obrazky(otocenie)
    
    
    
    output_constant('x0')
    maxima()
    

    
