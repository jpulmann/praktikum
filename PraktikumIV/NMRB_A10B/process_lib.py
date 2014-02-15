import math

import numpy as np

import uncertainties as un
import uncertainties.umath as um
import os

def guess_len(f):
    eps = 1e-10
    
    if  abs(round(f) - f) < eps :
        return 0
    
    guess = 1
    
    while abs(round(f, guess) - f) > eps:
        guess += 1
    
    return guess


def print_un(unn, digits=-1):
    x = unn.nominal_value
    dx = unn.std_dev()
    
    if digits == -1:
        if dx == 0:
            return print_un(unn, digits=guess_len(x))

        num_digits = -math.floor(math.log(dx, 10))

    else:
        num_digits = digits
    
    dx_normalized = dx * 10**num_digits
    
    delta = dx_normalized - math.floor(dx_normalized)
    
    if 10*delta > 3:
        if dx_normalized > 9:
            rounded_dx = math.ceil(dx_normalized) / 10**num_digits
            num_digits -= 1
        else:
            rounded_dx = math.ceil(dx_normalized) / 10**num_digits
    else:
        rounded_dx = math.floor(dx_normalized) / 10**num_digits
    if num_digits >= 0:
        return ("${:."+str(num_digits)+"f} \pm {:."+str(num_digits)+"f}$").format( x, rounded_dx )
    else:
        rounded_x = int(x) - int(x) % 10**(-num_digits)
        return "${} \pm {}$".format(rounded_x, int(rounded_dx))
        
def print_un_nopm(unn, digits=-1):
    un_printed = print_un(unn, digits)
    return (un_printed[:un_printed.find('\\pm')].strip() + '$')

def print_nice(f):
    if hasattr(f, "std_dev"):
        return print_un(f)
    if isinstance(f, str):
        return f
    if isinstance(f, float):
        if math.isnan(f):
            return ''
        else:
            return ('{:.'+str(guess_len(f))+'f}').format(f)
    elif isinstance(f, int):
        return str(int)
    elif float(int(f)) == f:
        return str(int(f))
    else:
        return ('{:.'+str(guess_len(f))+'f}').format(f)

def gnp(*args):
    assert len(args) > 0
    nlines = max(map(len, args))

    lines = []
    
    for i in range(nlines):
        line = []
        for arg in args:
            if hasattr(arg[i], 'std_dev'):
                line.append( arg[i].nominal_value )
                line.append( arg[i].std_dev() )
            elif np.isnan(arg[i]) or math.isnan(arg[i]):
                pass
            else:
                line.append(arg[i])
        linestr = "\t".join(  map( str, line) ) + '\n'
        lines.append(linestr)
    return lines

def tex(*args):
    assert len(args) > 0

    nlines = max(map(len, args))

    lines = []
    
    for i in range(nlines):
        line = [arg[i] if i<len(arg) else '' for arg in args ]
        print (line)
        linestr = " & ".join(  map( print_nice, line) ) + '\\\\\n'
        lines.append(linestr)
        
    return lines



def break_table(n, *args):
    assert len(args) > 0
    nlines = max(map(len, args))
    ntable = tuple([[] for i in range(n*len(args))])
    def get(p, i):
        if len(p)>i:
            return p[i]
        return float('nan')
    broke_n = math.ceil(nlines/n)
    
    for i in range(broke_n):
        for j in range(n):
            for k,a in enumerate(args):
                ntable[j*len(args)+k].append( get(a, i+broke_n*j))
                
    return ntable

def derivative(data):
    r = []
    for i in range(len(data)-1):
        r.append(data[i+1]-data[i])
    return r

def mean_std(data):
    return ( np.mean(data), np.std(data)/math.sqrt(len(data)-1) )

def get_analog(data, R, trieda, pocet_dielikov=float('inf')):
    return [ un.ufloat( (d, r*trieda/100 + r/(math.sqrt(3)*pocet_dielikov*2)) ) for d, r in zip(data, R) ]

def zip_map(D1, D2, fun):
    return [fun(d1, d2) for d1, d2 in zip(D1, D2) ]
    
def zip_un(D1, D2):
    return zip_map(D1, D2, lambda x, y: un.ufloat((x, y)))

def gnuprint(fname, *args):
    with open(os.path.join('data',fname), 'w') as ofile:
        ofile.writelines( gnp( *tuple(args) ))

def texprint(fname, n, *args):
    with open(os.path.join('data',fname), 'w') as ofile:
        if n == 1:
            ofile.writelines( tex( *tuple(args) ))
        else:
            ofile.writelines( tex( * break_table(n, *tuple(args)) ) )
            
def plain_print(lst, digits = -1):
    return list(map( lambda x: print_un_nopm(x, digits) , lst))

gnuplot_script = 'graph.gnp'
gnuplot_data = 'output/gnuplot_output.dat'
gnuplot_dict = dict()
def load_gnuplot_dict(gnuplot_data, gnuplot_dict):
    gnuplot_dict.clear()
    gnuplot_dict['noname'] = []
    
    def get_value(word):
        try:
            val = int(word)
            return val
        except ValueError:
            pass
        try:
            return float(word)
        except ValueError:
            return word
    
    with open(gnuplot_data, 'r') as ofile:
        for line in ofile.readlines():
            words = line.split()
            if len(words) == 0:
                pass
            elif len(words) == 1:
                gnuplot_dict['noname'].append(words)
            elif len(words) == 2:
                name = words[0]
                gnuplot_dict[name] = get_value(words[1])
            elif len(words) == 3:

                name = words[0]
                v1 = get_value(words[1])
                v2 = get_value(words[2])
                #~ print(v1, v2)
                try:
                    gnuplot_dict[name] = un.ufloat( (get_value(words[1]), get_value(words[2])) )
                except:
                    gnuplot_dict[name] = [v1, v2]
            else:
                name = words[0]
                gnuplot_dict[name] =  list(map(get_value, words[1:]))
def rerun_gnuplot(gnuplot_script):
    os.system('gnuplot '+gnuplot_script)
def reload():
    global gnuplot_dict
    global gnuplot_data
    global gnuplot_script
    rerun_gnuplot(gnuplot_script)
    load_gnuplot_dict(gnuplot_data, gnuplot_dict)

