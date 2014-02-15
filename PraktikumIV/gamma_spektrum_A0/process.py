from process_lib import *

import numpy as np
import os

def process_file(lines, name):
    data_pos = lines.index('$DATA:\n')
    data_range = map(int, lines[data_pos+1].strip().split())
    start, end = data_range
    counts = ((list(map (int, lines[data_pos + 2 + start:data_pos + 2 + end]))))
    x_axis = range(start, end)
    
    fit_pos = lines.index('$MCA_CAL:\n')
    a, b, c = list(map(float, lines[fit_pos+2].split()[:3]))
    print (a, b, c)
    def to_kev(x):
        return a+b*x+c*x**2
    kev_axis = list(map(to_kev, x_axis))
    with open('output/%s_gnp.dat'%name, 'w') as ofile:
        ofile.writelines(gnp(kev_axis, counts))
if not os.path.exists('output'):
    os.mkdir('output')

if __name__ == '__main__':
    names = ['kalibrace_CoCs.Spe', 'Cs.Spe', 'NaCl.Spe']
    for name in names:
        with open('pulmann/%s'%name, 'r') as ifile:
            lines = ifile.readlines()
            
        process_file(lines, name)
    #~ os.system('pdflatex uloha8.tex > /dev/null')
    
