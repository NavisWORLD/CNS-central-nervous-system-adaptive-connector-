from __future__ import annotations
from collections.abc import Awaitable, Callable
from typing import Protocol, runtime_checkable
import inspect
from .models import CNSPacket


@runtime_checkable
class CNSBackend(Protocol):
    async def generate(self, prompt: str, packet: CNSPacket) -> str: ...


class CallableBackend:
    """Wrap a user-provided sync or async function as a CNS backend."""

    def __init__(self, fn: Callable[[str, CNSPacket], str | Awaitable[str]], name: str = "callable"):
        self.fn = fn
        self.name = name

    async def generate(self, prompt: str, packet: CNSPacket) -> str:
        result = self.fn(prompt, packet)
        if inspect.isawaitable(result):
            result = await result
        return str(result)


class StateSummaryBackend:
    """Offline reference backend used by demos and tests."""

    name = "state-summary"

    async def generate(self, prompt: str, packet: CNSPacket) -> str:
        dominant = sorted(enumerate(abs(packet.adaptive_54d)), key=lambda p: p[1], reverse=True)[:4]
        dom = ", ".join(f"D{i+1}={packet.adaptive_54d[i]:+.3f}" for i, _ in dominant)
        source = packet.entropy.get("source", "unknown")
        return (
            f"CNS processed: {prompt.strip()} | dominant state: {dom} | "
            f"entropy source: {source} | memory hits: {len(packet.memory.get('recall', []))}."
        )
