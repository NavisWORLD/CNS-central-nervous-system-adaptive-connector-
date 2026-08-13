#pragma once
#include <array>
#include <stdexcept>
extern "C" {
#include "../../c/include/cns_state_core.h"
}
namespace cns {
using State12 = std::array<double, 12>;
using State42 = std::array<double, 42>;
using State54 = std::array<double, 54>;
inline State12 encode(const State12& input) {
  State12 out{};
  if (cns_encode_12d(input.data(), out.data()) != 0) throw std::runtime_error("encode failed");
  return out;
}
inline State54 modulation(const std::array<double, 2916>& weights, const State54& state) {
  State54 out{};
  if (cns_weight_modulation(weights.data(), state.data(), out.data()) != 0) throw std::runtime_error("modulation failed");
  return out;
}
}
