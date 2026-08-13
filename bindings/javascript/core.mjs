export const SENSORY_DIM = 12;
export const CONTEXT_DIM = 42;
export const STATE_DIM = 54;

export const finite = (x, fallback = 0) => Number.isFinite(Number(x)) ? Number(x) : fallback;

export function unit(x, low = 0, high = 1) {
  if (!(high > low)) throw new RangeError("high must exceed low");
  return Math.max(0, Math.min(1, (finite(x) - low) / (high - low)));
}

export function signed(x, scale = 1) {
  if (!(scale > 0)) throw new RangeError("scale must be positive");
  return Math.tanh(finite(x) / scale);
}

export function encode12(input = []) {
  if (input.length !== 12) throw new RangeError("input must contain 12 values");
  const rms = unit(input[0]);
  const freq = unit(input[1], 0, 4000);
  const flat = unit(input[2]);
  const phi = (1 + Math.sqrt(5)) / 2;
  const motion = unit(input[9]);
  const light = unit(input[10]);
  return [
    Math.sqrt(Math.max(rms, 0)) * (2 * freq - 1),
    Math.sin(finite(input[3])),
    2 * flat - 1,
    signed(input[4], 10),
    2 * unit(input[5]) - 1,
    Math.max(-1, Math.min(1, finite(input[6]))),
    2 * unit(input[7]) - 1,
    2 * unit(input[8]) - 1,
    Math.sin(2 * Math.PI * freq) * rms,
    Math.cos(2 * Math.PI * ((freq * phi) % 1)) * (0.25 + 0.75 * rms),
    2 * (1 - Math.min(1, Math.abs(motion - light))) - 1,
    2 * unit(input[11]) - 1,
  ];
}

export function expand42(x12, context30 = Array(30).fill(0)) {
  if (x12.length !== 12 || context30.length !== 30) throw new RangeError("invalid shape");
  return [...x12, ...context30.map(v => Math.tanh(finite(v)))];
}

export function weightUpdate(weights, state, reward = 1, learningRate = 0.002, decay = 0.001, limit = 1) {
  if (weights.length !== 2916 || state.length !== 54) throw new RangeError("invalid shape");
  const out = weights.slice();
  const r = Math.max(-1, Math.min(1, reward));
  for (let i = 0; i < 54; i++) for (let j = 0; j < 54; j++) {
    const k = i * 54 + j;
    const v = out[k] * (1 - decay) + learningRate * r * state[i] * state[j];
    out[k] = i === j ? 0 : Math.max(-limit, Math.min(limit, v));
  }
  return out;
}

export function weightModulation(weights, state) {
  if (weights.length !== 2916 || state.length !== 54) throw new RangeError("invalid shape");
  return Array.from({ length: 54 }, (_, i) => Math.tanh(state.reduce((sum, v, j) => sum + weights[i * 54 + j] * v, 0)));
}

export function recurrentTail(prior, modulation, memoryStrength, entropy) {
  if (prior.length !== 54 || modulation.length !== 54) throw new RangeError("invalid shape");
  const q = unit(entropy);
  const memory = Math.max(0, finite(memoryStrength));
  return Array.from({ length: 12 }, (_, i) => Math.tanh(0.35 * prior[i] + 0.35 * modulation[i] + 0.15 * memory + 0.15 * (2 * q - 1)));
}

export function assemble54(context42, tail12) {
  if (context42.length !== 42 || tail12.length !== 12) throw new RangeError("invalid shape");
  return [...context42, ...tail12];
}

export function blend54(base54, mixed54) {
  if (base54.length !== 54 || mixed54.length !== 54) throw new RangeError("invalid shape");
  return base54.map((v, i) => Math.tanh(0.7 * v + 0.3 * mixed54[i]));
}
