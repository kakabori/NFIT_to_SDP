import numpy as np
import math
import sys

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


def convert_scaling_to_form_factors(qz, scale):
    """Convert scaling factors to form factors. 
    
    qz : list
    scale : list
    """
    for i in xrange(len(scale)):
        scale[i] = sqrt(scale[i])
    
    
def apply_Lorentz_correction(qz, scale):
    """Apply Lorentz correction to input scaling factors.
    
    qz : list
    scale : list
    """
    for i in xrange(len(scale)):
        scale[i] = scale[i] * qz[i]


def apply_absorption_correction(qz, scale):
    """Apply absorption correction to input scaling factors.
    
    qz : list
    scale : list
    """
    pass
    

def remove_errorneous_data_points(qz, scale):
    """Remove certain errorneous data points. An errorneous
    data point is defined by a scaling factor that looks like
    ***e13.
    
    qz : list
    scale : list
    """
    pass
    
    
def output_to_smp_file(qz_values, form_factors, errors, filename):
    pass
    
    
def smooth_form_factor(f):
    pass
    

def average_form_factors(qz_lists, F_lists)
    """Average multiple sets of form factors. Need at least two 
    input data sets.
    
    qz_lists : list of lists
    F_lists : list of lists
    """ 
    if len(qz_lists) < 2:
        raise TypeError('Need more than one form factor set for averaging')
    if len(qz_lists) != len(F_lists):
        raise TypeError('Number of qz and F data sets must agree')
    for qzvalues, Fvalues in zip(qz_lists, F_lists):
        if len(qzvalues) != len(Fvalues):
            raise TypeError('Length of each qz and F data set must agree') 
    bin_size = 0.0005
    avg_qz, avg_F = [], []
    err_qz, err_F = [], []
    tmp_qz_list = []
    tmp_F_list = []
    while not qz_lists[0]:
        base_qz = qz_lists[0][0]
        for qzvalues, Fvalues in zip(qz_lists, F_lists):
            while True:
                qz = qzvalues.pop(0)
                F = Fvalues.pop(0)
                if (qz <= base_qz + 0.5*bin_size) and (qz >= base_qz - 0.5*bin_size): 
                    tmp_qz_list.append(qz)
                    tmp_F_list.append(F)
                    break
        avg_qz.append(np.mean(tmp_qz_list))
        err_qz.append(np.std(tmp_qz_list, ddof=1, dtype=np.float64))
        avg_F.append(np.mean(tmp_F_list)))
        err_F.append(np.std(tmp_F_list, ddof=1, dtype=np.float64))
    return avg_qz, err_qz, avg_F, err_F
   
   
if __name__ == '__main__':
    filenames = []
    all_qz = []
    all_scale = []
    for arg in sys.argv:
        filenames.append(arg)   
    for f in filenames:
        px, scale, cz, qz, sig_scale, sig_cz = read_frm_dot_dat(f)
        all_qz.append(qz)
        all_scale.append(scale)
    for i in xrange(len(all_qz)):
        remove_errorneous_data_points(all_qz[i], all_scale[i])
        apply_absorption_correction(all_qz[i], all_scale[i])
        apply_Lorentz_correction(all_qz[i], all_scale[i])
        convert_scaling_to_form_factors(all_qz[i], all_scale[i])
    average_form_factors(all_qz, all_scale)
