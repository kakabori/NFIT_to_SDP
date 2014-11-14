The NFIT_to_SDP program averages multiple scaling factors. Inputs must
be frm.dat files from NFIT. See the test folder for example frm.dat files.
To run a test, type

python main.py test/test1.dat test/test2.dat test/test3.dat

The program will ask for the X-ray wavelength. To accept the default value,
just hit Enter. For actual data sets, you need to enter the wavelength
for those data sets. Type in the value and hit enter.

Examine the output file called averaged_form_factor.smp. It is formatted
as a usual smp file. If parameters don't make sense, read the SDP manual.

To use this program, you need relative or absolute paths to frm.dat files
you want to average. For example, if you have files named file1.dat, file2.dat,
file3.dat, and file4.dat in /home/biophysicists/data/, then type

python main.py /home/biophysicists/data/file1.dat /home/biophysicists/data/file2.dat /home/biophysicists/data/file3.dat /home/biophysicists/data/file4.dat 

If you put all your frm.dat files in the NFIT_to_SDP folder, type

python main.py file1.dat file2.dat file3.dat file4.dat

The output file named average_form_factors.smp will contain the averaged
form factors along with standard deviations and averaged qz values.

Note that the bin size for qz is 0.001. This choice assumes that your CCD
data were collected with a usual setup (S-distance ~ 360 mm, wavelength ~ 1.18 A,
pixel size ~ 0.07113 mm), which leads to 0.001 inverse Angstrom per pixel.
If the setup is considerably different, you might need to adjust the bin size.
