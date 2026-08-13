# Downloads and Installation

## Prebuilt wheel

A locally validated Python wheel is committed under `dist/`:

`cns_adaptive_connector-0.1.0-py3-none-any.whl`

SHA-256:

`0c023608ffd8817607451b9dc04efd0a7f8f6b9135ead25ebf30402d4212ff2f`

Install it directly after downloading:

```bash
python -m pip install cns_adaptive_connector-0.1.0-py3-none-any.whl
```

The wheel was built from the repository source with no network dependency resolution and the source test suite passed before publication.

## Build from source

```bash
python -m pip install -e .[dev]
pytest -q
python -m build
```

The GitHub CI workflow validates supported Python versions and builds the package from source.
