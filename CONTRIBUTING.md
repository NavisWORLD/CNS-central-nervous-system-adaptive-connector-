# Contributing

Thank you for improving the CNS Adaptive Connector.

## Principles

- Keep state schemas explicit and versionable.
- Keep optional integrations fail-soft.
- Add tests for numerical behavior.
- Do not commit API keys, tokens, private datasets, or private model weights.
- Distinguish measured, derived, replayed, simulated, inferred, and speculative data.
- Do not add claims of consciousness, biological equivalence, or quantum advantage without appropriate evidence.

## Development

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
```

## Pull requests

Explain:

- what changed;
- why;
- compatibility impact;
- tests performed;
- any new persistent state or privacy implications.
