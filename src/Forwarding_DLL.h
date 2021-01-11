#pragma once

#ifdef _MSC_VER
	#define DLLEXPORT __declspec(dllexport)
#else
	#define DLLEXPORT
#endif

extern "C" {
	DLLEXPORT double* Forwarding(int lx, int ly, int point_count, int prism_count, double x_min, double dx, double x_max,
	double y_min, double dy, double y_max, double z_obs, double *x, double *y, double *mx, double *my, double *mz, double *p);
}
