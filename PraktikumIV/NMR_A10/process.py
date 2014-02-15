from process_lib import *

import glob

import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')
    
def T0():
    data = np.genfromtxt('data/zmena_T0.txt')[1:]
    casy, intenzity = data.T
    intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
    print(intenzity)
    
    with open('output/T0_gnp.dat', 'w') as ofile:
        ofile.writelines(gnp(casy, intenzity))
    
    with open('output/T0_tab.tex', 'w') as ofile:
        ofile.writelines(tex(casy, intenzity))
    
    gamma = 2*math.pi*42.512990
    w0 = 2*math.pi*un.ufloat((18.305,0.001))
    B0 = w0/gamma
    with open('output/B0.tex', 'w') as ofile:
        ofile.write(print_un(B0).replace('$', ''))
def tau():
    data = np.genfromtxt('data/meranie_tau.txt')[1:]
    casy, intenzity = data.T
    intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
    with open('output/tau_gnp.dat', 'w') as ofile:
        ofile.writelines(gnp(casy, intenzity))
    
    with open('output/tau_tab.tex', 'w') as ofile:
        ofile.writelines(tex(casy, intenzity))
    gamma = 2*math.pi*42.512990
    omega = reload()
    omega = gnuplot_dict['omega']
    print(omega)
    B1 = omega/gamma
    print(B1)
    with open('output/B1.tex', 'w') as ofile:
        ofile.write(print_un(B1*1000).replace('$', ''))
        
def D2():
    data = np.genfromtxt('data/t2.txt')[1:]
    casy, intenzity = data.T
    intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
    with open('output/D2_gnp.dat', 'w') as ofile:
        ofile.writelines(gnp(casy, intenzity))
    
    with open('output/D2_tab.tex', 'w') as ofile:
        ofile.writelines(tex(casy, intenzity))

def statistika():
    subory = glob.glob('data/statistika/*')
    sqns = []
    pocty = []
    rozptyly = []
    for subor in subory:
        pocet_merani = int(subor.split('/')[2].split('.')[0])
        pocty.append(pocet_merani)
        data = np.genfromtxt(subor)
        frekv, amplituda = data.T
        
        vybrane_amplitudy = amplituda[abs(frekv)>20]
        amplituda = [un.ufloat((c, 0.0001)) for c in amplituda]

        sqn = 1/np.sqrt(pocet_merani)
        sqns.append(sqn)
        
        
        rozptyl = np.std(vybrane_amplitudy)
        rozptyly_jednotlive = (vybrane_amplitudy - np.mean(vybrane_amplitudy))**2

        #~ rozptyly.append(un.ufloat((rozptyl, (np.std(rozptyly_jednotlive)))))
        rozptyly.append((un.ufloat(mean_std(rozptyly_jednotlive)))**0.5)
        
        
    with open('output/stat_gnp.dat', 'w') as ofile:
        ofile.writelines(gnp(sqns, rozptyly))
    
    pocty, sqns, rozptyly = zip(*sorted(zip(pocty, ['%.3f'%sqn for sqn in sqns], rozptyly)))
    
    with open('output/stat_tab.tex', 'w') as ofile:
        ofile.writelines(tex(list(map(str, pocty)), sqns, [r*1e6 for r  in rozptyly]))
        
        
if __name__ == '__main__':
    T0()
    tau()
    D2()
    statistika()
    reload()
    T1 = gnuplot_dict['T1']
    T2 = gnuplot_dict['T2']
    with open('output/T1.tex', 'w') as ofile:
        ofile.write(print_un(T1).replace('$', ''))
    with open('output/T2.tex', 'w') as ofile:
        ofile.write(print_un(T2).replace('$', ''))
