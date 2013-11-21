from process_lib import *

import glob
import itertools

import numpy as np
import os

if not os.path.exists('output'):
    os.mkdir('output')

def pdf():
    pages = 9
    os.system('pdfseparate data/pulmann.pdf -f 1 -l {}  output/sprska%d.pdf'.format(pages))
    for i in range(1, pages+1):
        os.system('pdfcrop --margins 10 output/sprska{i}.pdf output/sprska{i}crop.pdf'.format(i=i))
    
    
    
if __name__ == '__main__':
    pdf()
