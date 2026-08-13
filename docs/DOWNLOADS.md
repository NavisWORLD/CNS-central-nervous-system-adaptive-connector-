# Downloads and Installation

## Prebuilt wheel

A validated Python wheel is committed under `dist/`:

`cns_adaptive_connector-0.1.0-py3-none-any.whl`

SHA-256 of the exact wheel committed to GitHub:

`5913892a69e809db230929c101761757492c1ff892c9d1876330e2182d350d9b`

Install it directly after downloading:

```bash
python -m pip install cns_adaptive_connector-0.1.0-py3-none-any.whl
```

The release-verification workflow checks this exact committed artifact, installs it on clean Linux, Windows, and macOS runners, runs the CLI, and executes a complete CNS cycle.

## Build from source

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
```

The GitHub CI workflow validates supported Python versions and builds the package from source.
