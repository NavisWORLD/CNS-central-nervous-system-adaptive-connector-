#include "cns_state_core.h"
#include <math.h>
#include <string.h>

static double cns_clamp(double x, double lo, double hi) { return x < lo ? lo : (x > hi ? hi : x); }

double cns_finite(double value, double fallback) { return isfinite(value) ? value : fallback; }

double cns_unit(double value, double low, double high) {
  if (!(high > low)) return NAN;
  return cns_clamp((cns_finite(value, 0.0) - low) / (high - low), 0.0, 1.0);
}

double cns_signed(double value, double scale) {
  if (!(scale > 0.0)) return NAN;
  return tanh(cns_finite(value, 0.0) / scale);
}

int cns_encode_12d(const double in[12], double out[12]) {
  if (!in || !out) return -1;
  const double pi = 3.14159265358979323846;
  const double phi = (1.0 + sqrt(5.0)) / 2.0;
  const double rms = cns_unit(in[0], 0.0, 1.0);
  const double freq = cns_unit(in[1], 0.0, 4000.0);
  const double flat = cns_unit(in[2], 0.0, 1.0);
  const double motion = cns_unit(in[9], 0.0, 1.0);
  const double light = cns_unit(in[10], 0.0, 1.0);
  out[0] = sqrt(fmax(rms, 0.0)) * (2.0 * freq - 1.0);
  out[1] = sin(cns_finite(in[3], 0.0));
  out[2] = 2.0 * flat - 1.0;
  out[3] = cns_signed(in[4], 10.0);
  out[4] = 2.0 * cns_unit(in[5], 0.0, 1.0) - 1.0;
  out[5] = cns_clamp(cns_finite(in[6], 0.0), -1.0, 1.0);
  out[6] = 2.0 * cns_unit(in[7], 0.0, 1.0) - 1.0;
  out[7] = 2.0 * cns_unit(in[8], 0.0, 1.0) - 1.0;
  out[8] = sin(2.0 * pi * freq) * rms;
  out[9] = cos(2.0 * pi * fmod(freq * phi, 1.0)) * (0.25 + 0.75 * rms);
  out[10] = 2.0 * (1.0 - fmin(1.0, fabs(motion - light))) - 1.0;
  out[11] = 2.0 * cns_unit(in[11], 0.0, 1.0) - 1.0;
  return 0;
}

int cns_expand_42d(const double x12[12], const double ctx30[30], double out42[42]) {
  if (!x12 || !out42) return -1;
  memcpy(out42, x12, 12 * sizeof(double));
  for (int i = 0; i < 30; ++i) out42[12 + i] = tanh(cns_finite(ctx30 ? ctx30[i] : 0.0, 0.0));
  return 0;
}

int cns_weight_update(double w[2916], const double x[54], double reward, double lr, double decay, double limit) {
  if (!w || !x || lr < 0.0 || decay < 0.0 || decay >= 1.0 || limit <= 0.0) return -1;
  const double r = cns_clamp(reward, -1.0, 1.0);
  for (int i = 0; i < 54; ++i) {
    for (int j = 0; j < 54; ++j) {
      const int k = i * 54 + j;
      const double v = w[k] * (1.0 - decay) + lr * r * x[i] * x[j];
      w[k] = (i == j) ? 0.0 : cns_clamp(v, -limit, limit);
    }
  }
  return 0;
}

int cns_weight_modulation(const double w[2916], const double x[54], double out54[54]) {
  if (!w || !x || !out54) return -1;
  for (int i = 0; i < 54; ++i) {
    double sum = 0.0;
    for (int j = 0; j < 54; ++j) sum += w[i * 54 + j] * x[j];
    out54[i] = tanh(sum);
  }
  return 0;
}

int cns_recurrent_tail(const double prior[54], const double mod[54], double memory_strength, double entropy, double out12[12]) {
  if (!prior || !mod || !out12) return -1;
  const double q = cns_unit(entropy, 0.0, 1.0);
  const double mem = fmax(0.0, cns_finite(memory_strength, 0.0));
  for (int i = 0; i < 12; ++i) out12[i] = tanh(0.35 * prior[i] + 0.35 * mod[i] + 0.15 * mem + 0.15 * (2.0 * q - 1.0));
  return 0;
}

int cns_assemble_54d(const double context42[42], const double tail12[12], double out54[54]) {
  if (!context42 || !tail12 || !out54) return -1;
  memcpy(out54, context42, 42 * sizeof(double));
  memcpy(out54 + 42, tail12, 12 * sizeof(double));
  return 0;
}

int cns_blend_54d(const double base54[54], const double mixed54[54], double out54[54]) {
  if (!base54 || !mixed54 || !out54) return -1;
  for (int i = 0; i < 54; ++i) out54[i] = tanh(0.7 * base54[i] + 0.3 * mixed54[i]);
  return 0;
}
