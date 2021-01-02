# PIS-G
Parallel inversion software of gravity gradiometry data (PIS-G) is used for obtaining underground density distribution accurately, suitable for the large-scale data inversion research and education. PIS-G is developed by Python, combined with OpenMP and CUDA. At present, it offers the functions of data & file management, visualization, forwarding and inversion; in the future work, more powerful functions would be introduced into this platform by secondary development. It is demonstrated to be practical and easy-to-use in the tests. We hope it could be helpful for your study and work!

The software platform is developed on Windows system with tool of Eric 6.0. Python 3.6.0 is used for writing most of the codes, the toolboxes of PyQt 5.10.1, Matplotlib 3.0.3, Numpy 1.17.4, xlrd 1.2, xlwt 1.3 and xlutils 2.0 are applied. CUDA 10.2 is chosen for parallel computing, CUDA Runtime (cudart64_102) file is offered and located in the folder of “supplementary_files”, the latest version of CUDA could be downloaded from https://developer.nvidia.com/cuda-downloads.

In addition, if you want to reproduce the inversion results of synthetic data in the paper, use the software as described in the file “user manual.md” or “user manual.pdf” in the folder of “supplementary_files”. Refer to the sections of “1.1 Project operation”, “1.2 Import data” and “4 Inversion” to reproduce the results. Refer to section of “2.4 3D view of Model (2)-(5)” for the 3D view of results, then right-click the plot of 3D view to obtain X-Y profile, X-Z profile and Y-Z profile. The input data is named “grav_rfi_data.txt” in the folder of “Test data”. The inversion parameters could be input as described in the section “4.1 Synthetic data test” of paper. The real data in the paper could not be offered because the data is supplied by the other organization, mentioned in the section of “Acknowledgement” in the paper.

Name of program: Parallel Inversion Software of Gravity gradiometry data (PIS-G)
Title of the manuscript: Three dimensional inversion and software development of vertical gravity gradient based on multiple GPUs
Developer: Zhenlong Hou, Jikang Wei, Tianxiao Mao, Yujun Zheng, Yuchen Ding
Contact address: NO. 3-11, Wenhua Road, Heping District, Shenyang, P. R. China
Telephone number: +8618309831845
E-mail: houzhenlong@mail.neu.edu.cn; houzlatjlu@163.com
