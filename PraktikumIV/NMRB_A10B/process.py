from process_lib import *

import glob

import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')

def T1():
    
    GNP_TEMPLATE = """
f{i}(x) = A_0{i} * abs(1 - 2*exp(-x/T1_{i}))
A_0{i} = 0.1
T1_{i} = {T0}
fit f{i}(x) 'output/t1_{i}.dat' via A_0{i}, T1_{i}

print 'A_0{i} ', A_0{i}, A_0{i}_err
print 'T1_{i} ', T1_{i}, T1_{i}_err
"""
    gnp_command = ''
    tab_tup = ()
    for i in range(6):
        filename = 'data/%d_t1.txt'%i
        print(filename)
        data = np.genfromtxt(filename, delimiter='\t', skip_header=1)
        casy, intenzity = data.T
        intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
        tab_tup += (casy, [print_un_nopm(val) for val in intenzity] )
        with open('output/t1_%d.dat'%i, 'w') as ofile:
            ofile.writelines(gnp(casy, intenzity))
        
        with open('output/t1_%d.tex'%i, 'w') as ofile:
            ofile.writelines(tex(casy, intenzity))
    
        gnp_command += GNP_TEMPLATE.format(i=i, T0=4*2**i)
        
    with open('output/T1_all_tab.tex', 'w') as ofile:
        ofile.writelines(tex(*tab_tup))
    gnp_command += """
plot """
    for i in range(6):
        gnp_command += """ 'output/t1_{i}.dat' with yerrorbars ls {ip} lw 3 ps 2.3 pt 8 title '$c_{i}$', f{i}(x) ls {ip} notitle, """.format(i=i, ip=i+1)
    
    with open('output/T1_graph_all.gnp', 'w') as ofile:
        ofile.write(gnp_command)
    
    print (gnp_command)
    reload()
    iss = [str(i) for i in range(6)]
    As = [gnuplot_dict['A_0%d'%i] for i in range(6)]
    T1s = np.array([gnuplot_dict['T1_%d'%i] for i in range(6)])
    
    with open('output/T1c.dat', 'w') as ofile:
        ofile.writelines(gnp(1/2**np.arange(6), T1s, 1000*T1s**(-1), As))
    
    with open('output/T1c.tex', 'w') as ofile:
        ofile.writelines(tex(iss, T1s, 1000*T1s**(-1), As))
        
        
    data = np.genfromtxt('data/t1guma.txt', delimiter='\t', skip_header=1)
    casy, intenzity = data.T
    intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
    tab_tup += (casy, [print_un_nopm(val) for val in intenzity] )
    with open('output/t1guma.dat', 'w') as ofile:
        ofile.writelines(gnp(casy, intenzity))
    
    with open('output/t1guma.tex', 'w') as ofile:
        ofile.writelines(tex(casy, intenzity))

def T2():
    
    GNP_TEMPLATE = """
ff{i}(x) = AA_0{i}*exp(-2*x/T2_{i} - c{i}*x**3)
AA_0{i} = 0.1
T2_{i} = 1.0*{T0}
c{i} = 1e-7
fit ff{i}(x) 'output/t2_{i}.dat' via AA_0{i}, T2_{i}, c{i}

print 'AA_0{i} ', AA_0{i}, AA_0{i}_err
print 'T2_{i} ', T2_{i}, T2_{i}_err
print 'c{i} ', c{i}, c{i}_err
"""
    gnp_command = ''
    tab_tup = ()
    for i in range(6):
        filename = 'data/%d_t2.txt'%i
        print(filename)
        data = np.genfromtxt(filename, delimiter='\t', skip_header=1)
        casy, intenzity = data.T
        intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
        tab_tup += (casy, [print_un_nopm(val) for val in intenzity] )
        with open('output/t2_%d.dat'%i, 'w') as ofile:
            ofile.writelines(gnp(casy, intenzity))
        
        with open('output/t2_%d.tex'%i, 'w') as ofile:
            ofile.writelines(tex(casy, intenzity))
        if not i in [0, 1]:
            gnp_command += GNP_TEMPLATE.format(i=i, T0=4*2**i)
        else:
            gnp_command += """
ff{i}(x) = AA_0{i}*exp(-2*x/T2_{i} - c{i}*x**3)
AA_0{i} = 0.1
T2_{i} = 1.0*{T0}
c{i} = 0
c{i}_err = 0
fit ff{i}(x) 'output/t2_{i}.dat' via AA_0{i}, T2_{i}

print 'AA_0{i} ', AA_0{i}, AA_0{i}_err
print 'T2_{i} ', T2_{i}, T2_{i}_err
print 'c{i} ', c{i}, c{i}_err
""".format(i=i, T0=4*2**i)
    with open('output/T2_all_tab.tex', 'w') as ofile:
        ofile.writelines(tex(*tab_tup))
    gnp_command += """
plot """
    for i in range(6):
        gnp_command += """ 'output/t2_{i}.dat' with yerrorbars ls {ip} lw 3 ps 2.3 pt 8 title '$c_{i}$', ff{i}(x) ls {ip} notitle, """.format(i=i, ip=i+1)
    
    with open('output/T2_graph_all.gnp', 'w') as ofile:
        ofile.write(gnp_command)
    
    print (gnp_command)
    reload()
    iss = [str(i) for i in range(6)]
    As = [gnuplot_dict['AA_0%d'%i] for i in range(6)]
    T2s = np.array([gnuplot_dict['T2_%d'%i] for i in range(6)])
    cs = np.array([gnuplot_dict['c%d'%i] for i in range(6)])
    
    with open('output/T2c.dat', 'w') as ofile:
        ofile.writelines(gnp(1/2**np.arange(6), T2s, 1000*T2s**(-1), As))
    
    with open('output/T2c.tex', 'w') as ofile:
        ofile.writelines(tex(iss, T2s, 1000*T2s**(-1), As, cs*1e6))


def T22():
    
    GNP_TEMPLATE = """
ff2{i}(x) = AA2_0{i}*exp(-2*x/T22_{i} - c2{i}*x**2)
AA2_0{i} = 0.1
T22_{i} = 1.0*{T0}
c2{i} = 1e-7
fit ff2{i}(x) 'output/t2_{i}.dat' via AA2_0{i}, T22_{i}, c2{i}

print 'AA2_0{i} ', AA2_0{i}, AA2_0{i}_err
print 'T22_{i} ', T22_{i}, T22_{i}_err
print 'c2{i} ', c2{i}, c2{i}_err
"""
    gnp_command = ''
    tab_tup = ()
    for i in range(6):
        filename = 'data/%d_t2.txt'%i
        print(filename)
        data = np.genfromtxt(filename, delimiter='\t', skip_header=1)
        casy, intenzity = data.T
        intenzity = [un.ufloat((c, 0.0001)) for c in intenzity]
        tab_tup += (casy, [print_un_nopm(val) for val in intenzity] )
        with open('output/t2_%d.dat'%i, 'w') as ofile:
            ofile.writelines(gnp(casy, intenzity))
        
        with open('output/t2_%d.tex'%i, 'w') as ofile:
            ofile.writelines(tex(casy, intenzity))
        if not i in [0, 1]:
            gnp_command += GNP_TEMPLATE.format(i=i, T0=4*2**i)
        else:
            gnp_command += """
ff2{i}(x) = AA2_0{i}*exp(-2*x/T22_{i} - c2{i}*x**2)
AA2_0{i} = 0.1
T22_{i} = 1.0*{T0}
c2{i} = 0
c2{i}_err = 0
fit ff2{i}(x) 'output/t2_{i}.dat' via AA2_0{i}, T22_{i}

print 'AA2_0{i} ', AA2_0{i}, AA2_0{i}_err
print 'T22_{i} ', T22_{i}, T22_{i}_err
print 'c2{i} ', c2{i}, c2{i}_err
""".format(i=i, T0=4*2**i)
    with open('output/T22_all_tab.tex', 'w') as ofile:
        ofile.writelines(tex(*tab_tup))
    gnp_command += """
plot """
    for i in range(6):
        gnp_command += """ 'output/t2_{i}.dat' with yerrorbars ls {ip} lw 3 ps 2.3 pt 8 title '$c_{i}$', ff2{i}(x) ls {ip} notitle, """.format(i=i, ip=i+1)
    
    with open('output/T2_graph_all2.gnp', 'w') as ofile:
        ofile.write(gnp_command)
    
    print (gnp_command)
    reload()
    iss = [str(i) for i in range(6)]
    As = [gnuplot_dict['AA2_0%d'%i] for i in range(6)]
    T2s = np.array([gnuplot_dict['T22_%d'%i] for i in range(6)])
    cs = np.array([gnuplot_dict['c2%d'%i] for i in range(6)])
    
    with open('output/T22c.dat', 'w') as ofile:
        ofile.writelines(gnp(1/2**np.arange(6), T2s, 1000*T2s**(-1), As))
    
    with open('output/T22c.tex', 'w') as ofile:
        ofile.writelines(tex(iss, T2s, As, cs*1e3))

if __name__ == '__main__':
    T1()
    T2()
    T22()
