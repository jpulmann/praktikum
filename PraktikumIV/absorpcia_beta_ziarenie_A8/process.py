from process_lib import *

import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')

def one_measurement_statistics():
    counts_no_shielding = np.genfromtxt('data/counts_no_shielding.dat', delimiter='\t')
    
    #~ print (counts_no_shielding)
    first_measurement_mean = un.ufloat((
                            np.mean(counts_no_shielding),
                            np.std(counts_no_shielding, ddof=1)/math.sqrt(counts_no_shielding.shape[0]),
                            ))
                    
    with open('output/no_shielding_mean.tex', 'w') as ofile:
        ofile.write(
                print_un(
                        first_measurement_mean
                        ).replace('$', '')
                )
                
    relative = np.std(counts_no_shielding, ddof=1)/np.mean(counts_no_shielding)
    #~ print (relative)
    
    with open('output/relative.tex', 'w') as ofile:
        ofile.write(
            '%.1f'%(relative*100)
        )
    
    with open('output/no_shielding_tab.tex', 'w') as ofile:
        ofile.writelines(' & '.join([('%.2f'%c) for c in counts_no_shielding]))
            
    return relative, first_measurement_mean
    
def process_counts(relative, first_measurement_mean):
    counts = np.genfromtxt('data/counts.dat', delimiter='\t')
    counts.sort(axis=0)
    width, time = counts.T
    width = [un.ufloat((w, w/100)) for w in width]
    time = [un.ufloat((t, t*relative)) for t in time]
    time[0]=first_measurement_mean
    
    N = [1000.0/t for t in time]
        
    with open('output/counts_tab.tex', 'w') as ofile:
        ofile.writelines(tex(width, time, N))
    with open('output/counts_gnp.dat', 'w') as ofile:
        ofile.writelines(gnp(width, time, N))
    
    
    
    reload()
    print (gnuplot_dict)
    
    for par in ['a1', 'a2', 'N1', 'N2', 'NB']:
        with open('output/%s_fit.tex'%par, 'w') as ofile:
            ofile.write(print_un(gnuplot_dict[par]).replace('$', ''))
    
    for i in [1, 2]:
        a = 'a' + str(i)
        u = gnuplot_dict[a]
        E = (u/22)**(-3/4)
        with open('output/muE%d.tex'%i, 'w') as ofile:
            ofile.write(print_un(E).replace('$', ''))
    
    reload()
    #~ print (gnuplot_dict['D01'])
    Rb1 = gnuplot_dict['D01']/1000
    Rb2 = gnuplot_dict['D02']/1000
    for i, Rb in enumerate([Rb1, Rb2]):
        if Rb < 0.3:
            E = (Rb/0.407)**(1/1.38)
        else:
            E = (Rb+0.133)/0.542
        with open('output/RE%d.tex'%(i+1), 'w') as ofile:
            ofile.write(print_un(E).replace('$', ''))
        
if __name__ == '__main__':
    relative, first_measurement_mean = one_measurement_statistics()
    process_counts(relative, first_measurement_mean)
    #~ os.system('pdflatex uloha8.tex > /dev/null')
    
