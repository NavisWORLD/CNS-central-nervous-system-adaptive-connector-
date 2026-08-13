pub const SENSORY_DIM: usize = 12;
pub const CONTEXT_DIM: usize = 42;
pub const STATE_DIM: usize = 54;

#[link(name = "cns_state_core")]
extern "C" {
    fn cns_encode_12d(input: *const f64, output: *mut f64) -> i32;
    fn cns_expand_42d(input: *const f64, context: *const f64, output: *mut f64) -> i32;
    fn cns_weight_update(matrix: *mut f64, state: *const f64, gain: f64, rate: f64, decay: f64, limit: f64) -> i32;
    fn cns_weight_modulation(matrix: *const f64, state: *const f64, output: *mut f64) -> i32;
    fn cns_recurrent_tail(prior: *const f64, modulation: *const f64, memory: f64, entropy: f64, output: *mut f64) -> i32;
    fn cns_assemble_54d(context: *const f64, tail: *const f64, output: *mut f64) -> i32;
    fn cns_blend_54d(base: *const f64, mixed: *const f64, output: *mut f64) -> i32;
}

pub fn encode12(input: &[f64; 12]) -> Result<[f64; 12], i32> {
    let mut out = [0.0; 12];
    let rc = unsafe { cns_encode_12d(input.as_ptr(), out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}

pub fn expand42(input: &[f64; 12], context: &[f64; 30]) -> Result<[f64; 42], i32> {
    let mut out = [0.0; 42];
    let rc = unsafe { cns_expand_42d(input.as_ptr(), context.as_ptr(), out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}

pub fn matrix_step(matrix: &mut [f64; 2916], state: &[f64; 54], gain: f64, rate: f64, decay: f64, limit: f64) -> Result<(), i32> {
    let rc = unsafe { cns_weight_update(matrix.as_mut_ptr(), state.as_ptr(), gain, rate, decay, limit) };
    if rc == 0 { Ok(()) } else { Err(rc) }
}

pub fn modulation(matrix: &[f64; 2916], state: &[f64; 54]) -> Result<[f64; 54], i32> {
    let mut out = [0.0; 54];
    let rc = unsafe { cns_weight_modulation(matrix.as_ptr(), state.as_ptr(), out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}

pub fn recurrent_tail(prior: &[f64; 54], modulation: &[f64; 54], memory: f64, entropy: f64) -> Result<[f64; 12], i32> {
    let mut out = [0.0; 12];
    let rc = unsafe { cns_recurrent_tail(prior.as_ptr(), modulation.as_ptr(), memory, entropy, out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}

pub fn assemble54(context: &[f64; 42], tail: &[f64; 12]) -> Result<[f64; 54], i32> {
    let mut out = [0.0; 54];
    let rc = unsafe { cns_assemble_54d(context.as_ptr(), tail.as_ptr(), out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}

pub fn blend54(base: &[f64; 54], mixed: &[f64; 54]) -> Result<[f64; 54], i32> {
    let mut out = [0.0; 54];
    let rc = unsafe { cns_blend_54d(base.as_ptr(), mixed.as_ptr(), out.as_mut_ptr()) };
    if rc == 0 { Ok(out) } else { Err(rc) }
}
