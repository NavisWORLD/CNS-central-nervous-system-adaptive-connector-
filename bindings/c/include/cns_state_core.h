#ifndef CNS_STATE_CORE_H
#define CNS_STATE_CORE_H
#ifdef __cplusplus
extern "C" {
#endif
#define CNS_SENSORY_DIM 12
#define CNS_CONTEXT_DIM 42
#define CNS_STATE_DIM 54
double cns_finite(double value, double fallback);
double cns_unit(double value, double low, double high);
double cns_signed(double value, double scale);
int cns_encode_12d(const double input12[12], double out12[12]);
int cns_expand_42d(const double x12[12], const double ctx30[30], double out42[42]);
int cns_weight_update(double weights[2916], const double state[54], double reward, double learning_rate, double decay, double clamp_value);
int cns_weight_modulation(const double weights[2916], const double state[54], double out54[54]);
int cns_recurrent_tail(const double prior[54], const double modulation[54], double memory_strength, double entropy, double out12[12]);
int cns_assemble_54d(const double context42[42], const double tail12[12], double out54[54]);
int cns_blend_54d(const double base54[54], const double mixed54[54], double out54[54]);
#ifdef __cplusplus
}
#endif
#endif
