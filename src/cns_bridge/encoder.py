from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from .normalization import unit, signed, finite


@dataclass(slots=True)
class SensorySnapshot:
    """Compact multimodal observation accepted by the reference 12D encoder.

    Inputs are summaries, not raw recordings. Applications may calculate these
    fields locally and discard raw audio/video immediately.
    """

    audio_rms: float = 0.0
    dominant_frequency_hz: float = 0.0
    spectral_flatness: float = 0.0
    geometric_phase_rad: float = 0.0
    phase_velocity: float = 0.0
    av_coherence: float = 0.0
    pleasure: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    motion_energy: float = 0.0
    luminance: float = 0.5
    entropy: float = 0.5


class CNS12DEncoder:
    """Reference 12-channel state encoder.

    These channels are an interoperable public schema, not a claim that they
    are physical spatial dimensions.
    """

    CHANNELS = (
        "frequency_mass",
        "geometric_phase",
        "spectral_flatness",
        "phase_velocity",
        "av_entanglement",
        "pleasure",
        "arousal",
        "dominance",
        "audio_psi",
        "phi_harmonics",
        "motion_luminance_coherence",
        "entropy",
    )

    PHI = (1.0 + math.sqrt(5.0)) / 2.0

    def encode(self, s: SensorySnapshot) -> np.ndarray:
        rms = unit(s.audio_rms, 0.0, 1.0)
        freq = unit(s.dominant_frequency_hz, 0.0, 4000.0)
        flat = unit(s.spectral_flatness, 0.0, 1.0)
        phase = math.sin(finite(s.geometric_phase_rad))
        phase_v = signed(s.phase_velocity, 10.0)
        av = unit(s.av_coherence, 0.0, 1.0) * 2.0 - 1.0
        p = float(np.clip(finite(s.pleasure), -1.0, 1.0))
        a = unit(s.arousal, 0.0, 1.0) * 2.0 - 1.0
        d = unit(s.dominance, 0.0, 1.0) * 2.0 - 1.0
        audio_psi = math.sin(2.0 * math.pi * freq) * rms
        phi_h = math.cos(2.0 * math.pi * ((freq * self.PHI) % 1.0)) * (0.25 + 0.75 * rms)
        motion = unit(s.motion_energy, 0.0, 1.0)
        luminance = unit(s.luminance, 0.0, 1.0)
        mlc = 1.0 - min(1.0, abs(motion - luminance))
        mlc = mlc * 2.0 - 1.0
        ent = unit(s.entropy, 0.0, 1.0) * 2.0 - 1.0
        frequency_mass = math.sqrt(max(rms, 0.0)) * (2.0 * freq - 1.0)
        return np.asarray(
            [frequency_mass, phase, 2*flat-1, phase_v, av, p, a, d, audio_psi, phi_h, mlc, ent],
            dtype=np.float64,
        )
