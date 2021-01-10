# include "grav_rfi_ompcuda.h"
# include <stdlib.h>
# include <stdio.h>
# include <string.h>
# include <math.h>
# include <omp.h>
# include <cuda.h>
# include <cuda_runtime.h>
# include <device_launch_parameters.h>

struct Vz_struct
{
	double* Vz, * x_obs, * y_obs;
	double* m1_x, * m1_y, * m1_z;
};
struct input_struct
{
	double* h_Vz, * h_x_obs, * h_y_obs, * h_m1_x, * h_m1_y, * h_m1_z;
	double* d_Vz, * d_x_obs, * d_y_obs, * d_m1_x, * d_m1_y, * d_m1_z;
	cudaStream_t stream;
};
struct Vz_mat_mc_struct
{
	double* d_Vz_mat_mc;
	int nBlocks;
	cudaStream_t stream;
};
struct rfi_struct
{
	int localNum, nBlocks, base, nBlocks_Am, nBlocks_Gm;
	double* d_local_Wm, * d_local_Wv, * d_local_W, * d_local_g, * d_local_g0, * d_local_p, * d_local_p0, * d_local_q1, * d_local_q2;
	double* d_local_m_temp, * d_local_m_real, * d_local_d_fit1, * d_local_d_fit2, * d_local_d_fit_temp1, * d_local_d_fit_temp2, * d_d_fit_temp;
	double* h_local_g, * h_local_g0, * h_local_q, * h_local_m_real, * h_local_d_fit, * h_local_d_fit_temp;
	cudaStream_t stream;
};

void xy_cmp(int point_count, int lx, int ly, double* x, double* y, double* xmin, double* xmax, double* dx, double* ymin, double* ymax, double* dy);

double* rwt_foc_inv(int deviceCount, int h_point_count, int h_prism_count, int h_lx, int h_ly, int h_lz, int h_kmax,
	double h_z_obs, double h_m_min, double h_m_max, double h_epsilon, double h_lambda, double h_sigma, struct Vz_struct VzX, int Max_GPU_Number, int nThreadPerBlock,double wn);
__global__ void Vz_mat_mc_sln(double* Vz_mat_mc, double* x_obs, double* y_obs, double* m1_x, double* m1_y, double* m1_z, double z_obs, int lx, int lz, int point_count, int prism_count);
__global__ void W_init_sln(double* Wm, double* Wv, double* W, double* m_temp, double* m_real, double* Vz_mat_mc, double sigma, int localNum, int base, int point_count, int lx, double wn);
__global__ void g0_sln(double* g, double* Vz_mat_mc, double* W, double* Vz, int localNum, int base, int point_count, int lx);
__global__ void A_mult_v_col_sln(double* q, double* Vz_mat_mc, double* W, double* vector, int localNum, int base, int point_count, int lx, int nThreadPerBlock);
__global__ void A_mult_v_sum_sln(double* q2, double* q1, double* vector, double lambda, int localNum, int base, int point_count, int prism_count, int nBlocks);
__global__ void m_sln(double* m_temp, double* m_real, double* p, double* W, double alpha, double m_min, double m_max, int localNum);
__global__ void G_mult_m_col_sln(double* d_fit, double* Vz_mat_mc, double* m_temp, int localNum, int base, int point_count, int lx, int nThreadPerBlock);
__global__ void G_mult_m_sum_sln(double* d_fit2, double* d_fit1, int localNum, int point_count, int nBlocks);
__global__ void p_sln(double* p, double* g, double* p0, double beta, int localNum);
__global__ void update_sln(double* p0, double* g0, double* W, double* m_temp, double* p, double* g, double* m_real, double* Wm, double* Wv, int localNum);
__global__ void g_sln(double* g, double* Vz_mat_mc, double* W, double* Vz, double* d_fit_temp, double lambda, int localNum, int base, int point_count, int lx);
double beta_sln(double* g, double* g0, int prism_count);
double vector_dot_product(double* a, double* b, int count);

int CheckCount()
{
	int deviceCount = 0;
	cudaGetDeviceCount(&deviceCount);
	return deviceCount;
}

double* foo(int h_point_count, int h_prism_count, int h_lx, int h_ly, int h_lz, int h_kmax, int Max_GPU_Number, int nThreadPerBlock,  double h_z_obs, double h_dz, double h_zmax,
	double h_m_min, double h_m_max, double h_epsilon, double h_lambda, double h_sigma,double wn, double *zc, double *thick, double* Vz, double* x, double* y)
{
	struct Vz_struct VzX;
	double xmin, xmax, ymin, ymax, dx, dy;
	double* h_m_result, * m1_x, * m1_y, * m1_z, * x_obs, * y_obs;
	int deviceCount = 0;
	cudaGetDeviceCount(&deviceCount);
	if (deviceCount > Max_GPU_Number)
	{
		deviceCount = Max_GPU_Number;
	}
	xy_cmp(h_point_count, h_lx, h_ly, x, y, &xmin, &xmax, &dx, &ymin, &ymax, &dy);

	x_obs = (double*)malloc(h_lx * sizeof(double));
	y_obs = (double*)malloc(h_ly * sizeof(double));
	for (int xi = 0; xi < h_lx; xi++)
	{
		*(x_obs + xi) = x[xi];
	}
	for (int yi = 0; yi < h_ly; yi++)
	{
		*(y_obs + yi) = y[yi * h_lx];
	}

	m1_x = (double*)malloc(2 * sizeof(double)); *(m1_x + 0) = xmin - 0.5 * dx; *(m1_x + 1) = xmin + 0.5 * dx;
	m1_y = (double*)malloc(2 * sizeof(double)); *(m1_y + 0) = ymin - 0.5 * dy; *(m1_y + 1) = ymin + 0.5 * dy;
	m1_z = (double*)malloc(2 * h_lz * sizeof(double));
	for (int zi = 0; zi < h_lz; zi++)
	{
		*(m1_z + zi) = zc[zi] - 0.5 * thick[zi];
		*(m1_z + zi + h_lz) = zc[zi] + 0.5 * thick[zi];
	}
	VzX.Vz = Vz;
	VzX.x_obs = x_obs;
	VzX.y_obs = y_obs;
	VzX.m1_x = m1_x;
	VzX.m1_y = m1_y;
	VzX.m1_z = m1_z;

	h_m_result = rwt_foc_inv(deviceCount, h_point_count, h_prism_count, h_lx, h_ly, h_lz, h_kmax, h_z_obs, h_m_min, h_m_max, h_epsilon, h_lambda, h_sigma, VzX, Max_GPU_Number, nThreadPerBlock,wn);

	cudaDeviceReset();
	return h_m_result;
}

void xy_cmp(int point_count, int lx, int ly, double* x, double* y, double* xmin, double* xmax, double* dx, double* ymin, double* ymax, double* dy)
{
	*xmin = x[0]; *xmax = x[0];
	*ymin = y[0]; *ymax = y[0];
	for (int ni = 1; ni < point_count; ni++)
	{
		*xmin = *xmin < x[ni] ? *xmin : x[ni];
		*xmax = *xmax > x[ni] ? *xmax : x[ni];
		*ymin = *ymin < y[ni] ? *ymin : y[ni];
		*ymax = *ymax > y[ni] ? *ymax : y[ni];
	}
	*dx = (*xmax - *xmin) / (lx - 1);
	*dy = (*ymax - *ymin) / (ly - 1);
}

double* rwt_foc_inv(int deviceCount, int h_point_count, int h_prism_count, int h_lx, int h_ly, int h_lz, int h_kmax,
	double h_z_obs, double h_m_min, double h_m_max, double h_epsilon, double h_lambda, double h_sigma, struct Vz_struct VzX, int Max_GPU_Number, int nThreadPerBlock,double wn)
{
	/*struct input_struct i_struct[Max_GPU_Number_list];
	struct Vz_mat_mc_struct v_struct[Max_GPU_Number_list];
	struct rfi_struct r_struct[Max_GPU_Number_list];*/
	struct input_struct *i_struct = new struct input_struct[Max_GPU_Number];
	struct Vz_mat_mc_struct *v_struct = new struct Vz_mat_mc_struct[Max_GPU_Number];
	struct rfi_struct *r_struct = new struct rfi_struct[Max_GPU_Number];

	int k = 0;
	double alpha, beta, rms, h_d_square, h_phi_m;
	double* h_data_misfit = (double*)malloc(h_point_count * sizeof(double));
	double* h_data_fitting = (double*)malloc(h_point_count * sizeof(double));
	double* h_g = (double*)malloc(h_prism_count * sizeof(double));
	double* h_g0 = (double*)malloc(h_prism_count * sizeof(double));
	double* h_q = (double*)malloc((h_prism_count + h_point_count) * sizeof(double));
	double* h_d_fit_temp = (double*)malloc((h_prism_count + h_point_count) * sizeof(double));
	double* inv_result = (double*)malloc(h_prism_count * sizeof(double));

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		cudaStreamCreate(&i_struct[i].stream);
		cudaMalloc((void**)&i_struct[i].d_Vz, h_point_count * sizeof(double));
		cudaMalloc((void**)&i_struct[i].d_x_obs, h_lx * sizeof(double));
		cudaMalloc((void**)&i_struct[i].d_y_obs, h_ly * sizeof(double));
		cudaMalloc((void**)&i_struct[i].d_m1_x, 2 * sizeof(double));
		cudaMalloc((void**)&i_struct[i].d_m1_y, 2 * sizeof(double));
		cudaMalloc((void**)&i_struct[i].d_m1_z, 2 * h_lz * sizeof(double));

		cudaMallocHost((void**)&i_struct[i].h_Vz, h_point_count * sizeof(double));
		cudaMallocHost((void**)&i_struct[i].h_x_obs, h_lx * sizeof(double));
		cudaMallocHost((void**)&i_struct[i].h_y_obs, h_ly * sizeof(double));
		cudaMallocHost((void**)&i_struct[i].h_m1_x, 2 * sizeof(double));
		cudaMallocHost((void**)&i_struct[i].h_m1_y, 2 * sizeof(double));
		cudaMallocHost((void**)&i_struct[i].h_m1_z, 2 * h_lz * sizeof(double));

		memcpy(i_struct[i].h_Vz, VzX.Vz, h_point_count * sizeof(double));
		memcpy(i_struct[i].h_x_obs, VzX.x_obs, h_lx * sizeof(double));
		memcpy(i_struct[i].h_y_obs, VzX.y_obs, h_ly * sizeof(double));
		memcpy(i_struct[i].h_m1_x, VzX.m1_x, 2 * sizeof(double));
		memcpy(i_struct[i].h_m1_y, VzX.m1_y, 2 * sizeof(double));
		memcpy(i_struct[i].h_m1_z, VzX.m1_z, 2 * h_lz * sizeof(double));
	}

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		cudaMemcpyAsync(i_struct[i].d_Vz, i_struct[i].h_Vz, h_point_count * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);
		cudaMemcpyAsync(i_struct[i].d_x_obs, i_struct[i].h_x_obs, h_lx * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);
		cudaMemcpyAsync(i_struct[i].d_y_obs, i_struct[i].h_y_obs, h_ly * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);
		cudaMemcpyAsync(i_struct[i].d_m1_x, i_struct[i].h_m1_x, 2 * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);
		cudaMemcpyAsync(i_struct[i].d_m1_y, i_struct[i].h_m1_y, 2 * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);
		cudaMemcpyAsync(i_struct[i].d_m1_z, i_struct[i].h_m1_z, 2 * h_lz * sizeof(double), cudaMemcpyHostToDevice, i_struct[i].stream);

		cudaStreamSynchronize(i_struct[i].stream);
	}

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		cudaStreamDestroy(i_struct[i].stream);
		cudaStreamCreate(&v_struct[i].stream);
		cudaMalloc((void**)&v_struct[i].d_Vz_mat_mc, h_prism_count * sizeof(double));

		v_struct[i].nBlocks = h_prism_count / nThreadPerBlock + ((h_prism_count % nThreadPerBlock) ? 1 : 0);
		Vz_mat_mc_sln << <v_struct[i].nBlocks, nThreadPerBlock, 0, v_struct[i].stream >> > (v_struct[i].d_Vz_mat_mc, i_struct[i].d_x_obs, i_struct[i].d_y_obs,
			i_struct[i].d_m1_x, i_struct[i].d_m1_y, i_struct[i].d_m1_z, h_z_obs, h_lx, h_lz, h_point_count, h_prism_count);
		cudaStreamSynchronize(v_struct[i].stream);
	}
	for (int i = 0; i < deviceCount; i++)
	{
		r_struct[i].localNum = h_prism_count / deviceCount;
	}
	for (int i = 0; i < h_prism_count % deviceCount; i++)
	{
		r_struct[i].localNum++;
	}

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		cudaStreamDestroy(v_struct[i].stream);
		cudaStreamCreate(&r_struct[i].stream);

		r_struct[i].nBlocks = r_struct[i].localNum / nThreadPerBlock + ((r_struct[i].localNum % nThreadPerBlock) ? 1 : 0);
		r_struct[i].nBlocks_Am = (h_prism_count + h_point_count) / nThreadPerBlock + (((h_prism_count + h_point_count) % nThreadPerBlock) ? 1 : 0);
		r_struct[i].nBlocks_Gm = h_point_count / nThreadPerBlock + ((h_point_count % nThreadPerBlock) ? 1 : 0);
		r_struct[i].base = 0;
		for (int j = 0; j < i; j++)
		{
			r_struct[i].base += r_struct[j].localNum;
		}
		cudaMalloc((void**)&r_struct[i].d_local_Wm, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_Wv, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_W, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_g, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_g0, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_p, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_p0, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_q1, r_struct[i].nBlocks * h_point_count * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_q2, (h_prism_count + h_point_count) * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_m_temp, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_m_real, r_struct[i].localNum * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_d_fit1, r_struct[i].nBlocks * h_point_count * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_d_fit2, h_point_count * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_d_fit_temp1, r_struct[i].nBlocks * h_point_count * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_local_d_fit_temp2, (h_prism_count + h_point_count) * sizeof(double));
		cudaMalloc((void**)&r_struct[i].d_d_fit_temp, (h_prism_count + h_point_count) * sizeof(double));

		cudaMallocHost((void**)&r_struct[i].h_local_g, r_struct[i].localNum * sizeof(double));
		cudaMallocHost((void**)&r_struct[i].h_local_g0, r_struct[i].localNum * sizeof(double));
		cudaMallocHost((void**)&r_struct[i].h_local_q, (h_prism_count + h_point_count) * sizeof(double));
		cudaMallocHost((void**)&r_struct[i].h_local_m_real, r_struct[i].localNum * sizeof(double));
		cudaMallocHost((void**)&r_struct[i].h_local_d_fit, h_point_count * sizeof(double));
		cudaMallocHost((void**)&r_struct[i].h_local_d_fit_temp, (h_prism_count + h_point_count) * sizeof(double));

		W_init_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_Wm, r_struct[i].d_local_Wv, r_struct[i].d_local_W,
			r_struct[i].d_local_m_temp, r_struct[i].d_local_m_real, v_struct[i].d_Vz_mat_mc, h_sigma, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx,wn);
		g0_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_g, v_struct[i].d_Vz_mat_mc, r_struct[i].d_local_W,
			i_struct[i].d_Vz, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx);
		cudaMemcpyAsync(r_struct[i].h_local_g, r_struct[i].d_local_g, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
		cudaStreamSynchronize(r_struct[i].stream);
	}

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		for (int j = 0; j < r_struct[i].localNum; j++)
		{
			h_g[j + r_struct[i].base] = r_struct[i].h_local_g[j];
		}
	}
	while (k < h_kmax)
	{
		k++;
		if (k == 1)
		{
#pragma omp parallel num_threads(deviceCount)
			{
				int i = omp_get_thread_num();
				cudaSetDevice(i);
				cudaMemcpy(r_struct[i].d_local_p, r_struct[i].d_local_g, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToDevice);
				cudaStreamSynchronize(r_struct[i].stream);
			}
		}
		else
		{
			if (k == 2)
			{
				h_phi_m = 0;

#pragma omp parallel num_threads(deviceCount)
				{
					int i = omp_get_thread_num();
					cudaSetDevice(i);
					cudaMemcpyAsync(r_struct[i].h_local_m_real, r_struct[i].d_local_m_real, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
					cudaStreamSynchronize(r_struct[i].stream);
				}
				for (int i = 0; i < deviceCount; i++)
				{
					for (int j = 0; j < r_struct[i].localNum; j++)
					{
						h_phi_m += (r_struct[i].h_local_m_real[j] * r_struct[i].h_local_m_real[j]) / (r_struct[i].h_local_m_real[j] * r_struct[i].h_local_m_real[j] + h_sigma * h_sigma);
					}
				}
				h_lambda = h_d_square / h_phi_m;
			}
			else
			{
				h_lambda = h_lambda / 2;
			}

#pragma omp parallel num_threads(deviceCount)
			{
				int i = omp_get_thread_num();
				cudaSetDevice(i);

				update_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_p0, r_struct[i].d_local_g0, r_struct[i].d_local_W,
					r_struct[i].d_local_m_temp, r_struct[i].d_local_p, r_struct[i].d_local_g, r_struct[i].d_local_m_real, r_struct[i].d_local_Wm, r_struct[i].d_local_Wv, r_struct[i].localNum);

				A_mult_v_col_sln << <r_struct[i].nBlocks, nThreadPerBlock, nThreadPerBlock * sizeof(double), r_struct[i].stream>> > (r_struct[i].d_local_d_fit_temp1, v_struct[i].d_Vz_mat_mc, r_struct[i].d_local_W,
					r_struct[i].d_local_m_temp, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx, nThreadPerBlock);
				A_mult_v_sum_sln << <r_struct[i].nBlocks_Am, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_d_fit_temp2, r_struct[i].d_local_d_fit_temp1, r_struct[i].d_local_m_temp,
					h_lambda, r_struct[i].localNum, r_struct[i].base, h_point_count, h_prism_count, r_struct[i].nBlocks);

				cudaMemcpyAsync(r_struct[i].h_local_d_fit_temp, r_struct[i].d_local_d_fit_temp2, (h_prism_count + h_point_count) * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
				cudaStreamSynchronize(r_struct[i].stream);
			}
			memset(h_d_fit_temp, 0, (h_prism_count + h_point_count) * sizeof(double));
			for (int i = 0; i < deviceCount; i++)
			{
				for (int j = 0; j < (h_prism_count + h_point_count); j++)
				{
					h_d_fit_temp[j] += r_struct[i].h_local_d_fit_temp[j];
				}
			}

#pragma omp parallel num_threads(deviceCount)
			{
				int i = omp_get_thread_num();
				cudaSetDevice(i);
				cudaMemcpyAsync(r_struct[i].d_d_fit_temp, h_d_fit_temp, (h_prism_count + h_point_count) * sizeof(double), cudaMemcpyHostToDevice, r_struct[i].stream);
				g_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_g, v_struct[i].d_Vz_mat_mc, r_struct[i].d_local_W,
					i_struct[i].d_Vz, r_struct[i].d_d_fit_temp, h_lambda, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx);
				cudaMemcpyAsync(r_struct[i].h_local_g, r_struct[i].d_local_g, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
				cudaMemcpyAsync(r_struct[i].h_local_g0, r_struct[i].d_local_g0, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
				cudaStreamSynchronize(r_struct[i].stream);
			}

#pragma omp parallel num_threads(deviceCount)
			{
				int i = omp_get_thread_num();
				cudaSetDevice(i);
				for (int j = 0; j < r_struct[i].localNum; j++)
				{
					h_g[j + r_struct[i].base] = r_struct[i].h_local_g[j];
					h_g0[j + r_struct[i].base] = r_struct[i].h_local_g0[j];
				}
			}
			beta = beta_sln(h_g, h_g0, h_prism_count);
			//beta = vector_dot_product(h_g, h_g, h_prism_count) / vector_dot_product(h_g0, h_g0, h_prism_count);

#pragma omp parallel num_threads(deviceCount)
			{
				int i = omp_get_thread_num();
				cudaSetDevice(i);
				p_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_p, r_struct[i].d_local_g, r_struct[i].d_local_p0, beta, r_struct[i].localNum);
				cudaStreamSynchronize(r_struct[i].stream);
			}
		}

#pragma omp parallel num_threads(deviceCount)
		{
			int i = omp_get_thread_num();
			cudaSetDevice(i);
			A_mult_v_col_sln << <r_struct[i].nBlocks, nThreadPerBlock,nThreadPerBlock * sizeof(double), r_struct[i].stream >> > (r_struct[i].d_local_q1, v_struct[i].d_Vz_mat_mc, r_struct[i].d_local_W, r_struct[i].d_local_p, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx, nThreadPerBlock);
			A_mult_v_sum_sln << <r_struct[i].nBlocks_Am, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_q2, r_struct[i].d_local_q1, r_struct[i].d_local_p, h_lambda, r_struct[i].localNum, r_struct[i].base, h_point_count, h_prism_count, r_struct[i].nBlocks);

			cudaMemcpyAsync(r_struct[i].h_local_q, r_struct[i].d_local_q2, (h_prism_count + h_point_count) * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
			cudaStreamSynchronize(r_struct[i].stream);
		}
		memset(h_q, 0, (h_prism_count + h_point_count) * sizeof(double));
		for (int i = 0; i < deviceCount; i++)
		{
			for (int j = 0; j < (h_prism_count + h_point_count); j++)
			{
				h_q[j] += r_struct[i].h_local_q[j];
			}
		}
		alpha = vector_dot_product(h_g, h_g, h_prism_count) / vector_dot_product(h_q, h_q, (h_prism_count + h_point_count));

#pragma omp parallel num_threads(deviceCount)
		{
			int i = omp_get_thread_num();
			cudaSetDevice(i);
			m_sln << <r_struct[i].nBlocks, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_m_temp, r_struct[i].d_local_m_real,
				r_struct[i].d_local_p, r_struct[i].d_local_W, alpha, h_m_min, h_m_max, r_struct[i].localNum);
			G_mult_m_col_sln << <r_struct[i].nBlocks, nThreadPerBlock, nThreadPerBlock * sizeof(double), r_struct[i].stream >> > (r_struct[i].d_local_d_fit1, v_struct[i].d_Vz_mat_mc, r_struct[i].d_local_m_real, r_struct[i].localNum, r_struct[i].base, h_point_count, h_lx, nThreadPerBlock);
			G_mult_m_sum_sln << <r_struct[i].nBlocks_Gm, nThreadPerBlock, 0, r_struct[i].stream >> > (r_struct[i].d_local_d_fit2, r_struct[i].d_local_d_fit1, r_struct[i].localNum, h_point_count, r_struct[i].nBlocks);

			cudaMemcpyAsync(r_struct[i].h_local_d_fit, r_struct[i].d_local_d_fit2, h_point_count * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
			cudaStreamSynchronize(r_struct[i].stream);
		}
		memset(h_data_fitting, 0, h_point_count * sizeof(double));
		for (int i = 0; i < deviceCount; i++)
		{
			for (int j = 0; j < h_point_count; j++)
			{
				h_data_fitting[j] += r_struct[i].h_local_d_fit[j];
			}
		}
		for (int j = 0; j < h_point_count; j++)
		{
			h_data_misfit[j] = VzX.Vz[j] - h_data_fitting[j];
		}
		h_d_square = vector_dot_product(h_data_misfit, h_data_misfit, h_point_count);
		rms = sqrt(h_d_square / h_point_count);
		if (rms <= h_epsilon)
		{
			break;
		}
	}

#pragma omp parallel num_threads(deviceCount)
	{
		int i = omp_get_thread_num();
		cudaSetDevice(i);
		cudaMemcpyAsync(r_struct[i].h_local_m_real, r_struct[i].d_local_m_real, r_struct[i].localNum * sizeof(double), cudaMemcpyDeviceToHost, r_struct[i].stream);
		cudaStreamSynchronize(r_struct[i].stream);
		for (int j = 0; j < r_struct[i].localNum; j++)
		{
			inv_result[j + r_struct[i].base] = r_struct[i].h_local_m_real[j];
		}
		cudaFreeHost(i_struct[i].h_Vz);
		cudaFreeHost(i_struct[i].h_x_obs);
		cudaFreeHost(i_struct[i].h_y_obs);
		cudaFreeHost(i_struct[i].h_m1_x);
		cudaFreeHost(i_struct[i].h_m1_y);
		cudaFreeHost(i_struct[i].h_m1_z);
		cudaFreeHost(r_struct[i].h_local_g);
		cudaFreeHost(r_struct[i].h_local_g0);
		cudaFreeHost(r_struct[i].h_local_q);
		cudaFreeHost(r_struct[i].h_local_m_real);
		cudaFreeHost(r_struct[i].h_local_d_fit);
		cudaFreeHost(r_struct[i].h_local_d_fit_temp);
		cudaFree(i_struct[i].d_Vz);
		cudaFree(i_struct[i].d_x_obs);
		cudaFree(i_struct[i].d_y_obs);
		cudaFree(i_struct[i].d_m1_x);
		cudaFree(i_struct[i].d_m1_y);
		cudaFree(i_struct[i].d_m1_z);
		cudaFree(v_struct[i].d_Vz_mat_mc);
		cudaFree(r_struct[i].d_local_Wm);
		cudaFree(r_struct[i].d_local_Wv);
		cudaFree(r_struct[i].d_local_W);
		cudaFree(r_struct[i].d_local_g);
		cudaFree(r_struct[i].d_local_g0);
		cudaFree(r_struct[i].d_local_p);
		cudaFree(r_struct[i].d_local_p0);
		cudaFree(r_struct[i].d_local_q1);
		cudaFree(r_struct[i].d_local_q2);
		cudaFree(r_struct[i].d_local_m_temp);
		cudaFree(r_struct[i].d_local_m_real);
		cudaFree(r_struct[i].d_local_d_fit1);
		cudaFree(r_struct[i].d_local_d_fit2);
		cudaFree(r_struct[i].d_local_d_fit_temp1);
		cudaFree(r_struct[i].d_local_d_fit_temp2);
		cudaFree(r_struct[i].d_d_fit_temp);
		cudaStreamDestroy(r_struct[i].stream);
	}
	//free(h_data_misfit); free(h_data_fitting); free(h_g); free(h_g0); free(h_q); free(h_d_fit_temp);

	return inv_result;
}

__global__ void Vz_mat_mc_sln(double* Vz_mat_mc, double* x_obs, double* y_obs, double* m1_x, double* m1_y, double* m1_z, double z_obs, int lx, int lz, int point_count, int prism_count)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int obs_x, obs_y, prm_z;
	double r0, r1, r2, r3, r4, r5, r6, r7;
	double xt1, xt2, yt1, yt2, zt1, zt2;
	double d_G = 66.7;

	if (i < prism_count)
	{
		obs_x = (i % point_count) % lx;
		obs_y = (i % point_count) / lx;
		prm_z = i / point_count;
		xt1 = x_obs[obs_x] - m1_x[0]; xt2 = x_obs[obs_x] - m1_x[1];
		yt1 = y_obs[obs_y] - m1_y[0]; yt2 = y_obs[obs_y] - m1_y[1];
		zt1 = z_obs - m1_z[prm_z]; zt2 = z_obs - m1_z[prm_z + lz];

		r0 = sqrt(pow(xt1, 2) + pow(yt1, 2) + pow(zt1, 2));
		r1 = sqrt(pow(xt1, 2) + pow(yt1, 2) + pow(zt2, 2));
		r2 = sqrt(pow(xt1, 2) + pow(yt2, 2) + pow(zt1, 2));
		r3 = sqrt(pow(xt1, 2) + pow(yt2, 2) + pow(zt2, 2));
		r4 = sqrt(pow(xt2, 2) + pow(yt1, 2) + pow(zt1, 2));
		r5 = sqrt(pow(xt2, 2) + pow(yt1, 2) + pow(zt2, 2));
		r6 = sqrt(pow(xt2, 2) + pow(yt2, 2) + pow(zt1, 2));
		r7 = sqrt(pow(xt2, 2) + pow(yt2, 2) + pow(zt2, 2));
		Vz_mat_mc[i] += d_G * (-atan(xt1 * yt1 / zt1 / r0) + atan(xt1 * yt1 / zt2 / r1) + atan(xt1 * yt2 / zt1 / r2) - atan(xt1 * yt2 / zt2 / r3)
			+ atan(xt2 * yt1 / zt1 / r4) - atan(xt2 * yt1 / zt2 / r5) - atan(xt2 * yt2 / zt1 / r6) + atan(xt2 * yt2 / zt2 / r7));
	}
}

__global__ void W_init_sln(double* Wm, double* Wv, double* W, double* m_temp, double* m_real, double* Vz_mat_mc, double sigma, int localNum, int base, int point_count, int lx,double wn)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int i_base, m, n, px, py, pi, pj, pk, index;

	if (i < localNum)
	{
		Wm[i] = 0; m_temp[i] = 0; m_real[i] = 0;
		i_base = i + base;
		px = (i_base % point_count) % lx + 1;
		py = (i_base % point_count) / lx + 1;
		pk = i_base / point_count + 1;
		for (int j = 0; j < point_count; j++)
		{
			m = j % lx + 1; n = j / lx + 1;
			pi = abs(m - px) + 1;
			pj = abs(n - py) + 1;
			index = (pk - 1) * point_count + (pj - 1) * lx + pi - 1;
			Wm[i] += pow(Vz_mat_mc[index], 2);
		}
		/*Wm[i] = 1 / sqrt(sqrt(Wm[i]));
		Wv[i] = pow(sigma, 2) * Wm[i];*/
		Wm[i] = 1 / pow(Wm[i], wn);
		Wv[i] = pow(sigma, 2) * Wm[i];
		W[i] = sqrt(Wv[i]);
	}
}

__global__ void g0_sln(double* g, double* Vz_mat_mc, double* W, double* Vz, int localNum, int base, int point_count, int lx)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int i_base, m, n, px, py, pi, pj, pk, index;

	if (i < localNum)
	{
		g[i] = 0;
		i_base = i + base;
		px = (i_base % point_count) % lx + 1;
		py = (i_base % point_count) / lx + 1;
		pk = i_base / point_count + 1;
		for (int j = 0; j < point_count; j++)
		{
			m = j % lx + 1; n = j / lx + 1;
			pi = abs(m - px) + 1;
			pj = abs(n - py) + 1;
			index = (pk - 1) * point_count + (pj - 1) * lx + pi - 1;
			g[i] += Vz_mat_mc[index] * W[i] * Vz[j];
		}
	}
}

__global__ void A_mult_v_col_sln(double* q, double* Vz_mat_mc, double* W, double* vector, int localNum, int base, int point_count, int lx, int nThreadPerBlock)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int i_base, m, n, px, py, pi, pj, pk, index;
	double temp;
	extern __shared__ double V_temp_shared[];
	//cudaMalloc((void**)V_temp_shared, nThreadPerBlock * sizeof(double));


	if (i < localNum)
	{
		i_base = i + base;
		px = (i_base % point_count) % lx + 1;
		py = (i_base % point_count) / lx + 1;
		pk = i_base / point_count + 1;
		for (int j = 0; j < point_count; j++)
		{
			m = j % lx + 1; n = j / lx + 1;
			pi = abs(m - px) + 1;
			pj = abs(n - py) + 1;
			index = (pk - 1) * point_count + (pj - 1) * lx + pi - 1;
			V_temp_shared[threadIdx.x] = Vz_mat_mc[index] * W[i] * vector[i];
			//*(V_temp_shared + threadIdx.x) = Vz_mat_mc[index] * W[i] * vector[i];
			__syncthreads();
			temp = 0;
			if (threadIdx.x == 0)
			{
				for (int k = 0; k < nThreadPerBlock; k++)
				{
					temp += V_temp_shared[k];
					//temp += *(V_temp_shared + k);
				}
				q[blockIdx.x * point_count + j] = temp;
			}
			__syncthreads();
		}
	}
}

__global__ void A_mult_v_sum_sln(double* q2, double* q1, double* vector, double lambda, int localNum, int base, int point_count, int prism_count, int nBlocks)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if (i < (prism_count + point_count))
	{
		q2[i] = 0;
		if (i < point_count)
		{
			for (int j = 0; j < nBlocks; j++)
			{
				q2[i] += q1[j * point_count + i];
			}
		}
		else if (i >= (point_count + base) && i < (point_count + base + localNum))
		{
			q2[i] = sqrt(lambda) * vector[i - point_count - base];
		}
	}
}

__global__ void m_sln(double* m_temp, double* m_real, double* p, double* W, double alpha, double m_min, double m_max, int localNum)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if (i < localNum)
	{
		m_temp[i] += alpha * p[i];
		m_real[i] = W[i] * m_temp[i];
		if (m_real[i] < m_min)
		{
			m_real[i] = m_min;
		}
		else if (m_real[i] > m_max)
		{
			m_real[i] = m_max;
		}
	}
}

__global__ void G_mult_m_col_sln(double* d_fit, double* Vz_mat_mc, double* m_temp, int localNum, int base, int point_count, int lx, int nThreadPerBlock)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int i_base, m, n, px, py, pi, pj, pk, index;
	double temp;
	extern __shared__ double V_temp_shared[];
	//cudaMalloc((void**)V_temp_shared, nThreadPerBlock * sizeof(double));

	if (i < localNum)
	{
		i_base = i + base;
		px = (i_base % point_count) % lx + 1;
		py = (i_base % point_count) / lx + 1;
		pk = i_base / point_count + 1;
		for (int j = 0; j < point_count; j++)
		{
			m = j % lx + 1; n = j / lx + 1;
			pi = abs(m - px) + 1;
			pj = abs(n - py) + 1;
			index = (pk - 1) * point_count + (pj - 1) * lx + pi - 1;
			V_temp_shared[threadIdx.x] = Vz_mat_mc[index] * m_temp[i];
			//*(V_temp_shared + threadIdx.x) = Vz_mat_mc[index] * m_temp[i];
			__syncthreads();
			temp = 0;
			if (threadIdx.x == 0)
			{
				for (int k = 0; k < nThreadPerBlock; k++)
				{
					temp += V_temp_shared[k];
					//temp += *(V_temp_shared + k);
				}
				d_fit[blockIdx.x * point_count + j] = temp;
			}
			__syncthreads();
		}
	}
}

__global__ void G_mult_m_sum_sln(double* d_fit2, double* d_fit1, int localNum, int point_count, int nBlocks)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if (i < point_count)
	{
		d_fit2[i] = 0;
		for (int j = 0; j < nBlocks; j++)
		{
			d_fit2[i] += d_fit1[j * point_count + i];
		}
	}
}

__global__ void p_sln(double* p, double* g, double* p0, double beta, int localNum)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if (i < localNum)
	{
		p[i] = g[i] + beta * p0[i];
	}
}

__global__ void update_sln(double* p0, double* g0, double* W, double* m_temp, double* p, double* g, double* m_real, double* Wm, double* Wv, int localNum)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if (i < localNum)
	{
		p0[i] = p[i];
		g0[i] = g[i];
		W[i] = sqrt(pow(m_real[i], 2) * Wm[i] + Wv[i]);
		m_temp[i] = m_real[i] / W[i];
	}
}

__global__ void g_sln(double* g, double* Vz_mat_mc, double* W, double* Vz, double* d_fit_temp, double lambda, int localNum, int base, int point_count, int lx)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;
	int i_base, m, n, px, py, pi, pj, pk, index;

	if (i < localNum)
	{
		g[i] = 0;
		i_base = i + base;
		px = (i_base % point_count) % lx + 1;
		py = (i_base % point_count) / lx + 1;
		pk = i_base / point_count + 1;
		for (int j = 0; j < point_count; j++)
		{
			m = j % lx + 1; n = j / lx + 1;
			pi = abs(m - px) + 1;
			pj = abs(n - py) + 1;
			index = (pk - 1) * point_count + (pj - 1) * lx + pi - 1;
			g[i] += Vz_mat_mc[index] * W[i] * (Vz[j] - d_fit_temp[j]);
		}
		g[i] += sqrt(lambda) * (0 - d_fit_temp[i_base + point_count]);
	}
}

double beta_sln(double* g, double* g0, int prism_count)
{
	double beta;
	double beta_temp = 0;
	for (int i = 0; i < prism_count; i++)
	{
		beta_temp += g[i] * (g[i] - g0[i]);
	}
	beta = beta_temp / vector_dot_product(g0, g0, prism_count);
	return beta;
}

double vector_dot_product(double* a, double* b, int count)
{
	double result = 0;
	for (int vi = 0; vi < count; vi++)
	{
		result += a[vi] * b[vi];
	}
	return result;
}
