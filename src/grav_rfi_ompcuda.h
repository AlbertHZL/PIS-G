#pragma once

#ifdef _MSC_VER
	#define DLLEXPORT __declspec(dllexport)
#else
	#define DLLEXPORT
#endif

extern "C" {
	DLLEXPORT double* foo(int h_point_count, int h_prism_count, int h_lx, int h_ly, int h_lz, int h_kmax, int a, int b, double h_z_obs, double h_dz, double h_zmax,
	double h_m_min, double h_m_max, double h_epsilon, double h_lambda, double h_sigma,double wn, double* zc, double* thick, double* Vz, double* x, double* y);

	DLLEXPORT int CheckCount();
}
