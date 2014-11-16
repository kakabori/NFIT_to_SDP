import numpy as np
import math
import sys

wavelength = 1.18 # X-ray wavelength in Angstrom

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
    global t
    global mu
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


def normalize_to_each_other(F):
    for j in range(1, len(F[0])):
        num, denom = 0, 0        
        for i in range(len(F)):
            num += F[i][0]*F[i][j]
            denom += F[i][j]*F[i][j]
        a = num / denom
        for i in range(len(F)):
            F[i][j] = a * F[i][j]
    
    
def create_binned_data(qz_lists, F_lists):
    global bin_size
    qz_bin, F_bin = [], []
    largest_qz_value = final_qz_value(qz_lists)
    number_of_bins = int(round(largest_qz_value/bin_size)) + 1    
    for i in range(number_of_bins):
        tmp_qz_list, tmp_F_list = [], []
        current_bin = 0.001 * i
        for qzvalues, Fvalues in zip(qz_lists, F_lists):
            if within_current_bin(current_bin, qzvalues[0]):
                tmp_qz_list.append(qzvalues.pop(0))
                tmp_F_list.append(Fvalues.pop(0))                
        # Do not add if the temporary lists are not fully filled
        # for the current bin                    
        if len(tmp_qz_list) == len(qz_lists):        
            qz_bin.append(tmp_qz_list)
            F_bin.append(tmp_F_list)
    return qz_bin, F_bin   
               

def average_form_factors(qz_lists, F_lists):
    """Average multiple sets of form factors. Need at least two 
    input data sets.
    
    qz_lists : list of lists
    F_lists : list of lists
    
    Each list must be in an ascending order, which is the default format
    in NFIT frm.dat.
    """ 
    if len(qz_lists) < 2:
        raise TypeError('Need more than one form factor set for averaging')
    if len(qz_lists) != len(F_lists):
        raise TypeError('Number of qz and F data sets must agree')
    for qzvalues, Fvalues in zip(qz_lists, F_lists):
        if len(qzvalues) != len(Fvalues):
            raise TypeError('Length of each qz and F data set must agree') 
   
    qz_bin, F_bin = create_binned_data(qz_lists, F_lists)
    normalize_to_each_other(F_bin)
    qz_bin = np.array(qz_bin)
    F_bin = np.array(F_bin)
    avg_qz = np.mean(qz_bin, axis=1)
    err_qz = np.std(qz_bin, axis=1, ddof=1, dtype=np.float64)
    avg_F = np.mean(F_bin, axis=1)    
    err_F = np.std(F_bin, axis=1, ddof=1, dtype=np.float64)   
         
    return avg_qz, err_qz, avg_F, err_F
   

def within_current_bin(cbin, value):
    global bin_size
    if (value >= cbin - 0.5*bin_size) and (value < cbin + 0.5*bin_size):
        return True
    else:
        return False


def final_qz_value(qzlists):
    tmp = 10000 # some big value
    for qzvalues in qzlists:
        if qzvalues[-1] < tmp:
            tmp = qzvalues[-1]    
    return tmp
    

def get_filenames_from_CL():
    filenames = []
    if len(sys.argv) < 3:
        print("Need at least two filenames")
    else:
        print("\nInput filenames are:")
        for i in xrange(1, len(sys.argv)):
            filenames.append(sys.argv[i])  
            print(sys.argv[i])
        print("")
    return filenames


def get_all_qz_and_scale(filenames):
    all_qz = []
    all_scale = []
    for f in filenames:
        px, scale, cz, qz, sig_scale, sig_cz = read_frm_dot_dat(f)
        all_qz.append(qz)
        all_scale.append(scale)  
    return all_qz, all_scale  


def scaling_to_form_factors(all_qz, all_scale):
    for qz, scale in zip(all_qz, all_scale):
        convert_scaling_to_form_factors(qz, scale)
        
               
if __name__ == '__main__':
    filenames = get_filenames_from_CL() 
    # grab absorption length, sample thickness, and bin size
    execfile('parameters.py')
    tmp = raw_input('Enter the X-ray wavelength (default: 1.18) : ')
    if tmp != '':
        wavelength = float(tmp)    
    all_qz, all_scale = get_all_qz_and_scale(filenames)
    scaling_to_form_factors(all_qz, all_scale)
    qz, sigma_qz, F, sigma_F = average_form_factors(all_qz, all_scale)
    write_to_file(qz, F, sigma_F, "averaged_form_factors.smp")
