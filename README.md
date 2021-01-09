# PIS-G
Parallel inversion software of gravity gradiometry data (PIS-G) is used for obtaining underground density distribution accurately, suitable for the large-scale data inversion research and education. PIS-G is developed by Python, combined with OpenMP and CUDA. At present, it offers the functions of data & file management, visualization, forwarding and inversion; in the future work, more powerful functions would be introduced into this platform by secondary development. It is demonstrated to be practical and easy-to-use in the tests. We hope it could be helpful for your study and work!

The software platform is developed on Windows 10 with tool of Eric 6.0. Python 3.6.0 is used for writing most of the codes, the toolboxes of PyQt 5.10.1, Matplotlib 3.0.3, Numpy 1.17.4, xlrd 1.2 and xlwt 1.3 are applied. The requirements file about code dependencies named “requirements.txt” is also offered. CUDA 10.2 is chosen for parallel computing. The latest version of CUDA could be downloaded from https://developer.nvidia.com/cuda-downloads.

Before compiling the source codes, two dlls are needed, produced by “Forwarding_DLL.h” and “Forwarding_DLL.cpp”, “grav_rfi_ompcuda.h” and “grav_rfi_ompcuda.cu”, respectively. Visual Studio could be used to produce them on Windows system. Also, a CMakeLists.txt could also be used to build them. An example on Windows system of using CMakeLists.txt to produce dlls is introduced below：

(1) Go to https://cmake.org/download/ to download a distribution of CMake, here we download “cmake-3.19.2-win64-x64.msi”.

(2) Once CMake is installed, two directories should be prepared to build a project, one for the source code, the other for the binaries. Here are our directories: “C:\Users\Hou-ZL\Desktop\make_dlls”, where the source codes are located, including “Forwarding_DLL.h”, “Forwarding_DLL.cpp”, “grav_rfi_ompcuda.h”, “grav_rfi_ompcuda.cu” and “CMakeLists.txt”; “C:\Users\Hou-ZL\Desktop\make_dlls\build”, where the binary files are located.

(3) Run cmake-gui.exe, specify the directories, see fig-1.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_README/fig-1.jpg)

fig-1 CMake UI

(4) Click Configure button to show a configuration dialog, specify the generator, here we choose “Visual Studio 16 2019”, see fig-2. New values would be shown and colored red, some information is displayed at the bottom of UI, see fig-3.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_README/fig-2.jpg)

fig-2 Configuration dialog

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_README/fig-3.jpg)

fig-3 Configuration information and new values

(5) Click Generate button to produce the files.

In addition, if you want to reproduce the inversion results of synthetic data in the paper, use the software as described in the file “user manual.md” or “user manual.pdf” in the folder of “supplementary_files”. Refer to the sections of “1.1 Project operation”, “1.2 Import data” and “4 Inversion” to reproduce the results. Refer to section of “2.4 3D view of Model (2)-(5)” for the 3D view of results, then right-click the plot of 3D view to obtain X-Y profile, X-Z profile and Y-Z profile. The input data is named “grav_rfi_data.txt” in the folder of “Test data”. The inversion parameters could be input as described in the section “4.1 Synthetic data test” of paper. The real data in the paper could not be offered because the data is supplied by the other organization, mentioned in the section of “Acknowledgement” in the paper.

Name of program: Parallel Inversion Software of Gravity gradiometry data (PIS-G)
Title of the manuscript: Three dimensional inversion and software development of vertical gravity gradient based on multiple GPUs
Developer: Zhenlong Hou, Jikang Wei, Tianxiao Mao, Yujun Zheng, Yuchen Ding
Contact address: NO. 3-11, Wenhua Road, Heping District, Shenyang, P. R. China
Telephone number: +8618309831845
E-mail: houzhenlong@mail.neu.edu.cn; houzlatjlu@163.com
