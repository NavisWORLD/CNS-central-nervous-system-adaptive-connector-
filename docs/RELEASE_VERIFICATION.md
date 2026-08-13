# Release Verification Standard

This document defines what the project means by **verified runnable** for the public `cns-adaptive-connector` reference library.

A release is certified for this scope only when all of the following pass on GitHub-hosted clean runners:

1. source install succeeds;
2. complete pytest suite succeeds on Python 3.10, 3.11, and 3.12;
3. source distribution/wheel build succeeds;
4. the committed wheel's SHA-256 matches `dist/SHA256SUMS`;
5. that exact committed wheel installs on Linux, Windows, and macOS;
6. `cns-bridge status` executes after wheel installation;
7. `cns-bridge demo --json` completes a full CNS cycle;
8. the installed public API creates 12D, 42D, and 54D vectors of the promised shapes;
9. a custom backend receives the 54D packet;
10. recurrence increments state/memory/plasticity across cycles;
11. external entropy adapters work and fail-soft fallback remains tested;
12. vector memory save/load works;
13. Hebbian weight save/load works.

## Scope of certification

A PASS means the **public Python reference package and documented harness** are runnable for the tested environments and contracts.

It does not certify every possible third-party model, sensor, quantum provider, robot, operating environment, future dependency version, or downstream application. Those integrations must be tested by their integrator.

It also does not certify scientific claims outside the software behavior described in `SCIENTIFIC_BOUNDARIES.md`.

The final certification record is kept in `CERTIFICATION.md` after the release-verification workflow passes.
