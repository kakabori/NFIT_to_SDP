import numpy as np
import math

def read_frm_dot_dat(filename):
    pixel = []; scaling = []; cz = []; qz = []; sigma_scaling = []; sigma_cz = [];
    fileobj = open(filename, 'r')
    lines = fileobj.readlines()
    for line in lines:
        # This ignores an empty line
        line = line.rstrip()
        if not line: 
            continue
        p, s, c, q, ss, sc = line.split()
        p = int(p)
        s = float(s)
        c = float(c)
        q = float(q)
        ss = float(ss)
        sc = float(sc)
        pixel.append(p) 
        scaling.append(s) 
        cz.append(c)
        qz.append(q)
        sigma_scaling.append(ss)
        sigma_cz.append(sc)
    return pixel, scaling, cz, qz, sigma_scaling, sigma_cz

    
def apply_Lorentz_correction(f):
    for index, item in enumerate(f):
        f[index][1] = f[index][1] * f[index][0]
    return f


def apply_absorption_correction():
    pass
    

def output_to_smp_file():
    pass
    
    
def remove_errorneous_data_points():
    pass
    
    
def smooth_form_factor():
    pass
    

def average_form_factor() 
    pass

   

 

