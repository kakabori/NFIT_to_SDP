import numpy as np
import math
import sys

wavelength = 1.18

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
    apply_absorption_correction(qz, scale)
    apply_Lorentz_correction(qz, scale)
    for i in xrange(len(scale)):
        scale[i] = np.sign(scale[i]) * math.sqrt(abs(scale[i]))
    
    
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
    t = 10
    mu = 2600
    global wavelength
    for i in xrange(len(scale)):
        #a = wavelength * qz[i] / 4 / math.pi
        a = 1.18 * qz[i] / 4 / math.pi
        theta = math.asin(a)
        g = 2 / math.sin(theta)
        Ac = t * g / mu / (1-math.exp(-t*g/mu))
        scale[i] = Ac * scale[i]
    

def remove_errorneous_data_points(qz, scale):
    """Remove certain errorneous data points. An errorneous
    data point is defined by a scaling factor that looks like
    ***e13.
    
    qz : list
    scale : list
    """
    pass
    
    
def write_to_file(qz_values, form_factors, errors, filename):
    """Write to filename.smp file"""
    with open(filename, 'w') as f:
        f.write("""set direct_err 1
set stepsize_integral 0.05
set normal_mode 2

""")
        f.write("""# This sample was created by NFIT_to_SDP program.
# (1) Change all ? to an appropriate sample number. 
# (2) Change sample_name to whatever sample name you want.
# (3) Change other parameters to actual physical values.
# (4) Copy the following lines to your smp file.
samplist ? sample_name
parameter ? nobeam \\
1.18 2.3 5 2 10 1 -64 65 0.0 \\
x 0.333 67.0 91.0 0 7.875 0.0 9.0 0.0 \\
""")
        for qz, F, sig in zip(qz_values, form_factors, errors):
            f.write("{0: 8.3f} {1: .4f} {2: 8.3f} \\\n".format(F, qz, sig))
    
    
def smooth_form_factor(f):
    pass
    

def average_form_factors(qz_lists, F_lists):
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
    
    base_qz = qz_lists[0][0]
    while True:
        # If any of the lists is empty, no more averaing is required
        if len(qz_lists[0]) == 0:
            break
                    
        tmp_qz_list, tmp_F_list = [], []            
        for qzvalues, Fvalues in zip(qz_lists, F_lists):
            # If the current qz value is too small, discard it
            while (qzvalues[0] < base_qz - 0.5*bin_size):
                del(qzvalues[0])  
                del(Fvalues[0])
            # If the current qz value is too large, update base_qz
            # and start over with the updated base_qz     
            if (qzvalues[0] > base_qz + 0.5*bin_size):
                base_qz = qzvalues[0]
                break
            else:
                tmp_qz_list.append(qzvalues.pop(0))
                tmp_F_list.append(Fvalues.pop(0))
                
        # Do not average if the temporary lists are not fully filled
        # for this iteration                    
        if len(tmp_qz_list) == len(qz_lists):        
            avg_qz.append(np.mean(tmp_qz_list))
            err_qz.append(np.std(tmp_qz_list, ddof=1, dtype=np.float64))
            avg_F.append(np.mean(tmp_F_list))
            err_F.append(np.std(tmp_F_list, ddof=1, dtype=np.float64))
            if len(qz_lists[0]) > 0:
                base_qz = qz_lists[0][0]
        else:
            # If the temporary lists are not fully filled, base_qz
            # was already set to a larger value
            print('No avaraging was taken')
    
    return avg_qz, err_qz, avg_F, err_F
   
   
if __name__ == '__main__':
    filenames = []
    all_qz = []
    all_scale = []
    
    if len(sys.argv) < 4:
        print("Need at least two filenames")
    else:
        for i in xrange(2,len(sys.argv)):
            filenames.append(sys.argv[i])  
    
    tmp = raw_input('Enter the X-ray wavelength (default: 1.18) : ')
    if tmp != '':
        wavelength = float(tmp)
    
    for f in filenames:
        px, scale, cz, qz, sig_scale, sig_cz = read_frm_dot_dat(f)
        all_qz.append(qz)
        all_scale.append(scale)
    for qz, scale in zip(all_qz, all_scale):
        convert_scaling_to_form_factors(qz, scale)
    qz, sigma_qz, F, sigma_F = average_form_factors(all_qz, all_scale)
    write_to_file(qz, F, sigma_F, "averaged_form_factors.smp")
