from process_lib import *
from scipy.interpolate import interp1d
import glob
import itertools
import matplotlib.pyplot as plt
import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')


def find_inflex():
    ##nacitaj nulovy prud:
    data0 = np.genfromtxt('data/VA_0.00A.dat')
    data0j = np.genfromtxt('data/VA_0.00A_j.dat')
    
    U, I = data0j.T
    I_int = interp1d(U, I, kind='cubic')
    
    small_kody = ['0.35', '0.40', '0.50',  '0.60']
    for kod in small_kody:
        name = 'data/VA_%sA_j.dat'%kod
        data = np.genfromtxt(name)
        U, I = data.T
        I0 =I_int(U)
        plt.plot(U, np.gradient(I-I0))
        plt.show()
        print(I-I0)
    
import glob
def graf_spolu():
    subory = glob.glob('data/VA*A.dat')
    
    plot_command = ''
    
    plot_single = "'{sub}' with linespoints ls {i} ps 0.3 pt 4  {title}"
    
    singles = []

    def get_current(string):
        a = string.find('VA_')
        b = string.find('A.dat')
        return string[a+3:b]

    
    for i, subor in enumerate(sorted(subory)):
        singles.append((plot_single.format(sub=subor, title ="title"+"'$I\\di{mag} = %s \\unit A$'"%get_current(subor), i = i+1) ))
    
    for i, subor in enumerate(sorted(glob.glob('data/VA*A_j.dat'))):
        singles.append((plot_single.format(sub=subor, title ="notitle", i=i+1)))
    
    
    plot_command = 'plot '+',  '.join(singles)
    
    print (plot_command)


    
    print (get_current('data/VA_2.00A.dat'))
    
    with open('output/spolu.gnp', 'w') as ofile:
        ofile.write(plot_command)
        
def merny_naboj():
    data = np.genfromtxt('data/napatia.dat', skip_header=1, dtype='f8,f8,S4,f8,f8')
    I, dI, code, U, dU = zip(*data[1:])
    I = [un.ufloat((i, di)) for i, di in zip(I, dI)]
    U = [un.ufloat((u, du)) for u, du in zip(U, dU)]
    
    def pole(I):
        mu0 = 4*math.pi*1e-7
        N = 630
        rho0 = 75e-3
        return 8*mu0/(5*math.sqrt(5))*N*I/rho0
    
    B = [pole(i) for i in I]
    with open('output/napatia_p.dat', 'w') as ofile:
        ofile.writelines(gnp(B, U))
    with open('output/napatia_p.tex', 'w') as ofile:
        ofile.writelines(tex(I, [_*1000 for  _ in B], U))
    
    reload()
    a = gnuplot_dict['a']
    rA = 5e-3
    rK = 0.19e-3
    mn = a/( rA**2*(1-(rK/rA)**2)**2/8 )
    print (mn*1e-11)
    
    with open('output/c_mn.tex', 'w') as ofile:
        ofile.write(print_nice(mn*1e-11).replace('$', ''))

    index = 11
    U_chosen = 0
    I_magnetron = []
    for i, kod in zip(I,code):
        name = 'data/VA_%sA.dat'%kod.decode("utf-8")
        data = np.genfromtxt(name)
        U, I = data.T
        U_chosen = U[index]
        print(U_chosen)
        I_magnetron.append(I[index])
    with open('output/chosen.dat', 'w') as ofile:
        ofile.writelines(gnp(B, I_magnetron))

    with open('output/chosen.tex', 'w') as ofile:
        ofile.writelines(tex([_*1000 for  _ in B], ['%.2f'%(_*1e6) for  _ in I_magnetron]))
    with open('output/chosen_napatie.tex', 'w') as ofile:
        ofile.write('%.1f'%U_chosen)
if __name__ == '__main__':
    graf_spolu()
    #~ find_inflex()
    merny_naboj()
