from cns_bridge import CNSHarness, SensorySnapshot
from cns_bridge.backend import CallableBackend


def my_model(prompt, packet):
    # Replace this function with any local model, API, robot policy, planner, or agent.
    return f"MODEL SAW: {prompt} | CNS norm={float((packet.adaptive_54d**2).sum()**0.5):.3f}"


harness = CNSHarness(backend=CallableBackend(my_model, name="my-model"))
result = harness.run_step("Move safely toward the target.", SensorySnapshot(arousal=0.3))
print(result.response)
