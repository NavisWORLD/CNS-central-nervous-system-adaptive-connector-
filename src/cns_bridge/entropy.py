from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import secrets


EntropyCallable = Callable[[], float | None]


@dataclass(slots=True)
class EntropySample:
    value: float
    source: str
    live: bool = True


class CompositeEntropyBridge:
    """Fail-soft entropy/control bridge.

    External QRNG/quantum adapters are optional. If all external sources fail,
    the library uses cryptographic system entropy instead of blocking the CNS.
    """

    def __init__(self):
        self._sources: list[tuple[str, EntropyCallable]] = []

    def add_source(self, name: str, source: EntropyCallable) -> None:
        self._sources.append((str(name), source))

    def sample(self) -> EntropySample:
        for name, fn in self._sources:
            try:
                value = fn()
                if value is not None:
                    return EntropySample(max(0.0, min(1.0, float(value))), name, True)
            except Exception:
                continue
        return EntropySample(secrets.randbits(53) / float(2**53 - 1), "system_entropy", False)
