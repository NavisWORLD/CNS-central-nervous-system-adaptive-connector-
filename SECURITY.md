# Security Policy

This repository is a reference library and should not be treated as a safety-certified controller.

## Never commit

- API keys or provider tokens
- private biometric recordings
- passwords
- proprietary model weights without distribution rights
- arbitrary serialized Python pickle files from untrusted sources

## Action safety

If a CNS backend can affect physical systems, financial transactions, accounts, infrastructure, or other consequential resources, place a deterministic authorization/safety layer after the backend and before execution.

Generated text is not authorization.

## Reporting

For security issues, use GitHub's private vulnerability reporting feature when available rather than opening a public issue containing exploit details.
