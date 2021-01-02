# include "Forwarding_DLL.h"
# include <stdlib.h>
# include <stdio.h>
# include <string.h>
# include <math.h>
# include <time.h>

struct V_str
{
	double* Vxx;
	double* Vxy;
	double* Vxz;
	double* Vyy;
	double* Vyz;
	double* Vzz;
	double* Vz;
};

struct V_str Algorithm(int lx, int point_count, int prism_count, double z_obs, double* x, double* y, double* mx, double* my, double* mz, double* p);
double * ChangeData(int point_count, double* Vxx, double* Vxy, double* Vxz, double* Vyy, double* Vyz, double* Vzz, double* Vz);

const double G = 66.7;
const double G_10 = 66.7 / 10000;

double* Forwarding(int lx, int ly, int point_count, int prism_count, double x_min, double dx, double x_max,
	double y_min, double dy, double y_max, double z_obs, double* x, double* y, double* mx, double* my, double* mz, double* p)
{
	struct V_str V_s;
	double* m_result;
	V_s = Algorithm(lx, point_count, prism_count, z_obs, x, y, mx, my, mz, p);
	m_result = ChangeData(point_count, V_s.Vxx, V_s.Vxy, V_s.Vxz, V_s.Vyy, V_s.Vyz, V_s.Vzz, V_s.Vz);
	return m_result;
}

struct V_str Algorithm(int lx, int point_count, int prism_count, double z_obs, double* x, double* y, double* mx, double* my, double* mz, double* p)
{
	struct V_str V_str;
	double* Vxx = (double*)malloc(point_count * sizeof(double));
	double* Vxy = (double*)malloc(point_count * sizeof(double));
	double* Vxz = (double*)malloc(point_count * sizeof(double));
	double* Vyy = (double*)malloc(point_count * sizeof(double));
	double* Vyz = (double*)malloc(point_count * sizeof(double));
	double* Vzz = (double*)malloc(point_count * sizeof(double));
	double* Vz = (double*)malloc(point_count * sizeof(double));
	double r0, r1, r2, r3, r4, r5, r6, r7;
	double xt1, xt2, yt1, yt2, zt1, zt2;

	memset(Vxx, 0, point_count * sizeof(double));
	memset(Vxy, 0, point_count * sizeof(double));
	memset(Vxz, 0, point_count * sizeof(double));
	memset(Vyy, 0, point_count * sizeof(double));
	memset(Vyz, 0, point_count * sizeof(double));
	memset(Vzz, 0, point_count * sizeof(double));
	memset(Vz, 0, point_count * sizeof(double));

	for (int n = 0; n < point_count; n++)
	{
		for (int m = 0; m < prism_count; m++)
		{
			xt1 = x[n % lx] - mx[m]; xt2 = x[n % lx] - mx[prism_count + m];
			yt1 = y[n / lx] - my[m]; yt2 = y[n / lx] - my[prism_count + m];
			zt1 = z_obs - mz[m]; zt2 = z_obs - mz[prism_count + m];
			r0 = sqrt(pow(xt1, 2) + pow(yt1, 2) + pow(zt1, 2));
			r1 = sqrt(pow(xt1, 2) + pow(yt1, 2) + pow(zt2, 2));
			r2 = sqrt(pow(xt1, 2) + pow(yt2, 2) + pow(zt1, 2));
			r3 = sqrt(pow(xt1, 2) + pow(yt2, 2) + pow(zt2, 2));
			r4 = sqrt(pow(xt2, 2) + pow(yt1, 2) + pow(zt1, 2));
			r5 = sqrt(pow(xt2, 2) + pow(yt1, 2) + pow(zt2, 2));
			r6 = sqrt(pow(xt2, 2) + pow(yt2, 2) + pow(zt1, 2));
			r7 = sqrt(pow(xt2, 2) + pow(yt2, 2) + pow(zt2, 2));

			Vxx[n] += G * p[m] * (-atan(yt1 * zt1 / xt1 / r0) + atan(yt1 * zt2 / xt1 / r1) + atan(yt2 * zt1 / xt1 / r2) - atan(yt2 * zt2 / xt1 / r3)
				+ atan(yt1 * zt1 / xt2 / r4) - atan(yt1 * zt2 / xt2 / r5) - atan(yt2 * zt1 / xt2 / r6) + atan(yt2 * zt2 / xt2 / r7));
			Vxy[n] -= G * p[m] * (-log(zt1 + r0) + log(zt2 + r1) + log(zt1 + r2) - log(zt2 + r3)
				+ log(zt1 + r4) - log(zt2 + r5) - log(zt1 + r6) + log(zt2 + r7));
			Vxz[n] -= G * p[m] * (-log(yt1 + r0) + log(yt1 + r1) + log(yt2 + r2) - log(yt2 + r3)
				+ log(yt1 + r4) - log(yt1 + r5) - log(yt2 + r6) + log(yt2 + r7));
			Vyy[n] += G * p[m] * (-atan(xt1 * zt1 / yt1 / r0) + atan(xt1 * zt2 / yt1 / r1) + atan(xt1 * zt1 / yt2 / r2) - atan(xt1 * zt2 / yt2 / r3)
				+ atan(xt2 * zt1 / yt1 / r4) - atan(xt2 * zt2 / yt1 / r5) - atan(xt2 * zt1 / yt2 / r6) + atan(xt2 * zt2 / yt2 / r7));
			Vyz[n] -= G * p[m] * (-log(xt1 + r0) + log(xt1 + r1) + log(xt1 + r2) - log(xt1 + r3)
				+ log(xt2 + r4) - log(xt2 + r5) - log(xt2 + r6) + log(xt2 + r7));
			Vzz[n] += G * p[m] * (-atan(xt1 * yt1 / zt1 / r0) + atan(xt1 * yt1 / zt2 / r1) + atan(xt1 * yt2 / zt1 / r2) - atan(xt1 * yt2 / zt2 / r3)
				+ atan(xt2 * yt1 / zt1 / r4) - atan(xt2 * yt1 / zt2 / r5) - atan(xt2 * yt2 / zt1 / r6) + atan(xt2 * yt2 / zt2 / r7));
			Vz[n] -= G_10 * p[m] * (-(xt1 * log(yt1 + r0) + yt1 * log(xt1 + r0) + 2 * zt1 * atan((xt1 + yt1 + r0) / zt1))
				+ (xt1 * log(yt1 + r1) + yt1 * log(xt1 + r1) + 2 * zt2 * atan((xt1 + yt1 + r1) / zt2))
				+ (xt1 * log(yt2 + r2) + yt2 * log(xt1 + r2) + 2 * zt1 * atan((xt1 + yt2 + r2) / zt1))
				- (xt1 * log(yt2 + r3) + yt2 * log(xt1 + r3) + 2 * zt2 * atan((xt1 + yt2 + r3) / zt2))
				+ (xt2 * log(yt1 + r4) + yt1 * log(xt2 + r4) + 2 * zt1 * atan((xt2 + yt1 + r4) / zt1))
				- (xt2 * log(yt1 + r5) + yt1 * log(xt2 + r5) + 2 * zt2 * atan((xt2 + yt1 + r5) / zt2))
				- (xt2 * log(yt2 + r6) + yt2 * log(xt2 + r6) + 2 * zt1 * atan((xt2 + yt2 + r6) / zt1))
				+ (xt2 * log(yt2 + r7) + yt2 * log(xt2 + r7) + 2 * zt2 * atan((xt2 + yt2 + r7) / zt2)));
		}
	}

	V_str.Vxx = Vxx; V_str.Vxy = Vxy; V_str.Vxz = Vxz;
	V_str.Vyy = Vyy; V_str.Vyz = Vyz; V_str.Vzz = Vzz; V_str.Vz = Vz;

	return V_str;
}

double* ChangeData(int point_count, double* Vxx, double* Vxy, double* Vxz, double* Vyy, double* Vyz, double* Vzz, double* Vz)
{
	double* m_result = (double*)malloc(7 * point_count * sizeof(double));
	for (int rm = 0; rm < point_count; rm++)
	{
		m_result[rm] = Vxx[rm];
		m_result[rm + point_count] = Vxy[rm];
		m_result[rm + 2 * point_count] = Vxz[rm];
		m_result[rm + 3 * point_count] = Vyy[rm];
		m_result[rm + 4 * point_count] = Vyz[rm];
		m_result[rm + 5 * point_count] = Vzz[rm];
		m_result[rm + 6 * point_count] = Vz[rm];
	}
	return m_result;
}
