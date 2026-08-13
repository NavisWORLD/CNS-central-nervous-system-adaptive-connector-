package statecore

import "math"

const SensoryDim = 12
const ContextDim = 42
const StateDim = 54

func finite(x float64) float64 {
	if math.IsNaN(x) || math.IsInf(x, 0) { return 0 }
	return x
}

func unit(x, low, high float64) float64 {
	v := (finite(x) - low) / (high - low)
	if v < 0 { return 0 }
	if v > 1 { return 1 }
	return v
}

func Encode12(input [12]float64) [12]float64 {
	r := unit(input[0], 0, 1)
	f := unit(input[1], 0, 4000)
	flat := unit(input[2], 0, 1)
	phi := (1 + math.Sqrt(5)) / 2
	motion := unit(input[9], 0, 1)
	light := unit(input[10], 0, 1)
	return [12]float64{
		math.Sqrt(math.Max(r, 0)) * (2*f - 1),
		math.Sin(finite(input[3])),
		2*flat - 1,
		math.Tanh(finite(input[4]) / 10),
		2*unit(input[5], 0, 1) - 1,
		math.Max(-1, math.Min(1, finite(input[6]))),
		2*unit(input[7], 0, 1) - 1,
		2*unit(input[8], 0, 1) - 1,
		math.Sin(2*math.Pi*f) * r,
		math.Cos(2*math.Pi*math.Mod(f*phi, 1)) * (0.25 + 0.75*r),
		2*(1-math.Min(1, math.Abs(motion-light))) - 1,
		2*unit(input[11], 0, 1) - 1,
	}
}

func Expand42(x12 [12]float64, context [30]float64) [42]float64 {
	var out [42]float64
	copy(out[:12], x12[:])
	for i, v := range context { out[12+i] = math.Tanh(finite(v)) }
	return out
}
