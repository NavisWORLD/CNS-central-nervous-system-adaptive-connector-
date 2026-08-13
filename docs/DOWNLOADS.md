# Downloads and Installation

## Prebuilt wheel

A validated Python wheel is committed under `dist/`:

`cns_adaptive_connector-0.1.0-py3-none-any.whl`

SHA-256 of the exact wheel committed to GitHub:

`7473f1d548ad69a6a4bc46b6ed352ab148a5f71539083521bdad73fe34597ad8`

Install it directly after downloading:

```bash
python -m pip install cns_adaptive_connector-0.1.0-py3-none-any.whl
```

This wheel is promoted only after the release-verification workflow builds it from source and installs/runs the same artifact on clean Linux, Windows, and macOS runners.

## Build from source

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
```

The GitHub CI workflow validates supported Python versions and builds the package from source.
