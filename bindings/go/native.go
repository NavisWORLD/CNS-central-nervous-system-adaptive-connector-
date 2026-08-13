package statecore

/*
#cgo CFLAGS: -I${SRCDIR}/../c/include
#cgo LDFLAGS: -lm
#include "cns_state_core.h"
*/
import "C"
import "unsafe"

func MatrixStep(matrix *[2916]float64, state *[54]float64, gain, rate, decay, limit float64) int {
	return int(C.cns_weight_update(
		(*C.double)(unsafe.Pointer(&matrix[0])),
		(*C.double)(unsafe.Pointer(&state[0])),
		C.double(gain), C.double(rate), C.double(decay), C.double(limit),
	))
}

func MatrixModulation(matrix *[2916]float64, state *[54]float64) ([54]float64, int) {
	var out [54]float64
	rc := C.cns_weight_modulation(
		(*C.double)(unsafe.Pointer(&matrix[0])),
		(*C.double)(unsafe.Pointer(&state[0])),
		(*C.double)(unsafe.Pointer(&out[0])),
	)
	return out, int(rc)
}

func Tail(prior, modulation *[54]float64, memoryStrength, entropy float64) ([12]float64, int) {
	var out [12]float64
	rc := C.cns_recurrent_tail(
		(*C.double)(unsafe.Pointer(&prior[0])),
		(*C.double)(unsafe.Pointer(&modulation[0])),
		C.double(memoryStrength), C.double(entropy),
		(*C.double)(unsafe.Pointer(&out[0])),
	)
	return out, int(rc)
}
