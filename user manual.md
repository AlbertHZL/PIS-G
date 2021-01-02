
# User Manual

## Parallel Inversion Software of Gravity gradiometry data (PIS-G)

**Developed by Zhenlong Hou, Jikang Wei, Tianxiao Mao, Yujun Zheng, Yuchen Ding**

**September 24, 2020**

**Thanks very much for your attention and using PIS-G!**

# Introduction
Parallel inversion software of gravity gradiometry data (PIS-G) is used for obtaining 
underground density distribution accurately, suitable for the large-scale data inversion 
research and education. PIS-G is developed by Python, combined with OpenMP and 
CUDA. At present, it offers the functions of data & file management, visualization, 
forwarding and inversion; in the future work, more powerful functions would be 
introduced into this platform by secondary development. It is demonstrated to be 
practical and easy-to-use in the tests. We hope it could be helpful for your study and 
work!

Configuration requirement: CPU: dual core processor 2.5GHz; Memory: 4GB RAM; 
GPU: NVDIA GeForce GTX 1050 Ti; System: Windows XP or 7 or 10.

Program size: 178 MB

It is noted that the user’s computer must be equipped with GPU supporting CUDA, or 
the inversion module would not work.

## 1 Data and file management
### 1.1 Project operation

(1) Start PIS-G.

(2) Create a new project: Click “New project” of “File” in the menu.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-1.jpg)

(3) Load an existed project: Click “Load project” of “File” in the menu.

(4) Save a project: Click “Save project” of “File” in the menu.

(5) Close a project: Click “Close project” of “File” in the menu, it is noted that the user must 
save the project before closing it or the data may be lost.

### 1.2 Import data
(1) Click “Open File Data” of “File” in the menu.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-2.jpg)

(2) Choose the file to import.

(3) Preview the data, import the row number in “Data Start Line”, default is 1.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-3.jpg)
 
(4) After the preview, the names of data in columns could be revised. Rename it directly in the table. Click “Finish” to finish the wizards.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-4.jpg)

### 1.3 Data display and operation
(1) Data is displayed in the table, sorted by line.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-5.jpg)

(2) Right click on the data, click “Copy” or “Cut” or “Delete” or “Paste”.

(3) Data would be changed as user’s operation.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-6.jpg)

### 1.4 Set X & Y Coordinate
(1) Click “Set X & Y” of “Coordinate” in the menu.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-7.jpg)

(2) Determine which column of data is x or y coordinate by drop-down list.

(3) Click “OK” to finish. It is noted that coordinate must be set before using forwarding or inversion module.
1.5 Save or delete the files
(1) Right click the file names in the file list, user could choose save or delete the current file.

(2) Click “Save Result” of “Forwarding” in the menu, the synthetic data and forwarding parameters are saved into 2 text files.

(3) Click “Save Result” of “Parallel 3D Inversion” in “Inversion”, save the inversion results and parameters into 2 text files.

## 2 Data visualization
### 2.1 Profile
(1) Click “Profile” of “Paint” in the menu.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-8.jpg)

(2) Variable: choose which data to be displayed by checkbox.

(3) X axis unit: choose the unit (m or km) for x coordinate by drop-down list.

(4) V axis unit: choose the unit (g.u. or mGal or E) for displayed data by drop-down list.

(5) Show Symbol: choose whether to show the symbol for the data or not by drop-down list.

(6) The profile figure would change as the line is switched by drop-down list at top-left corner of table.

### 2.2 Grid
(1) Click “Grid” of “Paint” in the menu.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-9.jpg)

(2) Variable: choose which data to be displayed by checkbox.

(3) Type the title for color bar in “Color Bar Title”.

(4) Show Isoline or Value: choose whether to show the isolines, the values for the data or not by drop-down list.

(5) X or Y axis unit: choose the unit (m or km) for x or y coordinate by drop-down list.

### 2.3 3D view of Grid
(1) Click “3D” of “Paint” in the menu.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-10.jpg)

(2) Variable: choose which data to be displayed by checkbox.

(3) Type the title for color bar in “Color Bar Title”.

(4) X or Y axis unit: choose the unit (m or km) for x or y coordinate by drop-down list.

(5) Z axis unit: choose the unit (g.u. or mGal or E) for displayed data by drop-down list.

### 2.4 3D view of Model
(1) Click “Painting” of “Forwarding” in the menu, the synthetic model would be plotted in 3D view.

(2) Click “Painting” of “Parallel 3D Inversion” in “Inversion”, the dialog below appears, import the parameters to obtain the figure.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-11.jpg)

(3) lower or upper limit: the minimum or maximum value of the results to display.

(4) Type the title for figure or color bar in “Figure Title” or “ColorBar Title”.

(5) X or Y axis unit: choose the unit (m or km) for x or y coordinate by drop-down list.

## 3 Forwarding
(1) Click “Forwarding” of “Forwarding” in the menu, forwarding wizard appears.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-12.jpg)

(2) Number of Model: set the number of the prisms in the combination model.

(3) Type the title for figure or color bar in “Figure Title” or “ColorBar Title”.

(4) Observation Height: set the height of the observed plane, all of the observations are in this plane, unit is m.

(5) X or Y Range: the coordinate range of the observations in x or y axis direction.

(6) dx or dy: the interval in x or y axis direction.

(7) Import the parameters for each prism model in order, the parameters are shown in the wizard below. The model shape could be selected by drop-down list, only cube is offered at present.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-13.jpg)

(8) Preview the forwarding parameters for the model.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-14.jpg)

## 4 Inversion
(1) Click “Calculation” of “Parallel 3D Inversion” in “Inversion”.

![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-15.jpg)

(2) the number of divided layers: the number of prisms in z axis direction.

(3) maximum number of iterations: kmax in the manuscript.

(4) z_obs: the height of observed plane.

(5) dz: the interval in z axis direction.

(6) zmax: the maximum depth to inverse, equal to the number of divided layers multiplied by dz.

(7) m_min and m_max: the minimum and maximum of density constraints.

(8) epsilon: ε in the manuscript.

(9) miu: μ in the manuscript.

(10) sigma: σ in the manuscript.

(11) wn: wn in the manuscript.

(12) Max_GPU_Number: the number of GPUs used in the inversion.

(13) nThreadPerBlock: the number of threads per block in GPU.

(14) Click “OK” to start calculations.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-16.jpg)

(15) If the inversion ends, a dialog is presented.
 
 ![image](https://github.com/AlbertHZL/PIS-G/blob/master/supplementary_files/figures_in_user_manual/fig-17.jpg)
