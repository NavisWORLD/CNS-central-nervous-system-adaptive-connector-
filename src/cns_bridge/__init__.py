"""CNS Adaptive Connector public reference library."""

from .engine import CNSHarness, CNSResult
from .encoder import CNS12DEncoder, SensorySnapshot
from .models import CNSPacket
from .transformer import ReferenceStateTransformer
from .synaptic import (
    SENSORY_DIM,
    CONTEXT_DIM,
    STATE_DIM,
    encode_12d,
    expand_42d,
    hebbian_modulation,
    hebbian_update,
    adaptive_tail,
    assemble_54d,
    blend_54d,
)

__all__ = [
    "CNSHarness",
    "CNSResult",
    "CNS12DEncoder",
    "SensorySnapshot",
    "CNSPacket",
    "ReferenceStateTransformer",
    "SENSORY_DIM",
    "CONTEXT_DIM",
    "STATE_DIM",
    "encode_12d",
    "expand_42d",
    "hebbian_modulation",
    "hebbian_update",
    "adaptive_tail",
    "assemble_54d",
    "blend_54d",
]

__version__ = "0.1.0"
